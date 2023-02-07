from automata.fa.dfa import DFA
from aalpy.utils import load_automaton_from_file
from aalpy.automata.Dfa import Dfa, DfaState

from aalpy.utils import save_automaton_to_file


def aalpy_to_automata_lib(dfa):
    if not dfa.is_input_complete():
        dfa.make_input_complete("self_loop")
    mapper = dict([(x, str(i)) for i, x in enumerate(dfa.states)])
    return DFA(
        states=set(list(mapper.values())),
        input_symbols=set(dfa.get_input_alphabet()),
        transitions=dict(
            [(str(i), dict([(k, mapper[v]) for k, v in s.transitions.items()])) for i, s in enumerate(dfa.states)]),
        initial_state=mapper[dfa.initial_state],
        final_states=set([mapper[x] for x in dfa.states if x.is_accepting])
    )

def automata_lib_to_aalpy(dfa):
    states = []
    states_dict = {}
    for s in dfa.states:
        states.append(DfaState(s))
        states_dict[s] = states[-1]
    for s,d in dfa.transitions.items():
        for e, next_s in d.items():
            states_dict[s].transitions[e] = states_dict[next_s]
    for s in dfa.final_states:
        states_dict[s].is_accepting = True
    return Dfa(states_dict[dfa.initial_state], states)



dfa_a = aalpy_to_automata_lib(load_automaton_from_file("output/magento_result_a_0.2.dot", "dfa"))
dfa_b = aalpy_to_automata_lib(load_automaton_from_file("output/magento_result_b_0.2.dot", "dfa"))
print(dfa_a == dfa_b)
minimal_difference_dfa = dfa_a - dfa_b
for i in range(1, 5):
    for j in range(10):
        print(minimal_difference_dfa.random_word(i))

save_automaton_to_file(automata_lib_to_aalpy(minimal_difference_dfa), "tmp")
# print(minimal_difference_dfa)
# difference_dfa = dfa_a.difference(dfa_b, minify=False)
# print(difference_dfa)
