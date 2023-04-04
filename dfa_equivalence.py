from aalpy.utils import load_automaton_from_file, save_automaton_to_file, make_input_complete
from aalpy.automata import DfaState, Dfa
import numpy as np
from automata.fa.dfa import DFA
from random import choice, random


def dfa_to_transtion_matrix(dfa):
    l = dfa.states
    S = np.zeros((1, len(l)))
    A = np.zeros((len(l), len(l)))
    F = np.zeros((len(l), 1))
    S[0, dfa.initial_state] = 1
    for i in l:
        if i in dfa.final_states:
            F[i] = 1
        for _, j in dfa.transitions[i].items():
            A[i, j] = 1
    return S, A, F


def aalpy_to_automata_lib_format(dfa):
    d = dict([(v, k) for k, v in enumerate(dfa.states)])
    states = set(d.values())
    input_symbols = set(dfa.get_input_alphabet())
    transitions = {}
    for s, i in d.items():
        transitions[i] = {}
        for a, s2 in s.transitions.items():
            transitions[i][a] = d[s2]
    initial_state = d[dfa.initial_state]
    final_states = set([i for s,i in d.items() if s.is_accepting])
    return DFA(states=states,
               input_symbols=input_symbols,
               transitions=transitions,
               initial_state=initial_state,
               final_states=final_states
               )
def automata_lib_to_aalpy_format(dfa):
    l = []
    init_index = dfa.initial_state
    for i in dfa.states:
        s = DfaState(i)
        s.is_accepting = i in dfa.final_states
        l.append(s)
    for i in dfa.states:
        for a, j in dfa.transitions[i].items():
            l[i].transitions[a] = l[j]
    return Dfa(l[init_index], l)


def get_sim_diff_dfa(dfa1, dfa2):
    A = aalpy_to_automata_lib_format(dfa1)
    B = aalpy_to_automata_lib_format(dfa2)
    return A ^ B


def get_intersection_dfa(dfa1, dfa2):
    A = aalpy_to_automata_lib_format(dfa1)
    B = aalpy_to_automata_lib_format(dfa2)
    C = A & B
    return automata_lib_to_aalpy_format(C)


def get_dfas_distance(dfa1, dfa2):
    sim_dif = get_sim_diff_dfa(dfa1, dfa2)
    S, A, F = dfa_to_transtion_matrix(sim_dif)
    B = (1/(2*len(dfa1.get_input_alphabet())))*A
    C = np.linalg.inv(np.eye(A.shape[0]) - B)
    return np.matmul(np.matmul(S, C), F)[0][0]


def sample_based_dfa_equivalence(dfa1, dfa2, n=1000, stop_prob=0.2):
    equivalent = 0
    for i in range(n//2):
        w = []
        while True:
            w.append(choice(dfa1.current_state.get_diff_state_transitions() + dfa1.current_state.get_same_state_transitions()))
            if random() <= stop_prob:
                break
        if dfa1.execute_sequence(dfa1.initial_state, w)[-1] == dfa2.execute_sequence(dfa2.initial_state, w)[-1]:
            equivalent += 1
    for i in range(n//2):
        w = []
        while True:
            w.append(choice(
                dfa2.current_state.get_diff_state_transitions() + dfa2.current_state.get_same_state_transitions()))
            if random() <= stop_prob:
                break
        if dfa1.execute_sequence(dfa1.initial_state, w)[-1] == dfa2.execute_sequence(dfa2.initial_state, w)[-1]:
            equivalent += 1
    return equivalent/n

if __name__ == '__main__':
    B1 = load_automaton_from_file("output/a.dot", automaton_type='dfa')
    B2 = load_automaton_from_file("output/b.dot", automaton_type='dfa')
    make_input_complete(B1, 'sink_state')
    make_input_complete(B2, 'sink_state')
    print(get_dfas_distance(B1, B2))
    print(sample_based_dfa_equivalence(B1, B2))


