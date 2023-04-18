from aalpy.utils import load_automaton_from_file, save_automaton_to_file, make_input_complete
from utils import get_intersection_dfa, get_union_dfa

def magento_multiple_products(path, new_path, n):
    A = load_automaton_from_file(path, automaton_type='dfa')
    for s in A.states:
        if "A0" in s.transitions:
            s2 = s.transitions.pop("A0")
            for j in range(n):
                s.transitions["A0" + str(j)] = s2
    save_automaton_to_file(A, new_path)


def add_session_id(A, n):
    for s in A.states:
        l = list(s.transitions.keys())
        for a in l:
            s2 = s.transitions.pop(a)
            a = a[:1] + str(n) + a[2:]
            s.transitions[a] = s2
    return A

def sync_alphabets(A, B):
    alphabet_a = A.get_input_alphabet()
    alphabet_b = B.get_input_alphabet()
    for a in alphabet_a:
        B.initial_state.transitions[a] = B.initial_state
    for a in alphabet_b:
        A.initial_state.transitions[a] = A.initial_state
    make_input_complete(A, 'self_loop')
    make_input_complete(B, 'self_loop')
    return A, B

def magento_multiple_sessions(path, new_path, n):
    A = load_automaton_from_file(path, automaton_type='dfa')
    make_input_complete(A, 'sink_state')
    for i in range(1, n):
        B = load_automaton_from_file(path, automaton_type='dfa')
        make_input_complete(B, 'sink_state')
        B = add_session_id(B, i)
        A, B = sync_alphabets(A, B)
        A = get_intersection_dfa(A, B)
    save_automaton_to_file(A, new_path)


def magento_b1_multiple_sessions(path, new_path, n):
    A = load_automaton_from_file(path, automaton_type='dfa')
    for i in range(1, n):
        for s in A.states:
            l = list(s.transitions.keys())
            for a in l:
                new_a = a[:1] + str(i) + a[2:]
                s.transitions[new_a] = s.transitions[a]
    save_automaton_to_file(A, new_path)

def magento_b2_multiple_sessions(path, new_path, n):
    automata_list = []
    for i in range(n):
        A = load_automaton_from_file(path, automaton_type='dfa')
        make_input_complete(A, 'sink_state')
        for s in A.states:
            l = list(s.transitions.keys())
            for a in l:
                s2 = s.transitions.pop(a)
                if "i" in a:
                    a = a.replace("i", str(i))
                    s.transitions[a] = s2
                elif "j" in a:
                    for j in range(n):
                        if j != i:
                            a = a.replace("j", str(j))
                            s.transitions[a] = s2
        automata_list.append(A)
    A = automata_list[0]
    for i in range(1, n):
        B = automata_list[i]
        A, B = sync_alphabets(A, B)
        A = get_union_dfa(A, B)
    save_automaton_to_file(A, new_path)





# for i in range(4):
#     magento_multiple_products(
#         "data/our_models/magento_m.dot",
#         "data/our_models/magento_" + str(i+1) + "_m",
#         i+1
#     )
# for i in range(1, 5):
#     for j in range(1, 5):
#         magento_multiple_sessions(
#             "data/our_models/magento_" + str(i) + "_m.dot",
#             "data/our_models/magento_" + str(j) + "_" + str(i) + "_m",
#             j
#         )

# for i in range(4):
#     magento_multiple_products(
#         "data/our_models/magento_b1.dot",
#         "data/our_models/magento_" + str(i+1) + "_b1",
#         i+1
#     )
# for i in range(1, 5):
#     for j in range(1, 5):
#         magento_b1_multiple_sessions(
#             "data/our_models/magento_" + str(i) + "_b1.dot",
#             "data/our_models/magento_" + str(j) + "_" + str(i) + "_b1",
#             j
#         )

for i in range(1, 4):
    magento_b2_multiple_sessions(
        "data/our_models/magento_b2.dot",
        "data/our_models/magento_" + str(i+1) + "_b2",
        i+1
    )
