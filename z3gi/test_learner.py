import automata.base.exceptions

from algorithm import learn
from fa_learner import FALearner
from dfa_encoder import DFAEncoder
from dfa3_encoder import DFA3Encoder
from test import Test
from aalpy.utils import load_automaton_from_file, make_input_complete, generate_random_moore_machine
from aalpy.automata import MooreMachine, Dfa, MooreState, DfaState

from rc_lstar import run_Lstar
import time
from complete_dc_sul import CompleteDCSUL
from complete_dc_oracle import CompleteDCOracle
from complete_dfa_oracle import CompleteDFAOracle
from dfa3_to_data import *
import random
from utils import aalpy_to_automata_lib_format, automata_lib_to_aalpy_format

NUM_STATES_MIN = 3
NUM_STATES_MAX = 5
ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
NUM_INPUTS_MIN = 2
NUM_INPUTS_MAX = 5


def moore_to_dfa(machine, accepting_output):
    d = {}
    for s in machine.states:
        d[s.state_id] = DfaState(s.state_id, is_accepting=s.output == accepting_output)
    for s in machine.states:
        for a, s2 in s.transitions.items():
            d[s.state_id].transitions[a] = d[s2.state_id]
    initial_state = d[machine.initial_state.state_id]
    return Dfa(initial_state, list(d.values()))

def random_3dfa():
    return generate_random_moore_machine(num_states=random.randint(NUM_STATES_MIN, NUM_STATES_MAX),
                                         input_alphabet=ALPHABET[:random.randint(NUM_INPUTS_MIN, NUM_INPUTS_MAX)],
                                         output_alphabet=["+", "-", "?"])

def test():
    for i in range(NUM_STATES_MIN, NUM_STATES_MAX + 1):
        for j in range(NUM_INPUTS_MIN, NUM_INPUTS_MAX + 1):
            for k in range(5):
                dfa3 = generate_random_moore_machine(num_states=i,
                                                     input_alphabet=ALPHABET[:j],
                                                     output_alphabet=["+", "-", "?"])

                B = moore_to_dfa(dfa3, "+")
                M_complement = moore_to_dfa(dfa3, "?")
                M = automata_lib_to_aalpy_format(aalpy_to_automata_lib_format(M_complement).complement())
                sul = CompleteDCSUL(M, B)
                oracle = CompleteDCOracle(dfa3.get_input_alphabet(), sul, M, B)

                dfa3, data = run_Lstar(dfa3.get_input_alphabet(),
                                       sul,
                                       oracle,
                                       closing_strategy='longest_first',
                                       cex_processing=None,
                                       automaton_type='moore',
                                       cache_and_non_det_check=False,
                                       return_data=True,
                                       print_level=0)

                option_a = []
                learner = FALearner(encoder=DFA3Encoder(dfa3),
                                    oracle=CompleteDFAOracle(dfa3.get_input_alphabet(), dfa3),
                                    alphabet=dfa3.get_input_alphabet(),
                                    max_states=len(dfa3.states),
                                    use_all_traces=True,
                                    binary_search=True,
                                    minimize_self_loops=True,
                                    verbose=False)
                start_time = int(time.time() * 1000) / 1000
                (dfa, statistics) = learn(learner, [])  # traces)
                end_time = int(time.time() * 1000) / 1000
                option_a.append(end_time - start_time)
                option_b = []
                learner = FALearner(encoder=DFAEncoder(),
                                    oracle=CompleteDFAOracle(dfa3.get_input_alphabet(), dfa3),
                                    alphabet=dfa3.get_input_alphabet(),
                                    max_states=len(dfa3.states),
                                    use_all_traces=True,
                                    binary_search=True,
                                    minimize_self_loops=True,
                                    verbose=False)
                start_time = int(time.time() * 1000) / 1000
                traces = get_table_data(dfa3, data["observation_table"])
                try:
                    (dfa, statistics) = learn(learner, traces)
                except automata.base.exceptions.SymbolMismatchError:
                    "hiii"
                    continue
                end_time = int(time.time() * 1000) / 1000
                option_b.append(end_time - start_time)
            print("states,", i, ",alphabet,", j, ",option a,", sum(option_a) / len(option_a), ",option b,", sum(option_b) / len(option_b))
            print()

test()

# dfa3=random_3dfa()
# print(dfa3)
# learner = FALearner(encoder=DFA3Encoder(dfa3),
#                     oracle=CompleteDFAOracle(dfa3.get_input_alphabet(), dfa3),
#                     alphabet=dfa3.get_input_alphabet(),
#                     max_states=len(dfa3.states),
#                     use_all_traces=True,
#                     binary_search=True,
#                     minimize_self_loops=True,
#                     verbose=True)
# start_time = int(time.time() * 1000) / 1000
# (dfa, statistics) = learn(learner, [])#traces)
# end_time = int(time.time() * 1000) / 1000
# print("Learning time: ", end_time - start_time)
# print(dfa)