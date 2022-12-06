from aalpy.learning_algs import run_Lstar
from test_oracle import TestOracle
from test_sul import TestSUL
from dc_dfa import find_minimal_consistent_dfa
import random


def run_test_lstar(alphabet: list, sul: TestSUL, oracle: TestOracle):
    dfa3 = run_Lstar(alphabet, sul, oracle, cex_processing='rs', closing_strategy='single', automaton_type='moore', cache_and_non_det_check=False)
    save_automaton_to_file(dfa3, path="magento_dfa3")
    return find_minimal_consistent_dfa(dfa3)


if __name__ == "__main__":
    from aalpy.utils import save_automaton_to_file
    from aalpy.learning_algs import run_RPNI
    from itertools import product
    def passed(w):
        if "L2" in w and "A" in w and "C" in w:
            if w.index("L2") < w.index("A") < w.index("C"):
                return False
        return True
    total_traces = set()
    for n in range(1, 5):
        base = ["L1"] + ["A"]*n + ["C"]
        for i in range(-1, len(base)):
            if i == -1:
                w = base # without L2
            else:
                w = base[:i] + ["L2"] + base[i:]
            for j in range(len(w)+1):
                total_traces.add((tuple(w[:j]), passed(w[:j])))
    total_traces = list(total_traces)

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
    test_coverage = 1
    passed_tests = set([w for w, l in total_traces if l and random.random() <= test_coverage])
    failed_tests = set([w for w, l in total_traces if not l and random.random() <= test_coverage])

    sul = TestSUL(failed_tests, passed_tests, spec_dfa, system_dfa)
    oracle = TestOracle(alphabet, sul, sample_size=10, min_walk_len=1, max_sample_len=7)
    hypothesis = run_test_lstar(alphabet, sul, oracle)
    save_automaton_to_file(hypothesis, path="magento_mealy")
    for t in passed_tests:
        if len(t) == 0: continue
        output = hypothesis.execute_sequence(hypothesis.initial_state, t)
        if output[-1] != 0:
            print("not equivalent:", t)
    for t in failed_tests:
        output = hypothesis.execute_sequence(hypothesis.initial_state,t)
        if output[-1] != 1:
            print("not equivalent:", t)