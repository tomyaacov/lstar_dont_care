from aalpy.automata.Dfa import Dfa, DfaState
import numpy as np


def initialize_table(dfa: Dfa):
    table = np.zeros((len(dfa.states), len(dfa.states)), dtype=bool)
    l = dfa.states
    for i in range(len(l)):
        for j in range(i+1, len(l)):
            if l[i].is_accepting != l[j].is_accepting:
                table[i,j] = True
                table[j,i] = True
    return table


def minimize_dfa(dfa: Dfa):
    state_to_id = {}
    id_to_state = {}
    states = dfa.states
    for i in range(len(states)):
        state_to_id[states[i]] = i
        id_to_state[i] = states[i]
    alphabet = dfa.get_input_alphabet()
    table = initialize_table(dfa)
    changed = True
    while changed:
        changed = False
        for i in range(len(states)):
            for j in range(i+1, len(states)):
                if not table[i, j]:
                    for s in alphabet:
                        next_i = state_to_id[id_to_state[i].transitions[s]]
                        next_j = state_to_id[id_to_state[j].transitions[s]]
                        if table[next_i, next_j]:
                            table[i, j] = True
                            table[j, i] = True
                            changed = True
    combinations = {}
    for i in range(len(states)):
        combinations[i] = {i}

    for i in range(len(states)):
        for j in range(i + 1, len(states)):
            if not table[i, j]:
                combinations[i].update(combinations[j])
                combinations[j].update(combinations[i])

    final_combinations = set([tuple(x) for x in combinations.values()])
    final_states = list()
    for combination in final_combinations:
        final_states.append(DfaState(combination, id_to_state[combination[0]].is_accepting))
    for state in final_states:
        for a in alphabet:
            for i in state.state_id:
                next = id_to_state[i].transitions[a]
                if next is not None:  # maybe not necessary
                    next_group_idx = [i for i, group in enumerate(final_combinations) if next.state_id in group][0]   # does it have to be determninstic
                    state.transitions[a] = final_states[next_group_idx]

    initial_state = final_states[[i for i, group in enumerate(final_combinations) if dfa.initial_state.state_id in group][0]]
    for state in final_states:
        state.state_id = str(state.state_id)
    return Dfa(initial_state, final_states)



# even A - works!
# states = list()
# for i in range(4):
#     states.append(DfaState(i))
#
# for i in range(4):
#     states[i].transitions["A"] = states[(i+1)%4]
#
# states[0].is_accepting = True
# states[2].is_accepting = True
#
# dfa = Dfa(states[0], states)

# from https://www.tutorialspoint.com/automata_theory/dfa_minimization.htm - works!
# states = list()
# states.append(DfaState(0))  # a
# states.append(DfaState(1))  # b
# states.append(DfaState(2))  # c
# states.append(DfaState(3))  # d
# states.append(DfaState(4))  # e
# states.append(DfaState(5))  # f
# states[0].transitions["0"] = states[1]
# states[0].transitions["1"] = states[2]
# states[1].transitions["0"] = states[0]
# states[1].transitions["1"] = states[3]
# states[2].transitions["0"] = states[4]
# states[2].transitions["1"] = states[5]
# states[3].transitions["0"] = states[4]
# states[3].transitions["1"] = states[5]
# states[4].transitions["0"] = states[4]
# states[4].transitions["1"] = states[5]
# states[5].transitions["0"] = states[5]
# states[5].transitions["1"] = states[5]
# states[2].is_accepting = True
# states[3].is_accepting = True
# states[4].is_accepting = True
# dfa = Dfa(states[0], states)

# random - works!
from aalpy.utils import generate_random_dfa
dfa = generate_random_dfa(6, ["A", "B"], 3)
dfa.execute_sequence()
print(dfa)
min_dfa = minimize_dfa(dfa)
print(min_dfa)
