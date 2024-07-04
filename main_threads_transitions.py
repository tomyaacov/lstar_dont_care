from generator_based_dfa import GeneratorBasedDFA
from rc_lstar import *
from aalpy.utils import load_automaton_from_file
from random import shuffle, sample
from threads_bug_finding2 import program_transitions

def run_n_tests(p, bug, n, oracle_opt, test_set_size, name, dfa_generator_opt, test_generator_opt="random_walk"):
    c = Counter()

    for i in range(n):
        if isinstance(bug, str):
            B = load_automaton_from_file(bug, automaton_type='dfa')
            make_input_complete(B, missing_transition_go_to="sink_state")
        else:
            B = GeneratorBasedDFA(bug)

        c.update(run_single_test(load_automaton_from_file("data/threads_transitions/M" + str(p) + "_2.dot", automaton_type='dfa'),
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
        final_word = [val for pair in zip([x+"A" for x in word], [x+"B" for x in word]) for val in pair]
        if B.execute_sequence(B.initial_state, final_word)[-1]:
            failed_tests.add(tuple(final_word))
        else:
            passed_tests.add(tuple(final_word))
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
    M = load_automaton_from_file("data/threads_transitions/M" + str(i) + "_2.dot", automaton_type='dfa')
    B = load_automaton_from_file("data/threads_transitions/B" + str(i) + ".dot", automaton_type='dfa')
    make_input_complete(B, missing_transition_go_to="sink_state")
    failed_tests, passed_tests = generate_tests(M, B, 100, 0.2, method=test_gen1)
    fail_prob = len(failed_tests) / (len(failed_tests) + len(passed_tests))
    current_results = run_n_tests(i, program_transitions, n, oracle_opt, test_sample_size,
                                  "threads_transitions_" + str(i), 1, test_gen1)
    current_results["pattern"] = i
    current_results["fail_prob"] = fail_prob
    current_results["test_sample_size"] = test_sample_size
    results[oracle_opt] = results[oracle_opt].append(current_results, ignore_index=True)
    results[oracle_opt].to_csv("output/" + "threads_transitions" + "_" + oracle_opt + ".csv", index=False)
