from aalpy.utils import load_automaton_from_file, make_input_complete, save_automaton_to_file
from aalpy.automata import DfaState, Dfa, MooreMachine, MooreState
from aalpy.learning_algs import run_RPNI



# step 1 - make all "+" (bug) states terminal
# step 2 - unite all "+" states into one
# step 3 - remove unreachable states
# step 4 - mark all states that has a trajectory to a "+" state and as no trajectory to a "-" state
# step 5 - all marked are accepting states and the rest are non-accepting
# step 6 - make all accepting states terminal
# step 7 - minimize the automaton


def dfa_3_to_dfa(dfa_3, remove_sink=True):
    # step 1
    for s in dfa_3.states:
        if s.output == "+":
            for a in s.transitions:
                s.transitions[a] = s
    # step 2
    l = [s for s in dfa_3.states if s.output == "+"]
    united = MooreState("+", "+")
    for s in l:
        for a, new_s in s.transitions.items():
            united.transitions[a] = united
    for s in dfa_3.states:
        for a, new_s in s.transitions.items():
            if new_s in l:
                s.transitions[a] = united
    dfa_3.states.append(united)
    # step 3
    before = 0
    reachable = [dfa_3.initial_state]
    while len(reachable) != before:
        before = len(reachable)
        for s in reachable:
            for a, new_s in s.transitions.items():
                if new_s not in reachable:
                    reachable.append(new_s)
    dfa_3.states = reachable
    # step 4
    before = 0
    reach_reject = set([s for s in dfa_3.states if s.output == "-"])
    while len(reach_reject) != before:
        before = len(reach_reject)
        for s in dfa_3.states:
            for a, new_s in s.transitions.items():
                if new_s in reach_reject:
                    reach_reject.add(s)
    before = 0
    reach_accept = set([s for s in dfa_3.states if s.output == "+"])
    while len(reach_accept) != before:
        before = len(reach_accept)
        for s in dfa_3.states:
            for a, new_s in s.transitions.items():
                if new_s in reach_accept:
                    reach_accept.add(s)
    # step 5
    dfa_states = {}
    dfa_initial_state = None
    for s in dfa_3.states:
        if s in reach_accept and s not in reach_reject:
            dfa_states[s.state_id] = DfaState(s.state_id, True)
        else:
            dfa_states[s.state_id] = DfaState(s.state_id, False)
        if s == dfa_3.initial_state:
            dfa_initial_state = dfa_states[s.state_id]
    for s in dfa_3.states:
        for a, new_s in s.transitions.items():
            dfa_states[s.state_id].transitions[a] = dfa_states[new_s.state_id]
    dfa = Dfa(dfa_initial_state, list(dfa_states.values()))
    # step 6
    for s in dfa.states:
        if s.is_accepting:
            for a in s.transitions:
                s.transitions[a] = s
    before = 0
    reachable = [dfa.initial_state]
    while len(reachable) != before:
        before = len(reachable)
        for s in reachable:
            for a, new_s in s.transitions.items():
                if new_s not in reachable:
                    reachable.append(new_s)
    dfa.states = reachable
    # step 7
    dfa.minimize()
    if remove_sink:
        sink_state = None
        for s in dfa.states:
            if all([s.transitions.get(a) == s for a in dfa.get_input_alphabet()]):
                sink_state = s
                break
        if sink_state is not None:
            for s in dfa.states:
                for a in dfa.get_input_alphabet():
                    if s.transitions.get(a) == sink_state:
                        s.transitions.pop(a)
            dfa.states.remove(sink_state)

    return dfa

def dfa3_to_data(dfa3: MooreMachine):
    from itertools import product
    data = []
    data.append((tuple(), False))  # empty word is not a bug
    for i in range(1, 12):
        for l in product(dfa3.get_input_alphabet(), repeat=i):
            result = dfa3.execute_sequence(dfa3.initial_state, l)
            if result[-1] != "?":
                data.append((l, result[-1] == "+"))
    return data


name = "magento"
dfa_3 = load_automaton_from_file(f"data/3dfa_tests/{name}.dot", automaton_type='moore')
#print(dfa_3)
dfa = dfa_3_to_dfa(dfa_3, remove_sink=True)
save_automaton_to_file(dfa, f"data/3dfa_tests/{name}_alg.dot")
# rpni_data = dfa3_to_data(dfa_3)
# dfa_rpni = run_RPNI(rpni_data, automaton_type="dfa", print_info=False)
# save_automaton_to_file(dfa_rpni, f"data/3dfa_tests/{name}_rpni.dot")









