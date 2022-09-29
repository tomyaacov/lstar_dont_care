from aalpy.base.Oracle import Oracle
from aalpy.automata.MooreMachine import MooreMachine
from magento_sul import DCSUL
from itertools import product
from random import shuffle


class DCOracle(Oracle):
    def __init__(self, alphabet, sul: DCSUL, depth=5):
        super().__init__(alphabet, sul)
        self.depth = depth
        self.l1_queue = []
        self.l2_queue = []

        # generate all test-cases
        for seq in product(self.alphabet, repeat=self.depth):
            input_seq = tuple([i for sub in seq for i in sub])
            self.l1_queue.append(input_seq)
            self.l2_queue.append(input_seq)

        shuffle(self.l1_queue)
        shuffle(self.l2_queue)

    def check_completeness(self, hypothesis: MooreMachine):

        # checking if L(c_minus) is contained in L1
        while self.l1_queue:
            test_case = self.l1_queue.pop()
            self.num_queries += 1
            hypothesis.reset_to_initial()
            for ind, letter in enumerate(test_case):
                try:
                    out_hyp = hypothesis.step(letter)
                    if out_hyp == "+":  # word in L(c_minus)
                        out_sul = self.sul.query(test_case[:ind + 1])[-1]
                        if out_sul in ["-", "?"]:  # word not in L1:
                            return test_case[:ind + 1], "L1"
                    self.num_steps += 1
                except KeyError:
                    break

        # checking if L(c_plus) contains L2 complement
        while self.l2_queue:
            test_case = self.l2_queue.pop()
            self.num_queries += 1
            hypothesis.reset_to_initial()
            for ind, letter in enumerate(test_case):
                try:
                    out_hyp = hypothesis.step(letter)
                    if out_hyp == "-":  # word not in L(c_plus)
                        out_sul = self.sul.query(test_case[:ind + 1])[-1]
                        if out_sul in ["+", "?"]:  # word not in L2:
                            return test_case[:ind + 1], "L2"
                    self.num_steps += 1
                except KeyError:
                    break

        return None  # complete

    def find_cex(self, hypothesis):
        raise NotImplementedError()
