from aalpy.automata.Dfa import Dfa, DfaState
from aalpy.utils import load_automaton_from_file, save_automaton_to_file, make_input_complete
import random
from utils import get_intersection_dfa

alphabets = [['A', 'B', 'C', "D"], ['A', 'B', 'C', "D", "E"], ['A', 'B', 'C', "D", "E", "F"]]
sizes = [10, 20, 30]
bugs = [
    load_automaton_from_file("data/our_models/random_b_1.dot", automaton_type="dfa"),
    load_automaton_from_file("data/our_models/random_b_2.dot", automaton_type="dfa"),
    load_automaton_from_file("data/our_models/random_b_3.dot", automaton_type="dfa"),
]
for j in range(len(bugs)):
    make_input_complete(bugs[j], missing_transition_go_to="sink_state")

for s, a in zip(sizes, alphabets):
    while True:
        states = [DfaState(i, is_accepting=True) for i in range(s)]
        for i in range(len(states)):
            for letter in a:
                if random.random() > 0.5:
                    states[i].transitions[letter] = states[random.randint(0, s - 1)]
        m = Dfa(states[0], states)
        save_automaton_to_file(m, f"data/our_models/random_m_{s}_{len(a)}")
        make_input_complete(m, missing_transition_go_to="sink_state")
        for i in range(len(states)):
            for l in alphabets[-1]:
                if l not in states[i].transitions:
                    states[i].transitions[l] = states[-1]
        make_input_complete(m, missing_transition_go_to="sink_state")
        all_good = True
        for j in range(len(bugs)):
            b_i_m = get_intersection_dfa(bugs[j], m)
            if len(b_i_m.states) <= 1:
                all_good = False
                break
            save_automaton_to_file(b_i_m, f"data/our_models/random_m_{s}_{len(a)}_intersection_b_{j + 1}")
        if all_good:
            break




