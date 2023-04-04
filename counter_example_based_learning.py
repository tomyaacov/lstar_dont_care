from aalpy.learning_algs import run_RPNI


def learn(failed_tests, passed_tests, oracle):
    data = [(x, True) for x in failed_tests] + [(x, False) for x in passed_tests]
    while True:
        hypothesis = run_RPNI(data, automaton_type="dfa")
        cte = oracle.find_cex(hypothesis)
        if cte is None:
            return hypothesis
        else:
            data.append((cte, not hypothesis.execute_sequence(hypothesis.initial_state, cte)[-1]))
