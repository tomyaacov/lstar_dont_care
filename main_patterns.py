from rc_lstar import *
from generator_based_dfa import *
from aalpy.utils import load_automaton_from_file


def run_n_tests(p, bug, n, oracle_opt, test_set_size, name, dfa_generator_opt):
    c = Counter()

    for i in range(n):
        if isinstance(bug, str):
            B = load_automaton_from_file(bug, automaton_type='dfa')
            make_input_complete(B, missing_transition_go_to="sink_state")
        else:
            B = GeneratorBasedDFA(bug)

        c.update(run_single_test(load_automaton_from_file("data/patterns_combined/" + str(p) + "_all_except_m.dot", automaton_type='dfa'),
                                 B,
                                 oracle_opt,
                                 test_set_size,
                                 name,
                                 dfa_generator_opt))
    c = {k: v / n for k, v in c.items()}
    return c


results = {}
test_sample_size = 10
n = 1
oracles = ["RandomWalkEqOracle"]#["SampleBasedRCOracle", "RandomWalkEqOracle", "RandomWMethodEqOracle"]
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
    for i in range(1, 7):
        M = load_automaton_from_file("data/patterns_combined/" + str(i) + "_all_except_m.dot", automaton_type='dfa')
        B = load_automaton_from_file("data/patterns_combined/" + str(i) + "_all_except_m_b.dot", automaton_type='dfa')
        make_input_complete(B, missing_transition_go_to="sink_state")
        failed_tests, passed_tests = generate_tests(M, B, 100, 0.2)
        fail_prob = len(failed_tests) / (len(failed_tests) + len(passed_tests))
        current_results = run_n_tests(i, "data/patterns/" + str(i) + ".dot", n, oracle_opt, test_sample_size,
                                      "pattern_" + str(i), 1)
        current_results["pattern"] = i
        current_results["fail_prob"] = fail_prob
        current_results["test_sample_size"] = test_sample_size
        results[oracle_opt] = results[oracle_opt].append(current_results, ignore_index=True)
    results[oracle_opt].to_csv("output/" + "patterns" + "_" + oracle_opt + ".csv", index=False)
