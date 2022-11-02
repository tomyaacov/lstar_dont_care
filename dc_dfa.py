import numpy as np
from aalpy.base import Automaton
from aalpy.automata.Dfa import Dfa, DfaState
from itertools import combinations


def dfa3_to_tables(dfa3: Automaton):
    output_map = {"-": 0, "+": 1, "?": 2}
    alphabet = dfa3.get_input_alphabet()
    transitions = np.zeros((dfa3.size, len(alphabet)), dtype=int)
    outputs = np.zeros((dfa3.size, len(alphabet)), dtype=int)
    state_to_idx = dict()
    idx_to_state = dict()
    for i, s in enumerate(dfa3.states):
        state_to_idx[s] = i
        idx_to_state[i] = s
    for i, s in enumerate(dfa3.states):
        for j, a in enumerate(alphabet):
            next = s.transitions[a]
            transitions[i, j] = state_to_idx[next]
            outputs[i, j] = output_map[next.output]
    return transitions, outputs, state_to_idx[dfa3.initial_state]


def is_pair_aligned(i,j, outputs):
    return np.all((outputs[i, :] == 2) | (outputs[j, :] == 2) | (outputs[i, :] == outputs[j,:]))


def group_cover(group):
    x = set()
    for g in group:
        x.update(g)
    return len(x)

def group_closed(group, transitions):
    for g in group:
        for j in range(transitions.shape[1]):
            implied = set()
            for i in g:
                if transitions[i, j] != -1:
                    implied.add(transitions[i, j])
            flag = False
            for next_g in group:
                if implied.issubset(next_g):
                    flag = True
            if not flag:
                return False
    return True



def minimize_table(transitions, outputs, initial_state_old):
    pairs = dict()
    for i in range(outputs.shape[0]):
        for j in range(i + 1, outputs.shape[0]):
            if is_pair_aligned(i, j, outputs):
                l = set()
                for a in range(outputs.shape[1]):
                    next_i, next_j = transitions[i, a], transitions[j, a]
                    next_i, next_j = min(next_i, next_j), max(next_i, next_j)
                    if next_i != -1 and next_j != -1 and (next_i, next_j) != (i, j) and next_i != next_j:
                        l.add((next_i, next_j))
                if len(l) == 0:
                    pairs[(i, j)] = True
                else:
                    pairs[(i, j)] = l
            else:
                pairs[(i, j)] = False
    changed = True
    while changed:
        changed = False
        for k in pairs:
            if type(pairs[k]) == set:
                for p in pairs[k]:
                    if not pairs[p]:
                        pairs[k] = False
                        changed = True
    for i in range(outputs.shape[0]):
        for j in range(i + 1, outputs.shape[0]):
            if type(pairs[(i, j)]) == set:
                pairs[(i, j)] = True

    candidates = [set([x for x in range(1, outputs.shape[0])]),
                  set([0] + [x for x in range(1, outputs.shape[0]) if pairs[(0, x)]])]
    print(str(0 + 1) + ")", [[x + 1 for x in cand] for cand in candidates])
    for i in range(1, outputs.shape[0] - 1):
        new_candidates = []
        for cand in candidates:
            if i in cand:
                a = cand.copy()
                a.remove(i)
                b = {x for x in cand if pairs.get((i, x), True)}
                if b == cand:
                    new_candidates.append(cand)
                else:
                    new_candidates.append(a)
                    new_candidates.append(b)
            else:
                new_candidates.append(cand)
        without_sub_groups = []
        for cand in new_candidates:
            flag = True
            for cand2 in new_candidates:
                if cand.issubset(cand2) and len(cand) != len(cand2):
                    flag = False
                    break
            if flag and cand not in without_sub_groups:
                without_sub_groups.append(cand)
        candidates = without_sub_groups
        print(str(i + 1) + ")", [[x + 1 for x in cand] for cand in candidates])
    num_of_groups = 1
    while num_of_groups <= len(candidates):
        for group in combinations(candidates, num_of_groups):
            if group_cover(group) == outputs.shape[0] and group_closed(group, transitions):
                final_transitions = np.zeros((len(group), outputs.shape[1]), dtype=int)
                final_outputs = np.zeros((len(group), outputs.shape[1]), dtype=int)
                for i, g in enumerate(group):
                    for j in range(outputs.shape[1]):
                        t = 0  # default value
                        next_group = set()
                        o = 1  # default value
                        for item in g:
                            if transitions[item, j] != -1:
                                next_group.add(transitions[item, j])
                            if outputs[item, j] != 2:
                                o = outputs[item, j]
                        if len(next_group) > 0:
                            t = [idx for idx, next in enumerate(group) if next_group.issubset(next)][0]
                        final_transitions[i, j] = t
                        final_outputs[i, j] = o
                initial_state_new = [idx for idx, g in enumerate(group) if {initial_state_old}.issubset(g)][0]
                return final_transitions, final_outputs, initial_state_new
        num_of_groups += 1


def dfa_from_table(transitions, outputs, init_state_idx, alphabet):
    states = []
    for i in range(transitions.shape[0]):
        states.append(DfaState(i))
    for i in range(transitions.shape[0]):
        for j in range(transitions.shape[1]):
            states[i].transitions[alphabet[j]] = transitions[i,j]
            states[transitions[i,j]].is_accepting = bool(outputs[i,j])
    return Dfa(states[init_state_idx], states)


def find_minimal_consistent_dfa(dfa3: Automaton):
    transitions, outputs, init_state_idx = dfa3_to_tables(dfa3)
    final_transitions, final_outputs, init_state_idx = minimize_table(transitions, outputs, init_state_idx)
    dfa = dfa_from_table(final_transitions, final_outputs, init_state_idx, dfa3.get_input_alphabet())
    return dfa

# transitions = np.array([
#        [-1, 2, 4, 1],
#        [4, -1, -1, -1],
#        [5, 5, -1, -1],
#        [-1, -1, 1, -1],
#        [-1, 5, 0, 3],
#        [2, -1, 1, 2]])
# outputs = np.array([
#        [2, 1, 1, 1],
#        [0, 2, 2, 2],
#        [0, 1, 2, 2],
#        [2, 2, 1, 2],
#        [2, 0, 0, 1],
#        [0, 2, 0, 1]])

# table 4
# transitions = np.array([
#        [-1, 0, 1],
#        [0, 2, 1],
#        [2, 1, 0]])
# outputs = np.array([
#        [2, 0, 0],
#        [0, 0, 0],
#        [1, 0, 0]])

#table 3
# transitions = np.array([
#        [-1, 0],
#        [0, 2],
#        [3, 1],
#        [3, 1]])
# outputs = np.array([
#        [0, 0],
#        [0, 0],
#        [0, 0],
#        [1, 0]])
# final_transitions, final_outputs = minimize_table(transitions, outputs)
# print(final_transitions)
# print(final_outputs)