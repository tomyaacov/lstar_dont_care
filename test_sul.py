from aalpy.base import SUL
from aalpy.automata.Dfa import Dfa


class TestSUL(SUL):

    def __init__(self, failed: set, passed: set, spec_dfa: Dfa, system_dfa: Dfa):
        super().__init__()
        self.failed = failed
        self.passed = set()
        for p in passed:
            for i in range(len(p)):
                self.passed.add(p[:i+1])
        self.spec_dfa = spec_dfa
        self.system_dfa = system_dfa

    def query(self, word: tuple) -> list:
        if len(word) == 0:
            in_system = self.spec_dfa.initial_state.is_accepting
        else:
            in_system = self.spec_dfa.execute_sequence(self.spec_dfa.initial_state, word)[-1]
        if not in_system:
            return ["?"]
        if word in self.passed:
            return ["-"]
        if word in self.failed:
            return ["+"]
        if len(word) == 0:
            passed_in_system = self.system_dfa.initial_state.is_accepting
        else:
            passed_in_system = self.system_dfa.execute_sequence(self.spec_dfa.initial_state, word)[-1]
        if passed_in_system:
            return ["-"]
        else:
            return ["+"]


    def pre(self):
        pass

    def post(self):
        pass

    def step(self, letter):
        pass


