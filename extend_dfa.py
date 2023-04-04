from aalpy.utils import load_automaton_from_file, save_automaton_to_file


def magento_multiple_products(path, new_path, n):
    A = load_automaton_from_file(path, automaton_type='dfa')
    for s in A.states:
        if "A" in s.transitions:
            s2 = s.transitions.pop("A")
            for j in range(n):
                s.transitions["A" + str(j)] = s2
    save_automaton_to_file(A, new_path)


for i in range(1, 5):
    magento_multiple_products(
        "data/our_models/magento_m.dot",
        "data/our_models/magento_" + str(i) + "_m",
        i
    )
    magento_multiple_products(
        "data/our_models/magento_b.dot",
        "data/our_models/magento_" + str(i) + "_b",
        i
    )


