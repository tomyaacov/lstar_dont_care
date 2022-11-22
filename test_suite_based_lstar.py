from aalpy.learning_algs import run_Lstar
from test_oracle import TestOracle
from test_sul import TestSUL
from dc_dfa import find_minimal_consistent_dfa


def run_test_lstar(alphabet: list, sul: TestSUL, oracle: TestOracle):
    dfa3 = run_Lstar(alphabet, sul, oracle, cex_processing='rs', closing_strategy='single', automaton_type='moore', cache_and_non_det_check=False)
    save_automaton_to_file(dfa3, path="magento_dfa3")
    return find_minimal_consistent_dfa(dfa3)



if __name__ == "__main__":
    from aalpy.utils import save_automaton_to_file
    from aalpy.learning_algs import run_RPNI
    from itertools import product
    total_traces = [
            (tuple(), True),
            (("L2", "L1", "A", "A", "A", "C"), True),
            (("L2",), True),
            (("L2", "L1"), True),
            (("L2", "L1", "A"), True),
            (("L2", "L1", "A", "A"), True),
            (("L2", "L1", "A", "A", "A"), True),
            (("L1", "L2", "A", "A", "A", "C"), True),
            (("L1",), True),
            (("L1", "L2"), True),
            (("L1", "L2", "A"), True),
            (("L1", "L2", "A", "A"), True),
            (("L1", "L2", "A", "A", "A"), True),
            (("L1", "A", "L2", "A", "A", "C"), False),
            (("L1", "A"), True),
            (("L1", "A", "L2"), False),
            (("L1", "A", "L2", "A"), False),
            (("L1", "A", "L2", "A", "A"), False),
            (("L1", "A", "A", "L2", "A", "C"), False),
            (("L1", "A", "A"), True),
            (("L1", "A", "A", "L2"), False),
            (("L1", "A", "A", "L2", "A"), False),
            (("L1", "A", "A", "A", "L2", "C"), False),
            (("L1", "A", "A", "A"), True),
            (("L1", "A", "A", "A", "L2"), False),
    ]
    alphabet = ["L1", "L2", "A", "C"]
    spec_data = [(x, True) for x,_ in total_traces]
    for i in range(1, 7):
        for w in product(alphabet, repeat=i):
            if not ((w, True) in total_traces or (w, False) in total_traces):
                spec_data.append((w, False))
    spec_dfa = run_RPNI(spec_data, automaton_type="dfa")
    save_automaton_to_file(spec_dfa, path="spec_dfa")
    system_dfa = run_RPNI(total_traces, automaton_type="dfa")
    save_automaton_to_file(system_dfa, path="system_dfa")
    passed_tests = {
        ("L2", "L1", "A", "A", "A", "C"),
        ("L1", "L2", "A", "A", "A", "C"),
        ("L1", "A", "A", "A")
    }
    failed_tests = {
        ("L1", "A", "L2", "A", "A", "C"),
        ("L1", "A", "A", "L2", "A", "C"),
        ("L1", "A", "L2"),
        ("L1", "A", "L2", "A"),
        ("L1", "A", "L2", "A", "A"),
        ("L1", "A", "A", "L2", "A", "C"),
        ("L1", "A", "A", "L2"),
        ("L1", "A", "A", "L2", "A"),
        ("L1", "A", "A", "A", "L2", "C"),
        ("L1", "A", "A", "A", "L2")
    }
    sul = TestSUL(failed_tests, passed_tests, spec_dfa, system_dfa)
    oracle = TestOracle(alphabet, sul, sample_size=10, min_walk_len=1, max_sample_len=7)
    hypothesis = run_test_lstar(alphabet, sul, oracle)
    save_automaton_to_file(hypothesis, path="magento")
