from aalpy.base import SUL
from aalpy.base.Oracle import Oracle
from utils import get_intersection_dfa, get_diff_dfa, are_dfa_equivalent, aalpy_to_automata_lib_format
from aalpy.automata import Dfa, DfaState
from automata.base.exceptions import EmptyLanguageException
import sys
class CompleteDCOracle(Oracle):
    def __init__(self, alphabet: list, sul: SUL, M, B):
        super().__init__(alphabet, sul)
        self.M_intersect_B = get_intersection_dfa(M, B)
        self.M_diff_B = get_diff_dfa(M, B)
        self.equivalence_queries = 0

    def find_cex(self, hypothesis):
        self.equivalence_queries += 1
        c_plus = self.moore_to_dfa(hypothesis, "+")
        c_minus = self.moore_to_dfa(hypothesis, "-")
        if not are_dfa_equivalent(c_plus, self.M_intersect_B):
            A = aalpy_to_automata_lib_format(c_plus)
            B = aalpy_to_automata_lib_format(self.M_intersect_B)
            C = A - B
            D = B - A
            try:
                C_k = C.minimum_word_length()
            except EmptyLanguageException:
                C_k = sys.maxsize
            try:
                D_k = D.minimum_word_length()
            except EmptyLanguageException:
                D_k = sys.maxsize
            if C_k < D_k:
                for word in C.words_of_length(C_k):
                    return self.str_to_word(word)
            else:
                for word in D.words_of_length(D_k):
                    return self.str_to_word(word)
            raise Exception("No counterexample found")
        elif not are_dfa_equivalent(c_minus, self.M_diff_B):
            A = aalpy_to_automata_lib_format(c_minus)
            B = aalpy_to_automata_lib_format(self.M_diff_B)
            C = A - B
            D = B - A
            try:
                C_k = C.minimum_word_length()
            except EmptyLanguageException:
                C_k = sys.maxsize
            try:
                D_k = D.minimum_word_length()
            except EmptyLanguageException:
                D_k = sys.maxsize
            if C_k < D_k:
                for word in C.words_of_length(C_k):
                    return self.str_to_word(word)
            else:
                for word in D.words_of_length(D_k):
                    return self.str_to_word(word)
            raise Exception("No counterexample found")
        else:
            return None

    def reset_hyp_and_sul(self, hypothesis):
        pass

    def moore_to_dfa(self, machine, accepting_output):
        d = {}
        for s in machine.states:
            d[s.state_id] = DfaState(s.state_id, is_accepting=s.output==accepting_output)
        for s in machine.states:
            for a, s2 in s.transitions.items():
                d[s.state_id].transitions[a] = d[s2.state_id]
        initial_state = d[machine.initial_state.state_id]
        return Dfa(initial_state, list(d.values()))

    def str_to_word(self, s):
        l = []
        while len(s) > 0:
            for a in self.alphabet:
                if s.startswith(a):
                    l.append(a)
                    s = s[len(a):]
        return tuple(l)
