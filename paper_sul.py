from dc_sul import DCSUL
from aalpy.automata.Dfa import Dfa
import re
from itertools import product


class PaperSUL(DCSUL):

    def __init__(self):
        super().__init__()
        self.L1_reg = re.compile("(a*b+a+b+)(a+b+a+b+)*")
        self.L2_reg = re.compile("a*(b*a+)*")
        self.current_state = ""

    def pre(self):
        self.current_state = ""
        return self.get_current_label()

    def post(self):
        pass

    def step(self, letter):
        self.current_state += letter
        return self.get_current_label()

    def get_current_label(self):
        if self.L1_reg.fullmatch(self.current_state):
            return "+"
        elif self.L2_reg.fullmatch(self.current_state):
            return "-"
        else:
            return "?"

    def check_soundness(self, hypothesis: Dfa, alphabet, depth=5):
        # generate all test-cases - not efficient
        for d in range(depth+1):
            for seq in product(alphabet, repeat=d):
                test_case = tuple([i for sub in seq for i in sub])
                hypothesis.reset_to_initial()
                for ind, letter in enumerate(test_case):
                    try:
                        out_sul = self.query(test_case[:ind + 1])[-1]
                        if out_sul == "+":
                            out_hyp = hypothesis.step(letter)
                            if not out_hyp:  # word not in A:
                                return test_case[:ind + 1], "L1"  # word in L1 but not in A
                        if out_sul == "-":
                            out_hyp = hypothesis.step(letter)
                            if out_hyp:  # word in A:
                                return test_case[:ind + 1], "L2"  # word in A and in L2
                    except KeyError:
                        break





