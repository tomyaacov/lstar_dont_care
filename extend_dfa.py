from aalpy.utils import load_automaton_from_file, save_automaton_to_file, make_input_complete
from utils import get_intersection_dfa, get_union_dfa, get_sim_diff_dfa, load_automaton


def magento_multiple_products(path, new_path, n):
    A = load_automaton_from_file(path, automaton_type='dfa')
    for s in A.states:
        l = list(s.transitions.keys())
        for a in l:
            if a.startswith("A"):
                s2 = s.transitions.pop(a)
                for j in range(n):
                    s.transitions[a[:-1] + str(j)] = s2
    save_automaton_to_file(A, new_path)


def add_session_id(A, n):
    for s in A.states:
        l = list(s.transitions.keys())
        for a in l:
            if "i" not in a:
                continue
            s2 = s.transitions.pop(a)
            a = a.replace("i", str(n))
            s.transitions[a] = s2
    return A

def add_session_ids(A, n):
    for s in A.states:
        l = list(s.transitions.keys())
        for a in l:
            if "i" not in a:
                continue
            s2 = s.transitions.pop(a)
            for i in range(n):
                new_a = a.replace("i", str(i))
                s.transitions[new_a] = s2
    return A

def add_product_ids(A, n):
    for s in A.states:
        l = list(s.transitions.keys())
        for a in l:
            if "j" not in a:
                continue
            s2 = s.transitions.pop(a)
            for j in range(n):
                new_a = a.replace("j", str(j))
                s.transitions[new_a] = s2
    return A

def sync_alphabets(A, B):
    alphabet_a = set(A.get_input_alphabet())
    alphabet_b = set(B.get_input_alphabet())
    alphabet_a = alphabet_a - alphabet_b
    alphabet_b = alphabet_b - alphabet_a
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

# n=2
# A = load_automaton_from_file("data/our_models/magento_m_checkout.dot", automaton_type='dfa')
# make_input_complete(A, 'sink_state')
# for i in range(1, n):
#     B = load_automaton_from_file("data/our_models/magento_m_session.dot", automaton_type='dfa')
#     make_input_complete(B, 'sink_state')
#     B = add_session_id(B, i)
#     A = add_session_id(A, i)
#     A, B = sync_alphabets(A, B)
#     A = get_intersection_dfa(A, B)
# save_automaton_to_file(A, "data/our_models/test")

def remove_sink_state(A):
    sink = None
    for s in A.states:
        if s.is_accepting:
            continue
        is_sink = True
        for a in s.transitions:
            if s.transitions[a] != s:
                is_sink = False
                break
        if is_sink:
            sink = s
            break
    if sink is not None:
        A.states.remove(sink)
        for s in A.states:
            l = list(s.transitions.keys())
            for a in l:
                if s.transitions[a] == sink:
                    s.transitions.pop(a)
    return A


def magento_extend(session_num, products_num, output_path):
    A = load_automaton_from_file("data/our_models/magento_m_checkout.dot", automaton_type='dfa')
    make_input_complete(A, 'sink_state')
    A = add_session_ids(A, session_num)
    for i in range(session_num):
        B = load_automaton_from_file("data/our_models/magento_m_session.dot", automaton_type='dfa')
        make_input_complete(B, 'sink_state')
        B = add_session_id(B, i)
        A, B = sync_alphabets(A, B)
        A = get_intersection_dfa(A, B)
    A = add_product_ids(A, products_num)
    #A = remove_sink_state(A)
    save_automaton_to_file(A, output_path)
# magento_extend(2, 1, "data/our_models/test")
#
# B = load_automaton_from_file("data/our_models/magento_m_2_1.dot", automaton_type='dfa')
# make_input_complete(B, 'sink_state')
# print(get_sim_diff_dfa(load_automaton_from_file("data/our_models/test.dot", automaton_type='dfa'), B))

for i in range(1, 5):
    for j in range(1, 5):
        B = load_automaton(f"data/our_models/magento_m_{i}_{j}.dot", automaton_type='dfa')

# for i in range(2, 5):
#     magento_multiple_products(
#         "data/our_models/magento_m_1_1.dot",
#         f"data/our_models/magento_m_{1}_{i}",
#         i
#     )

# for i in range(1, 4):
#     for j in range(2, 5):
#         magento_multiple_products(
#             f"data/our_models/magento_m_{i}_{1}.dot",
#             f"data/our_models/magento_m_{i}_{j}",
#             j
#         )


# for i in range(2, 3):
#     for j in range(1, 2):
#         magento_multiple_sessions(
#             f"data/our_models/magento_m_{1}_{j}.dot",
#             f"data/our_models/magento_m_{i}_{j}",
#             i
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

# for i in range(1, 4):
#     magento_b2_multiple_sessions(
#         "data/our_models/magento_b2.dot",
#         "data/our_models/magento_" + str(i+1) + "_b2",
#         i+1
#     )
