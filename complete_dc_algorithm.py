from rc_lstar import *
from complete_dc_sul import CompleteDCSUL
from complete_dc_oracle import CompleteDCOracle
from aalpy.utils import load_automaton_from_file, save_automaton_to_file
from aalpy.automata import DfaState, Dfa, MooreMachine, MooreState

# step 1 - make all "+" (bug) states terminal
# step 2 - unite all "+" states into one
# step 3 - remove unreachable states
# step 4 - mark all states that has a trajectory to a "+" state and as no trajectory to a "-" state
# step 5 - all marked are accepting states and the rest are non-accepting
# step 6 - make all accepting states terminal
# step 7 - minimize the automaton


def dfa_3_to_dfa(dfa_3, remove_sink=False):
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
            if all([s.transitions.get(a) == s for a in dfa.get_input_alphabet()]) and not s.is_accepting:
                sink_state = s
                break
        if sink_state is not None:
            for s in dfa.states:
                for a in dfa.get_input_alphabet():
                    if s.transitions.get(a) == sink_state:
                        s.transitions.pop(a)
            dfa.states.remove(sink_state)

    return dfa


def run(example):
    M = load_automaton_from_file(f'data/{example}/M.dot', automaton_type='dfa')
    B = load_automaton_from_file(f'data/{example}/B.dot', automaton_type='dfa')
    make_input_complete(M, missing_transition_go_to="sink_state")
    make_input_complete(B, missing_transition_go_to="sink_state")

    alphabet = M.get_input_alphabet()

    sul = CompleteDCSUL(M, B)
    oracle = CompleteDCOracle(alphabet, sul, M, B)

    dfa3, data = run_Lstar(alphabet,
                           sul,
                           oracle,
                           closing_strategy='longest_first',
                           cex_processing=None,
                           automaton_type='moore',
                           cache_and_non_det_check=False,
                           return_data=True,
                           print_level=0)


    dfa = dfa_3_to_dfa(dfa3)
    save_automaton_to_file(dfa, f'data/{example}/result.dot')




run('magento')
# run('coffee')
# run('threads_example')

