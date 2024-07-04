from aalpy.automata.Dfa import Dfa, DfaState
from aalpy.utils import load_automaton_from_file, save_automaton_to_file
from utils import minimize_dfa
from copy import deepcopy
"""
P0:      flag[0] = true; 0
P0_gate: turn = 1; 0
         while (flag[1] && turn == 1) 0, 0 enter
         {
             // busy wait
         }
         // critical section
         assert ! (flag[1] && flag[0])
         // end of critical section
         flag[0] = false; 0
"""


def p(i, d):
    while True:
        d["flags"][i] = True
        yield 0
        d["turn"] = 1 - i
        yield 1
        while d["flags"][1 - i] and d["turn"] == 1 - i:
            yield 1
        d["count"] += 1
        assert d["count"] == 1
        yield 2
        d["count"] -= 1
        d["flags"][i] = False
        yield 3

def in_crit(i):
    return p(i) == 3


visited = []
alphabet = [0, 1]

def get_continuation(w):
    d = {
        "flags": [False, False],
        "turn": 0,
        "count": 0
    }
    p0 = p(0, d)
    _p0 = 3
    p1 = p(1, d)
    _p1 = 3
    for i in range(len(w)):
        if w[i] == 0:
            _p0 = next(p0, d)
        else:
            _p1 = next(p1, d)
    if (d, _p0, _p1) not in visited:
        visited.append((d, _p0, _p1))
        print(w, d, _p0, _p1)
        for a in alphabet:
            get_continuation(w + [a])

#get_continuation([1,1])
get_continuation([])
print(len(visited))


# def main():
#     p0 = p(0, d)
#     p1 = p(1, d)
#
#
#
#
#
#
#
# def next(state, symbol):
#     (pcs, flags, turn) = state
#     pcs = list(pcs[:])
#     flags = list(flags[:])
#     increase = True
#     if pcs[symbol] == 0:
#         flags[symbol] = True
#     elif pcs[symbol] == 1:
#         turn = 1 - symbol
#     elif pcs[symbol] == 2:
#         if flags[1 - symbol] and turn == 1 - symbol:
#             increase = False
#     elif pcs[symbol] == 3:
#         flags[symbol] = False
#     if increase:
#         pcs[symbol] = (pcs[symbol] + 1) % 4
#     return tuple(pcs), tuple(flags), turn
#
#
# alphabet = [0, 1]
# visited = set()
# mapper = {}
# transitions_mapper = {}
# transitions = []
# stack = [((0, 0), (False, False), 0)]
# while len(stack) > 0:
#     state = stack.pop()
#     if state in visited:
#         continue
#     visited.add(state)
#     mapper[state] = len(mapper)
#     for symbol in alphabet:
#         next_state = next(state, symbol)
#         transitions.append((state, symbol, next_state))
#         transitions_mapper[(state, symbol)] = next_state
#         stack.append(next_state)
#
# # print("digraph G {")
# # for (state, symbol, next_state) in transitions:
# #     print(f'  "{state}" -> "{next_state}" [label="{symbol}"];')
# # print("}")
#
#
#
# def get_dfa(s, dfa_states):
#     s1 = DfaState(str(mapper[s]), is_accepting=any([x == 3 for x in s[0]]))
#     dfa_states.append(s1)
#     for a in alphabet:
#         n = transitions_mapper[(s, a)]
#         s_new = DfaState(str(mapper[n]), is_accepting=any([x == 3 for x in n[0]]))
#         s1.transitions["P" + str(a)] = s_new
#         if s_new.state_id not in [x.state_id for x in dfa_states]:
#             get_dfa(n, dfa_states)
#
#
# initial_state = ((0, 0), (False, False), 0)
# l = []
# get_dfa(initial_state, l)
#
# for s in l:
#     for a in alphabet:
#         s.transitions["P" + str(a)] = [x for x in l if x.state_id == s.transitions["P" + str(a)].state_id][0]
#
# dfa = Dfa(l[0], l)
# dfa = minimize_dfa(dfa)
# save_automaton_to_file(dfa, "data/peterson/M.dot")





