from aalpy.automata import DfaState, Dfa
from utils import get_diff_dfa, get_intersection_dfa
from aalpy.utils import load_automaton_from_file, save_automaton_to_file, make_input_complete
import os
alphabet = ["A", "B", "C", "D"]

def sigma_star():
    s = DfaState(0)
    s.is_accepting = True
    s.transitions = dict([(a, s) for a in alphabet])
    return Dfa(s, [s])

def make_prefix_closed(dfa):
    done = False
    while not done:
        done = True
        for s in dfa.states:
            for a, next_s in s.transitions.items():
                if next_s.is_accepting and not s.is_accepting:
                    done = False
                    s.is_accepting = True
    return dfa


def remove_sink_state(dfa):
    non_accepting = [s for s in dfa.states if not s.is_accepting]
    for s in dfa.states:
        l = list(s.transitions.keys())
        for a in l:
            if s.transitions[a] in non_accepting:
                s.transitions.pop(a)
    for s in non_accepting:
        dfa.states.remove(s)
    return dfa


def all_except(p):
    m = sigma_star()
    for file in os.listdir("data/patterns"):
        if str(p) + "." not in file:
            a = load_automaton_from_file("data/patterns/" + file, "dfa")
            make_input_complete(a, "sink_state")
            m = get_diff_dfa(m, a)
            m = make_prefix_closed(m)
    return m


for i in range(1, 7):
    print(i)
    b = load_automaton_from_file("data/patterns/" + str(i) + ".dot", "dfa")
    make_input_complete(b, "sink_state")
    m = all_except(i)
    m_b = get_intersection_dfa(m, b)
    m = remove_sink_state(m)
    print(len(m.states))
    print(len(m_b.states))
    save_automaton_to_file(m, "data/patterns_combined/" + str(i) + "_all_except_m.dot", "dot")
    save_automaton_to_file(m_b, "data/patterns_combined/" + str(i) + "_all_except_m_b.dot", "dot")

