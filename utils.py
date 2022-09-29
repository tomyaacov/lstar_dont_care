from aalpy.learning_algs.deterministic.ObservationTable import ObservationTable
from collections import defaultdict
from itertools import combinations


def get_all_groupings(S):
    all_groupings = []
    for i in range(1, len(S)+1):
        all_groupings.extend(list(combinations(S, i)))
    return all_groupings

def is_group_covering(group, S):
    final = tuple()
    for member in group:
        final += member
    final = set(final)
    return len(final) == len(S)

def rows_closed(row1, row2):
    for i in range(len(row1)):
        if row1[i] in [0,1] and row2[i] in [0,1]:
            if row1[i] != row2[i]:
                return False
    return True


def is_group_closed(group, Q):
    for g in group:
        for s1, s2 in combinations(g, 2):
            if not rows_closed(Q[s1], Q[s2]):
                return False
    return True


def build_table(group, Q):
    final_table = defaultdict(tuple)
    for g in group:
        row = tuple()
        for i in range(len(Q[g[0]])):
            found = False
            for s in g:
                if Q[s][i] is not None:
                    row += (bool(Q[s][i]),)
                    found = True
                    break
            if not found:
                row += (True,)  # TODO: marking all unspecified as True
        for s in g:
            final_table[s] = row
    return final_table


def find_minimal_consistent_dfa(observation_table):

    Q = defaultdict(tuple)
    extended_S = list(observation_table.T.keys())

    for s in extended_S:
        for i in range(len(observation_table.E)):
            if observation_table.T[s][i] == "+":
                Q[s] += (1,)
            elif observation_table.T[s][i] == "-":
                Q[s] += (0,)
            else:
                Q[s] += (None,)
    all_groupings = get_all_groupings(extended_S)
    num_of_groups = 1
    while True:
        for group in combinations(all_groupings, num_of_groups):
            if is_group_covering(group, extended_S):
                if is_group_closed(group, Q):
                    final_dfa = ObservationTable(observation_table.alphabet, observation_table.sul, "dfa")
                    final_dfa.S = observation_table.S  # TODO: consider removing duplicate rows
                    final_dfa.E = observation_table.E
                    final_dfa.T = build_table(group, Q)
                    return final_dfa.gen_hypothesis(check_for_duplicate_rows=False)  # TODO: maybe change to True
        num_of_groups += 1


