from algorithm import learn
from fa_learner import FALearner
from dfa_encoder import DFAEncoder
from dfa3_encoder import DFA3Encoder
from test import Test
from aalpy.utils import load_automaton_from_file, make_input_complete
from aalpy.automata import MooreMachine, Dfa, MooreState, DfaState
from utils import get_intersection_dfa
from rc_lstar import run_Lstar
import time
from complete_dc_sul import CompleteDCSUL
from complete_dc_oracle import CompleteDCOracle
from complete_dfa_oracle import CompleteDFAOracle
from dfa3_to_data import *
from copy import deepcopy


def run(example):
    M = load_automaton_from_file(f'../data/{example}/M.dot', automaton_type='dfa')
    B = load_automaton_from_file(f'../data/{example}/B.dot', automaton_type='dfa')
    make_input_complete(M, missing_transition_go_to="sink_state")
    make_input_complete(B, missing_transition_go_to="sink_state")
    print(len((get_intersection_dfa(M, B)).states))
    alphabet = M.get_input_alphabet()

    sul = CompleteDCSUL(M, B)
    # print(B.execute_sequence(B.initial_state, ('C', 'C', 'B', 'D', 'C', 'C', 'C', 'B', 'D', 'C', 'B', 'D')))
    oracle = CompleteDCOracle(alphabet, sul, M, B)

    dfa3, data = run_Lstar(alphabet,
                           sul,
                           oracle,
                           closing_strategy='longest_first',
                           cex_processing=None,
                           automaton_type='moore',
                           cache_and_non_det_check=False,
                           return_data=True,
                           print_level=1)

    return dfa3, data, M, B


example = "magento"
d = []
for example in ["magento", "threads_example", "coffee", "coffee_new", "peterson"][1:2]:
    dfa3, data, M, B = run(example)
    print(len(dfa3.states))
    print(dfa3)

    print(data)

    # dfa3 = load_automaton_from_file("../data/3dfa_tests/magento2.dot", automaton_type="moore")
    # traces = dfa3_to_data(dfa3)

    # print(dfa3)
    # print(dfa3.execute_sequence(dfa3.initial_state, ('C', 'C', 'B', 'D', 'C', 'C', 'C', 'B', 'D', 'C', 'B', 'D')))

    # traces1 = get_table_data(dfa3, data["observation_table"])
    # print(len(traces1))
    # traces2 = get_dfs_data(dfa3)
    # print(len(traces2))
    #
    # print(traces1.issubset(traces2))
    # print(traces1.difference(traces2))
    # print(dfa3.execute_sequence(dfa3.initial_state, ('C', 'C', 'C', 'B', 'D', 'C', 'C', 'B', 'D', 'C', 'B', 'D')))
    # traces = get_dfs_data(dfa3)
    traces = get_table_data(dfa3, data["observation_table"])

    # traces.append((('C', 'B', 'N', 'C', 'B', 'D', 'C', 'C', 'C', 'B', 'D', 'C', 'B', 'D'), True))
    # traces.append((('C', 'C', 'B', 'D', 'C', 'C', 'C', 'B', 'D', 'C', 'B', 'D'), True))
    # traces.add((('C', 'C', 'C', 'B', 'D', 'C', 'C', 'B', 'D', 'C', 'B', 'D'), True))

    dfa3_new_condition = deepcopy(dfa3)

    learner_new_condition = FALearner(encoder=DFA3Encoder(dfa3_new_condition, True),
                                      oracle=CompleteDFAOracle(dfa3.get_input_alphabet(), dfa3_new_condition),
                                      alphabet=dfa3.get_input_alphabet(),
                                      max_states=len(dfa3_new_condition.states),
                                      use_all_traces=True,
                                      binary_search=True,
                                      minimize_self_loops=True,
                                      verbose=True)
    start_time = int(time.time() * 1000) / 1000
    (dfa_new_condition, statistics) = learn(learner_new_condition, [])  # traces)
    end_time = int(time.time() * 1000) / 1000
    print("Learning time: ", end_time - start_time)
    solver_time_new_condition = end_time - start_time
    print(dfa_new_condition)

    dfa3_regular = deepcopy(dfa3)

    learner_regular = FALearner(encoder=DFA3Encoder(dfa3_regular, False),
                                oracle=CompleteDFAOracle(dfa3.get_input_alphabet(), dfa3_regular),
                                alphabet=dfa3.get_input_alphabet(),
                                max_states=len(dfa3_regular.states),
                                use_all_traces=True,
                                binary_search=True,
                                minimize_self_loops=True,
                                verbose=True)
    start_time = int(time.time() * 1000) / 1000
    (dfa_regular, statistics) = learn(learner_new_condition, [])  # traces)
    end_time = int(time.time() * 1000) / 1000
    print("Learning time: ", end_time - start_time)
    solver_time_regular = end_time - start_time
    print(dfa_regular)

    d.append({
        "example": example,
        "T": len(M.states),
        "B": len((get_intersection_dfa(M, B)).states),
        "3DFA": len(dfa3.states),
        "learning rounds": data["learning_rounds"],
        "L^* learning time": data["total_time"],
        "membership queries": data["membership_queries"],
        "equivalence queries": data["equivalence_queries"],
        "system queries": data["system_queries"],
        "E": len(dfa_regular.states),
        "Solver time regular": solver_time_regular,
        "E_gal": len(dfa_new_condition.states),
        "Solver time gal": solver_time_new_condition
    })

first = True
for e in d:
    if first:
        first = False
        for k in e:
            print(k, end=",")
    print("")
    for k, v in e.items():
        print(v, end=",")
