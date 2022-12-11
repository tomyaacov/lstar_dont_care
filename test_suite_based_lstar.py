from aalpy.automata import MooreMachine

from dc_lstar import run_Lstar
from test_oracle import TestOracle
from test_sul import TestSUL
from dc_dfa import find_minimal_consistent_dfa
import random
from aalpy.learning_algs.deterministic.ObservationTable import ObservationTable
import csv
from aalpy.base import Automaton
import time
import pandas as pd


def observation_table_to_data(observation_table: ObservationTable):
    data = []
    for prefix in observation_table.S:
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


def accuracy(hypothesis: Automaton, passed_tests, failed_tests):
    # sanity check
    counter = 0
    print("misclassified passed tests:")
    for t in passed_tests:
        if len(t) == 0: continue
        output = hypothesis.execute_sequence(hypothesis.initial_state, t)
        if output[-1] != 0:
            counter += 1
            print("not equivalent:", t)
    print("misclassified failed tests:")
    for t in failed_tests:
        output = hypothesis.execute_sequence(hypothesis.initial_state, t)
        if output[-1] != 1:
            counter += 1
            print("not equivalent:", t)
    return (len(passed_tests) + len(passed_tests) - counter) / (len(passed_tests) + len(passed_tests))


if __name__ == "__main__":
    from aalpy.utils import save_automaton_to_file
    from aalpy.learning_algs import run_RPNI
    import csv

    alphabet = ["L1", "L2", "A", "C"]

    with open('data/system_dfa.csv', newline='') as f:
        reader = csv.reader(f)
        total_traces = list(reader)
        total_traces = [(tuple(x[:-1]), x[-1] == "True") for x in total_traces]

    with open('data/spec_dfa.csv', newline='') as f:
        reader = csv.reader(f)
        spec_data = list(reader)
        spec_data = [(tuple(x[:-1]), x[-1] == "True") for x in spec_data]

    spec_dfa = run_RPNI(spec_data, automaton_type="dfa")
    save_automaton_to_file(spec_dfa, path="output/spec_dfa")
    system_dfa = run_RPNI(total_traces, automaton_type="dfa")
    save_automaton_to_file(system_dfa, path="output/system_dfa")

    results = pd.DataFrame(columns=["test_coverage",
                                    "l_star_learning_time",
                                    "l_star_queries_membership",
                                    "l_star_queries_equivalence",
                                    "3dfa_size",
                                    "l_star_system_queries",
                                    "option_a_time",
                                    "option_a_dfa_size",
                                    "opt_a_acc",
                                    "option_b_time",
                                    "option_b_dfa_size",
                                    "opt_b_acc",
                                    ])

    for test_coverage in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        passed_tests = set([w for w, l in total_traces if l and random.random() <= test_coverage])
        failed_tests = set([w for w, l in total_traces if not l and random.random() <= test_coverage])

        sul = TestSUL(failed_tests, passed_tests, spec_dfa, system_dfa)
        oracle = TestOracle(alphabet, sul, sample_size=10, min_walk_len=1, max_sample_len=7)

        dfa3, data = run_Lstar(alphabet, sul, oracle, cex_processing='rs', closing_strategy='single',
                               automaton_type='moore', cache_and_non_det_check=False, return_data=True)
        save_automaton_to_file(dfa3, path="output/magento_dfa3_" + str(test_coverage))

        print("option a:")
        opt_a_start = time.time()
        dfa_a = find_minimal_consistent_dfa(dfa3)
        opt_a_time = time.time() - opt_a_start
        save_automaton_to_file(dfa_a, path="output/magento_result_a_" + str(test_coverage))
        opt_a_acc = accuracy(dfa_a,
                             set([w for w, l in total_traces if l]),
                             set([w for w, l in total_traces if not l]))

        print("option b:")
        opt_b_start = time.time()
        rpni_data = dfa3_to_data(dfa3)
        # rpni_data = observation_table_to_data(data["observation_table"]) # not working!!!
        dfa_b = run_RPNI(rpni_data, automaton_type="dfa")
        opt_b_time = time.time() - opt_b_start
        save_automaton_to_file(dfa_b, path="output/magento_result_b_" + str(test_coverage))
        opt_b_acc = accuracy(dfa_b,
                             set([w for w, l in total_traces if l]),
                             set([w for w, l in total_traces if not l]))

        results = results.append({"test_coverage": test_coverage,
                                  "l_star_learning_time": data["total_time"],
                                  "l_star_queries_membership": data["queries_learning"],
                                  "l_star_queries_equivalence": data["queries_eq_oracle"],
                                  "3dfa_size": dfa3.size,
                                  "l_star_system_queries": sul.system_queries,
                                  "option_a_time": opt_a_time,
                                  "option_a_dfa_size": dfa_a.size,
                                  "opt_a_acc": opt_a_acc,
                                  "option_b_time": opt_b_time,
                                  "option_b_dfa_size": dfa_b.size,
                                  "opt_b_acc": opt_b_acc
                                  },
                                 ignore_index=True)

        results.to_csv("output/magento_results.csv",index=False)
