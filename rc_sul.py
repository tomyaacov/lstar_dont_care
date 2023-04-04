from aalpy.base import SUL
from aalpy.automata.Dfa import Dfa


class RCSUL(SUL):

    def __init__(self, spec_dfa: Dfa, system_dfa: Dfa, failed_tests, passed_tests):
        super().__init__()
        self.spec_dfa = spec_dfa
        self.system_dfa = system_dfa
        self.failed_tests = failed_tests
        self.passed_tests = {tuple()}
        for p in passed_tests:
            for i in range(len(p)):
                self.passed_tests.add(p[:i + 1])
        self.num_queries = 0
        self.membership_queries = 0
        self.num_steps = 0
        self.system_queries = 0
        self.already_not_in_system = False
        self.already_failed_in_system = False
        self.prefix = []

    def query(self, word: tuple) -> list:
        if type(word) == list:
            word = tuple(word)
        self.num_queries += 1
        self.membership_queries += 1
        self.num_steps += len(word)
        if len(word) == 0:
            in_system = self.spec_dfa.initial_state.is_accepting
        else:
            in_system = self.spec_dfa.execute_sequence(self.spec_dfa.initial_state, word)[-1]
        if not in_system:
            return ["?"]
        if word in self.passed_tests:
            return ["-"]
        if word in self.failed_tests:
            return ["+"]
        self.system_queries += 1
        if len(word) == 0:
            failed_in_system = self.system_dfa.initial_state.is_accepting
        else:
            failed_in_system = self.system_dfa.execute_sequence(self.system_dfa.initial_state, word)[-1]
        if failed_in_system:
            return ["+"]
        else:
            return ["-"]



    def pre(self):
        self.spec_dfa.reset_to_initial()
        self.system_dfa.reset_to_initial()
        self.already_not_in_system = False
        self.already_failed_in_system = False
        self.prefix = []

    def post(self):
        pass

    def step(self, letter):
        self.num_steps += 1
        self.prefix.append(letter)
        in_system = self.spec_dfa.step(letter)
        if (not in_system) or self.already_not_in_system:
            self.already_not_in_system = True
            return "?"
        self.system_queries += 1
        failed_in_system = self.system_dfa.step(letter)
        if failed_in_system or self.already_failed_in_system:
            self.already_failed_in_system = True
            return "+"
        else:
            return "-"