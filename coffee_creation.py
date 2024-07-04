from aalpy.automata.Dfa import Dfa, DfaState
from aalpy.utils import load_automaton_from_file, save_automaton_to_file

MAX_COINS = 3
DRINK_PRICE = 2

initial_state = {"coins": 0, "button": False, "assertion": False}


def next_state(s, a):
    if a == "C":
        if s["coins"] <= MAX_COINS and (not s["button"]):
            return [{"coins": s["coins"] + 1, "button": s["button"], "assertion": False}]
    if a == "B":
        if not s["button"]:
            return [{"coins": s["coins"], "button": True, "assertion": False}]
    if a == "D":
        if s["coins"] >= DRINK_PRICE and s["button"]:  # and (not s["assertion"]):
            return [{"coins": s["coins"] - DRINK_PRICE, "button": False, "assertion": True}]
    if a == "N":
        if s["coins"] < DRINK_PRICE and s["button"]:  # and (not s["assertion"]):
            return [{"coins": s["coins"], "button": False, "assertion": True}]
    return []


def state_name(s):
    return str(s["coins"]) + "_" + str(int(s["button"])) + "_" + str(int(s["assertion"]))


def get_dfa(s, dfa_states):
    s1 = DfaState(state_name(s), is_accepting=s["assertion"])
    dfa_states.append(s1)
    for a in ["C", "B", "D", "N"]:
        for n in next_state(s, a):
            s_new = DfaState(state_name(n), is_accepting=n["assertion"])
            s1.transitions[a] = s_new
            if s_new.state_id not in [x.state_id for x in dfa_states]:
                get_dfa(n, dfa_states)


l = []
get_dfa(initial_state, l)
dfa = Dfa(l[0], l)
save_automaton_to_file(dfa, "data/coffee_new/M_new.dot")

# bug dfa

initial_state = {"coins": 0, "_coins": 0, "button": False, "assertion": False, "consecutive": 0, "reached_bug": False}


# continue - create a bug dfa with additional flag of consecutive coins
def next_state(s, a):
    if a == "C":
        if s["coins"] <= MAX_COINS and (not s["button"]):
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
            return [{"coins": s["coins"] - DRINK_PRICE, "_coins": s["_coins"] - DRINK_PRICE, "button": False,
                     "assertion": True, "consecutive": 0, "reached_bug": s["reached_bug"] or s["_coins"] < DRINK_PRICE}]
    if a == "N":
        if s["coins"] < DRINK_PRICE and s["button"]:  # and (not s["assertion"]):
            return [{"coins": s["coins"], "_coins": s["_coins"], "button": False, "assertion": True,
                     "consecutive": 0, "reached_bug": s["reached_bug"] or s["_coins"] >= DRINK_PRICE}]
    return []


def state_name(s):
    return str(s["coins"]) + "_" + str(int(s["button"])) + "_" + str(int(s["assertion"])) + "_" + str(
        s["consecutive"]) + "_" + str(int(s["reached_bug"]))

def get_dfa(s, dfa_states):
    s1 = DfaState(state_name(s), is_accepting=s["reached_bug"])
    dfa_states.append(s1)
    for a in ["C", "B", "D", "N"]:
        for n in next_state(s, a):
            s_new = DfaState(state_name(n), is_accepting=s["reached_bug"])
            s1.transitions[a] = s_new
            if s_new.state_id not in [x.state_id for x in dfa_states]:
                get_dfa(n, dfa_states)


l = []
get_dfa(initial_state, l)
dfa = Dfa(l[0], l)
save_automaton_to_file(dfa, "data/coffee_new/B_new.dot")
