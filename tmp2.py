# from aalpy.utils import load_automaton_from_file, make_input_complete, save_automaton_to_file
# from aalpy.automata import DfaState, Dfa
#
# M = load_automaton_from_file("data/threads_combined/M_B_A.dot", automaton_type='dfa')
#
#
# def duplicate_transitions(dfa):
#     states_list = []
#     for s in dfa.states:
#         states_list.append(DfaState(s.state_id, s.is_accepting))
#     for s in dfa.states:
#         for a, next_s in s.transitions.items():
#             states_list.append(DfaState(s.state_id + a + next_s.state_id, False))
#             copy_s = [x for x in states_list if x.state_id == s.state_id][0]
#             copy_next_s = [x for x in states_list if x.state_id == next_s.state_id][0]
#             copy_s.transitions[a + "A"] = states_list[-1]
#             states_list[-1].transitions[a + "B"] = copy_next_s
#     copy_initial = [x for x in states_list if x.state_id == dfa.initial_state.state_id][0]
#     return Dfa(copy_initial, states_list)
#
#
# M_trans = duplicate_transitions(M)
# save_automaton_to_file(M_trans, "data/threads_transitions/" + "M_B_A.dot", "dot")



from aalpy.utils import load_automaton_from_file, make_input_complete, save_automaton_to_file
from aalpy.automata import DfaState, Dfa

M = load_automaton_from_file("data/threads_transitions/MA.dot", automaton_type='dfa')


def duplicate_transitions(dfa):
    states_list = []
    for s in dfa.states:
        states_list.append(DfaState(s.state_id, s.is_accepting))
    for s in dfa.states:
        for a, next_s in s.transitions.items():
            copy_s = [x for x in states_list if x.state_id == s.state_id][0]
            copy_next_s = [x for x in states_list if x.state_id == next_s.state_id][0]
            copy_s.transitions[a] = copy_next_s
            copy_next_s.transitions[a] = copy_next_s
    copy_initial = [x for x in states_list if x.state_id == dfa.initial_state.state_id][0]
    return Dfa(copy_initial, states_list)


M_trans = duplicate_transitions(M)
save_automaton_to_file(M_trans, "data/threads_transitions/" + "MA_2.dot", "dot")

