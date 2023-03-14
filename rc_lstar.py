from aalpy.oracles import BreadthFirstExplorationEqOracle, RandomWalkEqOracle, RandomWMethodEqOracle

from bfe_oracle import BFEOracle
from dc_lstar import run_Lstar
from rc_sul import RCSUL
from rc_oracle import RCOracle, SampleBasedRCOracle
from aalpy.automata.Dfa import Dfa
from aalpy.automata.MealyMachine import MealyMachine
from dc_dfa import find_minimal_consistent_dfa
from aalpy.learning_algs.deterministic.ObservationTable import ObservationTable
import time
from aalpy.utils import load_automaton_from_file, save_automaton_to_file, make_input_complete
from aalpy.base.Oracle import Oracle
from aalpy.automata.MooreMachine import MooreMachine
from random import randint, choice, sample, random
from aalpy.learning_algs import run_RPNI

example = "coffee"

def observation_table_to_data(observation_table: ObservationTable):
    data = []
    for prefix in observation_table.T:
        labels = observation_table.T[prefix]
        for i, label in enumerate(labels):
            if label == "?":
                continue
            data.append((prefix + observation_table.E[i], label == "+"))
    return data

def dfa3_to_data(dfa3: MooreMachine):
    from itertools import product
    data = []
    data.append((tuple(), False))  # empty word is not a bug
    for i in range(1, 8):
        for l in product(dfa3.get_input_alphabet(), repeat=i):
            result = dfa3.execute_sequence(dfa3.initial_state, l)
            if result[-1] != "?":
                data.append((l, result[-1] == "+"))
    return data

def generate_tests(M, B, num_tests, cut_prob):
    failed_tests, passed_tests = set(), set()
    M.reset_to_initial()
    B.reset_to_initial()
    seq = []
    while len(failed_tests) + len(passed_tests) < num_tests or len(failed_tests) == 0 or len(passed_tests) == 0:
        available_transitions = M.current_state.get_diff_state_transitions() + M.current_state.get_same_state_transitions()
        if len(available_transitions) == 0 or (len(seq) > 0 and random() < cut_prob):
            if B.execute_sequence(B.initial_state, seq)[-1]:
                failed_tests.add(tuple(seq))
            else:
                passed_tests.add(tuple(seq))
            M.reset_to_initial()
            B.reset_to_initial()
            seq = []
        else:
            c = choice(available_transitions)
            M.step(c)
            seq.append(c)

    return failed_tests, passed_tests

M = load_automaton_from_file("data/our_models/" + example + "_m.dot", automaton_type='dfa')
B = load_automaton_from_file("data/our_models/" + example + "_b.dot", automaton_type='dfa')
failed_tests, passed_tests = generate_tests(M, B, 10, 0.2)

make_input_complete(M, 'sink_state')
sul = RCSUL(M, B, failed_tests=failed_tests, passed_tests=passed_tests)
oracle = RCOracle(M.get_input_alphabet(), sul, SampleBasedRCOracle(M.get_input_alphabet(), sul))
#oracle = RCOracle(M.get_input_alphabet(), sul, RandomWalkEqOracle(M.get_input_alphabet(), sul, num_steps=1000))
dfa3, data = run_Lstar(B.get_input_alphabet(), sul, oracle, closing_strategy='longest_first', cex_processing=None,
                       automaton_type='moore', cache_and_non_det_check=False, return_data=True, print_level=0)

print("dfa3 size:", dfa3.size)
print("system queries:", sul.system_queries)
save_automaton_to_file(dfa3, path="output/" + example + "_dfa3")

opt_a_start = time.time()
dfa_a, mealy_a = find_minimal_consistent_dfa(dfa3)
opt_a_time = time.time() - opt_a_start
print(opt_a_time)
print("dfa_a size: ", dfa_a.size)
save_automaton_to_file(dfa_a, path="output/" + example + "_dfa_a")
save_automaton_to_file(mealy_a, path="output/" + example + "_mealy_a")

print("option b:")
opt_b_start = time.time()
#rpni_data = dfa3_to_data(dfa3)
rpni_data = observation_table_to_data(data["observation_table"])  # not working!!!
dfa_b = run_RPNI(rpni_data, automaton_type="dfa")
opt_b_time = time.time() - opt_b_start
print(opt_b_time)
print("dfa_b size: ", dfa_b.size)
save_automaton_to_file(dfa_b, path="output/" + example + "_dfa_b")

















