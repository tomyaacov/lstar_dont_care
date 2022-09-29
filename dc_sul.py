from aalpy.base import SUL
from aalpy.automata.Dfa import Dfa


class DCSUL(SUL):

    def __init__(self):
        super().__init__()

    def query(self, word: tuple) -> list:
        initial_output = self.pre()
        out = [initial_output]
        for letter in word:
            out.append(self.step(letter))
        self.post()
        self.num_queries += 1
        self.num_steps += len(word)
        return out

    def check_soundness(self, hypothesis: Dfa, alphabet=None):
        pass

    def pre(self):
        pass

    def post(self):
        pass

    def step(self, letter):
        pass
