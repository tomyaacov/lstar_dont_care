from generator_based_dfa import GeneratorBasedDFA
from rc_lstar import *
from aalpy.utils import load_automaton_from_file
from random import shuffle, sample
from threads_bug_finding2 import program

def run_n_tests(p, bug, n, oracle_opt, test_set_size, name, dfa_generator_opt, test_generator_opt="random_walk"):
    c = Counter()

    for i in range(n):
        if isinstance(bug, str):
            B = load_automaton_from_file(bug, automaton_type='dfa')
            make_input_complete(B, missing_transition_go_to="sink_state")
        else:
            B = GeneratorBasedDFA(bug)

        c.update(run_single_test(load_automaton_from_file("data/threads_combined/M" + str(p) + ".dot", automaton_type='dfa'),
                                 B,
                                 oracle_opt,
                                 test_set_size,
                                 name,
                                 dfa_generator_opt,
                                 test_generator_opt,
                                 is_system_prefix_closed=False))
    c = {k: v / n for k, v in c.items()}
    return c

def test_gen1(M, B, num_tests):
    failed_tests, passed_tests = set(), set()
    word = ["T1"] * 10 + ["T2", "T2", "T2"]
    while len(failed_tests) + len(passed_tests) < num_tests or len(failed_tests) == 0 or len(passed_tests) == 0:
        shuffle(word)
        if B.execute_sequence(B.initial_state, word)[-1]:
            failed_tests.add(tuple(word))
        else:
            passed_tests.add(tuple(word))
        M.reset_to_initial()
        B.reset_to_initial()

    # make_input_complete(M, missing_transition_go_to="sink_state")
    # from itertools import product
    # data = []
    # data.append((tuple(), False))  # empty word is not a bug
    # for word in product(["T1", "T2"], repeat=13):
    #     M.reset_to_initial()
    #     B.reset_to_initial()
    #     if not M.execute_sequence(M.initial_state, word)[-1]:
    #         continue
    #     if B.execute_sequence(B.initial_state, word)[-1]:
    #         failed_tests.add(tuple(word))
    #     else:
    #         passed_tests.add(tuple(word))

    return failed_tests, passed_tests

def test_gen2(M, B, num_tests):
    failed_tests, passed_tests = set(), set()
    a = ["T11", "T12"] * 10
    b = ["T21", "T22", "T23"]
    while len(failed_tests) + len(passed_tests) < num_tests or len(failed_tests) == 0 or len(passed_tests) == 0:
        word = list(map(next, sample([iter(a)] * len(a) + [iter(b)] * len(b), len(a) + len(b))))
        if B.execute_sequence(B.initial_state, word)[-1]:
            failed_tests.add(tuple(word))
        else:
            passed_tests.add(tuple(word))
        M.reset_to_initial()
        B.reset_to_initial()

    return failed_tests, passed_tests


results = {}
test_sample_size = 100
n = 1
oracles = ["SampleBasedRCOracle", "RandomWalkEqOracle", "RandomWMethodEqOracle"][:1]
for oracle_opt in oracles:
    print(oracle_opt)
    results[oracle_opt] = pd.DataFrame(columns=["pattern",
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
    i = "A"
    M = load_automaton_from_file("data/threads_combined/M" + str(i) + ".dot", automaton_type='dfa')
    B = GeneratorBasedDFA(program)
    failed_tests, passed_tests = generate_tests(M, B, 100, 0.2, method=test_gen1)
    fail_prob = len(failed_tests) / (len(failed_tests) + len(passed_tests))
    current_results = run_n_tests(i, program, n, oracle_opt, test_sample_size,
                                  "threads_" + str(i), 1, test_gen1)
    current_results["pattern"] = i
    current_results["fail_prob"] = fail_prob
    current_results["test_sample_size"] = test_sample_size
    results[oracle_opt] = results[oracle_opt].append(current_results, ignore_index=True)
    i = "B"
    # M = load_automaton_from_file("data/threads_combined/M" + str(i) + ".dot", automaton_type='dfa')
    # B = GeneratorBasedDFA(program)
    # failed_tests, passed_tests = generate_tests(M, B, 100, 0.2, method=test_gen2)
    # fail_prob = len(failed_tests) / (len(failed_tests) + len(passed_tests))
    # current_results = run_n_tests(i, program, n, oracle_opt, test_sample_size,
    #                               "threads_" + str(i), 1, test_gen2)
    # current_results["pattern"] = i
    # current_results["fail_prob"] = fail_prob
    # current_results["test_sample_size"] = test_sample_size
    # results[oracle_opt] = results[oracle_opt].append(current_results, ignore_index=True)
    results[oracle_opt].to_csv("output/" + "threads" + "_" + oracle_opt + ".csv", index=False)
