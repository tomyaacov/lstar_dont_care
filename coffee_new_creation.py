from aalpy.automata.Dfa import Dfa, DfaState
from aalpy.utils import load_automaton_from_file, save_automaton_to_file, make_input_complete

MAX_COINS = 3
DRINK_PRICE = 2


# bug dfa

initial_state = {"coins": 0, "_coins": 0, "button": False, "assertion": False, "consecutive": 0, "reached_bug": False}


# continue - create a bug dfa with additional flag of consecutive coins
def next_state(s, a):
    if a == "C":
        if s["coins"] < MAX_COINS and (not s["button"]):
            if s["consecutive"] == 2:
                return [{"coins": s["coins"] + 1, "_coins": s["_coins"], "button": s["button"], "assertion": False,
                         "consecutive": s["consecutive"] + 1,
                         "reached_bug": s["reached_bug"]}]
            else:
                return [{"coins": s["coins"] + 1, "_coins": s["_coins"] + 1, "button": s["button"], "assertion": False,
                         "consecutive": s["consecutive"] + 1,
                         "reached_bug": s["reached_bug"]}]
    if a == "B":
        if not s["button"]:
            return [{"coins": s["coins"], "_coins": s["_coins"], "button": True, "assertion": False, "consecutive": 0, "reached_bug": s["reached_bug"]}]
    if a == "D":
        if s["coins"] >= DRINK_PRICE and s["button"]:  # and (not s["assertion"]):
            return [{"coins": s["coins"] - DRINK_PRICE, "_coins": max(s["_coins"] - DRINK_PRICE, 0), "button": False,
                     "assertion": True, "consecutive": 0, "reached_bug": s["reached_bug"] or s["_coins"] < DRINK_PRICE}]
    if a == "N":
        if s["coins"] < DRINK_PRICE and s["button"]:  # and (not s["assertion"]):
            return [{"coins": s["coins"], "_coins": s["_coins"], "button": False, "assertion": True,
                     "consecutive": 0, "reached_bug": s["reached_bug"] or s["_coins"] >= DRINK_PRICE}]
    return []


def state_name(s):
    return str(s["coins"]) + "_" + str(s["_coins"]) + "_" + str(int(s["button"])) + "_" + str(int(s["assertion"])) + "_" + str(
        s["consecutive"]) + "_" + str(int(s["reached_bug"]))

def get_dfa(s, dfa_states, acccepting_flag_name):
    s1 = DfaState(state_name(s), is_accepting=s[acccepting_flag_name])
    dfa_states.append(s1)
    for a in ["C", "B", "D", "N"]:
        for n in next_state(s, a):
            s_new = DfaState(state_name(n), is_accepting=s[acccepting_flag_name])
            s1.transitions[a] = s_new
            if s_new.state_id not in [x.state_id for x in dfa_states]:
                get_dfa(n, dfa_states, acccepting_flag_name)

from utils import are_dfa_equivalent, aalpy_to_automata_lib_format, automata_lib_to_aalpy_format
l = []
get_dfa(initial_state, l, "assertion")
dfa = Dfa(l[0], l)
print(len(dfa.states))
save_automaton_to_file(dfa, "data/coffee_new/M.dot")
dfa = load_automaton_from_file('data/coffee_new/M.dot', automaton_type='dfa')
dfa = make_input_complete(dfa, missing_transition_go_to="sink_state")
a = aalpy_to_automata_lib_format(dfa)
a = a.minify()
dfa = automata_lib_to_aalpy_format(a)
save_automaton_to_file(dfa, "data/coffee_new/M.dot")
dfa = load_automaton_from_file('data/coffee_new/M.dot', automaton_type='dfa')
print(len(dfa.states))

M_original = load_automaton_from_file('data/coffee/M.dot', automaton_type='dfa')
print(dfa.get_input_alphabet())
print(M_original.get_input_alphabet())
print(are_dfa_equivalent(M_original, dfa))



l = []
get_dfa(initial_state, l, "reached_bug")
dfa = Dfa(l[0], l)
print(len(dfa.states))
save_automaton_to_file(dfa, "data/coffee_new/B.dot")
dfa = load_automaton_from_file('data/coffee_new/B.dot', automaton_type='dfa')
dfa = make_input_complete(dfa, missing_transition_go_to="sink_state")
a = aalpy_to_automata_lib_format(dfa)
a = a.minify()
dfa = automata_lib_to_aalpy_format(a)
save_automaton_to_file(dfa, "data/coffee_new/B.dot")
dfa = load_automaton_from_file('data/coffee_new/B.dot', automaton_type='dfa')
print(len(dfa.states))


from utils import are_dfa_equivalent
M_original = load_automaton_from_file('data/coffee/B.dot', automaton_type='dfa')
print(dfa.get_input_alphabet())
print(M_original.get_input_alphabet())
print(are_dfa_equivalent(M_original, dfa))