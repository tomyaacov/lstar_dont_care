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
import z3

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
print(dfa3)


encoder = DFA3Encoder(dfa3)
number_of_states = 3
number_of_transitions = number_of_states * len(dfa3.get_input_alphabet()) + 1
fa, constraints = encoder.build(number_of_states, number_of_transitions, number_of_transitions)
solver = z3.Solver()
solver.set(unsat_core=True)
solver.add(constraints)

result = solver.check()

if result == z3.sat:
    model = solver.model()
    print(model)
    print("sat")
else:
    c = solver.unsat_core()
    print(len(c))
    print(c)
    print("unsat")
