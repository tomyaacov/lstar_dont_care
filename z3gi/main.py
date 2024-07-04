from algorithm import learn
from fa_learner import FALearner
from dfa_encoder import DFAEncoder
from dfa3_encoder import DFA3Encoder
from test import Test
from aalpy.utils import load_automaton_from_file, make_input_complete
from aalpy.automata import MooreMachine, Dfa, MooreState, DfaState

from rc_lstar import run_Lstar
import time
from complete_dc_sul import CompleteDCSUL
from complete_dc_oracle import CompleteDCOracle
from complete_dfa_oracle import CompleteDFAOracle
from dfa3_to_data import *


def run(example):
    M = load_automaton_from_file(f'../data/{example}/M.dot', automaton_type='dfa')
    B = load_automaton_from_file(f'../data/{example}/B.dot', automaton_type='dfa')
    make_input_complete(M, missing_transition_go_to="sink_state")
    make_input_complete(B, missing_transition_go_to="sink_state")

    alphabet = M.get_input_alphabet()

    sul = CompleteDCSUL(M, B)
    #print(B.execute_sequence(B.initial_state, ('C', 'C', 'B', 'D', 'C', 'C', 'C', 'B', 'D', 'C', 'B', 'D')))
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

    return dfa3, data


example = "magento"
dfa3, data = run(example)
print(len(dfa3.states))

#dfa3 = load_automaton_from_file("../data/3dfa_tests/magento2.dot", automaton_type="moore")
#traces = dfa3_to_data(dfa3)

#print(dfa3)
#print(dfa3.execute_sequence(dfa3.initial_state, ('C', 'C', 'B', 'D', 'C', 'C', 'C', 'B', 'D', 'C', 'B', 'D')))

# traces1 = get_table_data(dfa3, data["observation_table"])
# print(len(traces1))
traces2 = get_dfs_data(dfa3)
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
learner = FALearner(encoder=DFAEncoder(),
                    oracle=CompleteDFAOracle(dfa3.get_input_alphabet(), dfa3),
                    alphabet=dfa3.get_input_alphabet(),
                    max_states=len(dfa3.states),
                    use_all_traces=True,
                    binary_search=True,
                    minimize_self_loops=True,
                    verbose=True)
start_time = int(time.time() * 1000) / 1000
(dfa, statistics) = learn(learner, traces)
end_time = int(time.time() * 1000) / 1000
print("Learning time: ", end_time - start_time)
print(dfa)