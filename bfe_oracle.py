from aalpy.oracles import BreadthFirstExplorationEqOracle
from itertools import product
from random import shuffle

class BFEOracle(BreadthFirstExplorationEqOracle):
    def __init__(self, alphabet, sul, depth=5):
        super().__init__(alphabet, sul, depth)
        self.queue = []

        # generate all test-cases
        for seq in product(self.alphabet, repeat=self.depth):
            self.queue.append(seq)

        shuffle(self.queue)
