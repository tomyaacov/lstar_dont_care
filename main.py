from rc_lstar import *
from generator_based_dfa import *
from aalpy.utils import load_automaton_from_file

def run_n_tests(example, bug, n, oracle_opt, test_set_size, name, dfa_generator_opt):
    c = Counter()

    for i in range(n):
        if isinstance(bug, str):
            B = load_automaton_from_file(bug, automaton_type='dfa')
            make_input_complete(B, missing_transition_go_to="sink_state")
        else:
            B = GeneratorBasedDFA(bug)

        c.update(run_single_test(load_automaton_from_file("data/our_models/" + example + ".dot", automaton_type='dfa'),
                                 B,
                                 oracle_opt,
                                 test_set_size,
                                 name,
                                 dfa_generator_opt))
    c = {k: v / n for k, v in c.items()}
    return c

# example = "magento"
# def bug():
#     while True:
#         c = yield False
#         if c == "LC":
#             while True:
#                 c = yield False
#                 if c == "C":
#                     while True:
#                         c = yield True
#         elif c.startswith("A"):
#             while True:
#                 c = yield False
# results = {}
# test_sample_size = 10
# n = 10
# oracles = ["SampleBasedRCOracle", "RandomWalkEqOracle", "RandomWMethodEqOracle"]
# for oracle_opt in oracles:
#     results[oracle_opt] = pd.DataFrame(columns=["#sessions",
#                                                 "#products",
#                                                     "fail_prob",
#                                                     "test_sample_size",
#                                                     "l_star_time",
#                                                     "membership_queries",
#                                                     "equivalence_queries",
#                                                     "system_queries",
#                                                     "dfa3_size",
#                                                     "dfa_time",
#                                                     "dfa_size",
#                                                     "sample_based_similarity"])
#     for i in range(1, 5):
#         for j in range(1, 5):
#             current = str(i) + "_" + str(j)
#             M = load_automaton_from_file("data/our_models/" + example + "_m_" + current + ".dot", automaton_type='dfa')
#             B = GeneratorBasedDFA(bug)
#             failed_tests, passed_tests = generate_tests(M, B, 100, 0.2)
#             fail_prob = len(failed_tests) / (len(failed_tests) + len(passed_tests))
#             current_results = run_n_tests(example + "_m_" + current, bug, n, oracle_opt, test_sample_size, example + "_" + current, 2)
#             current_results["#sessions"] = i
#             current_results["#products"] = j
#             current_results["fail_prob"] = fail_prob
#             current_results["test_sample_size"] = test_sample_size
#             results[oracle_opt] = results[oracle_opt].append(current_results, ignore_index=True)
#     results[oracle_opt].to_csv("output/" + example + "_" + oracle_opt + ".csv", index=False)



example = "coffee"
def bug():
    while True:
        c = yield False
        if c.startswith("C"):
            c = yield False
            if c.startswith("C"):
                c = yield False
                if c.startswith("C"):
                    while True:
                        c = yield True

# def bug():
#     true_n = 0
#     bug_n = 0
#     while True:
#         c = yield False
#         if c.startswith("C"):
#             true_n += int(c[1:])
#             if bug_n != 5 - int(c[1:]):
#                 bug_n += int(c[1:])
#         elif c.startswith("D"):
#             true_n -= int(c[1:])
#             bug_n -= int(c[1:])
#         elif c.startswith("B"):
#             if true_n >= int(c[1:]) > bug_n:
#                 while True:
#                     c = yield True

results = {}
test_sample_size = 10
n = 1
oracles = ["SampleBasedRCOracle", "RandomWalkEqOracle", "RandomWMethodEqOracle"]
for oracle_opt in oracles:
    print(oracle_opt)
    results[oracle_opt] = pd.DataFrame(columns=["#max_coins",
                                                "#coins_type",
                                                    "fail_prob",
                                                    "test_sample_size",
                                                    "l_star_time",
                                                    "membership_queries",
                                                    "equivalence_queries",
                                                    "system_queries",
                                                    "dfa3_size",
                                                    "dfa_time",
                                                    "dfa_size",
                                                    "sample_based_similarity"])
    for i in [6, 9, 12][:1]:
        for j in range(1, 2):
            current = str(i) + "_" + "1" + "_" + str(j)  # missing different drinks not yet implemented
            M = load_automaton_from_file("data/our_models/" + example + "_m_" + current + ".dot", automaton_type='dfa')
            B = GeneratorBasedDFA(bug)
            failed_tests, passed_tests = generate_tests(M, B, 100, 0.2)
            fail_prob = len(failed_tests) / (len(failed_tests) + len(passed_tests))
            current_results = run_n_tests(example + "_m_" + current, bug, n, oracle_opt, test_sample_size, example + "_" + current, 2)
            current_results["#max_coins"] = i
            current_results["#coins_type"] = j
            current_results["fail_prob"] = fail_prob
            current_results["test_sample_size"] = test_sample_size
            results[oracle_opt] = results[oracle_opt].append(current_results, ignore_index=True)
            results[oracle_opt].to_csv("output/" + example + "_" + oracle_opt + ".csv", index=False)



# example = "random"
#
# results = {}
# test_sample_size = 10
# n = 5
# oracles = ["SampleBasedRCOracle", "RandomWalkEqOracle", "RandomWMethodEqOracle"]
# for oracle_opt in oracles:
#     results[oracle_opt] = pd.DataFrame(columns=["#size",
#                                                 "#bug",
#                                                     "fail_prob",
#                                                     "test_sample_size",
#                                                     "l_star_time",
#                                                     "membership_queries",
#                                                     "equivalence_queries",
#                                                     "system_queries",
#                                                     "dfa3_size",
#                                                     "dfa_time",
#                                                     "dfa_size",
#                                                     "sample_based_similarity"])
#     for i in ["10_4", "20_5", "30_6"]:
#         for j in [1, 2, 3]:
#             current = str(i) + "_" + str(j)  # missing different drinks not yet implemented
#             M = load_automaton_from_file("data/our_models/" + example + "_m_" + str(i) + ".dot", automaton_type='dfa')
#             B = load_automaton_from_file("data/our_models/" + example + "_b_" + str(j) + ".dot", automaton_type='dfa')
#             make_input_complete(B, missing_transition_go_to="sink_state")
#             failed_tests, passed_tests = generate_tests(M, B, 100, 0.2)
#             fail_prob = len(failed_tests) / (len(failed_tests) + len(passed_tests))
#             current_results = run_n_tests(example + "_m_" + str(i), "data/our_models/" + example + "_b_" + str(j) + ".dot", n, oracle_opt, test_sample_size, example + "_" + current )
#             current_results["#size"] = i
#             current_results["#bug"] = str(j)
#             current_results["fail_prob"] = fail_prob
#             current_results["test_sample_size"] = test_sample_size
#             results[oracle_opt] = results[oracle_opt].append(current_results, ignore_index=True)
#     results[oracle_opt].to_csv("output/" + example + "_" + oracle_opt + ".csv", index=False)
