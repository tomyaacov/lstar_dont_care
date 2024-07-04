from aalpy.utils import load_automaton_from_file, save_automaton_to_file, make_input_complete
from utils import get_product_dfa


T1 = load_automaton_from_file("data/threads/" + "_MT1A.dot", "dfa")
T2 = load_automaton_from_file("data/threads/" + "MT2A.dot", "dfa")

make_input_complete(T1, "sink_state")
make_input_complete(T2, "sink_state")

alphabet = T1.get_input_alphabet() + T2.get_input_alphabet()
l1 = T1.get_input_alphabet()
l2 = T2.get_input_alphabet()


for a in l1:
    T2.initial_state.transitions[a] = T2.initial_state

for a in l2:
    T1.initial_state.transitions[a] = T1.initial_state

make_input_complete(T1, "self_loop")
make_input_complete(T2, "self_loop")

A = get_product_dfa(T1, T2)

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

def mark_non_final_states(dfa):
    for s in dfa.states:
        if len(s.transitions) != 0:
            s.is_accepting = False
    return dfa

A = make_prefix_closed(A)
A = remove_sink_state(A)
A = mark_non_final_states(A)

save_automaton_to_file(A, "data/threads_combined/" + "MA.dot", "dot")






