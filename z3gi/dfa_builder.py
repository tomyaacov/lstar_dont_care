
class DFABuilder():
    def __init__(self, dfa):
        super().__init__()
        self.dfa = dfa

    def build_dfa(self, m):
        tr = DFATranslator(m, self.dfa)
        mut_dfa = MutableDFA()
        for state in self.dfa.states:
            accepting = m.eval(self.dfa.output(state))
            mut_dfa.add_state(tr.z3_to_state(state), tr.z3_to_bool(accepting))
        for state in self.dfa.states:
            for labels in self.dfa.labels.values():
                to_state = m.eval(self.dfa.transition(state, labels))
                trans = Transition(
                    tr.z3_to_state(state),
                    tr.z3_to_label(labels),
                    tr.z3_to_state(to_state))
                mut_dfa.add_transition(tr.z3_to_state(state), trans)
        #mut_dfa.generate_acc_seq()
        return mut_dfa.to_immutable()


class DFATranslator(object):
    """Provides translation from z3 constants to DFA elements. It evaluates everything (s.t. variables are resolved
    to their actual values), enabling it to translate both variables and values."""
    def __init__(self, model, fa):
        self._fa = fa
        self._z3_to_label = {model.eval(fa.labels[inp]): inp for inp in fa.labels.keys()}
        self._z3_states = list(map(model.eval, fa.states))
        self._model = model

    def z3_to_bool(self, z3bool):
        return str(z3bool) == "True"

    def z3_to_state(self, z3state):
        return "q"+str(self._z3_states.index(self._model.eval(z3state)))

    def z3_to_label(self, z3label):
        return self._z3_to_label[self._model.eval(z3label)]

class Transition():
    def __init__(self, start_state, start_label, end_state):
        self.start_state = start_state
        self.start_label = start_label
        self.end_state = end_state

    def __str__(self, shortened=False):
        short = "{0} -> {1}".format(self.start_label, self.end_state)
        if not shortened:
            return "{0} {1}".format(self.start_state, short)
        else:
            return short

class MutableAcceptorMixin:
    def add_state(self, state, accepts):
        if state not in self._states:
            self._states.append(state)
        self._state_to_acc[state] = accepts

    def _remove_state(self, state):
        self._states.remove(state)
        self._state_to_trans.pop(state)

    def add_transition(self, state, transition):
        if state not in self._state_to_trans:
            self._state_to_trans[state] = []
        self._state_to_trans[state].append(transition)

    def generate_acc_seq(self, remove_unreachable=True):
        """generates access sequences for an automaton. It removes states that are not reachable."""
        new_acc_seq = get_trans_acc_seq(self, from_state=self.start_state())
        for state in self.states():
            if state not in new_acc_seq and remove_unreachable:
                self._remove_state(state)

        assert(len(new_acc_seq) == len(self.states()))
        self._acc_trans_seq = new_acc_seq

class Automaton:
    def __init__(self, states, state_to_trans, acc_trans_seq={}):
        super().__init__()
        self._states = states
        self._state_to_trans = state_to_trans
        self._acc_trans_seq = acc_trans_seq

    def start_state(self):
        return self._states[0]

    def acc_trans_seq(self, state=None):
        """returns the access sequence to a state in the form of transitions"""
        if state is not None:
            return list(self._acc_trans_seq[state])
        else:
            return dict(self._acc_trans_seq)

    def acc_seq(self, state=None):
        """returns the access sequence to a state in the form of sequences of inputs"""
        if state is not None:
            if len(self._acc_trans_seq) == 0:
                raise Exception("Access sequences haven't been defined for this machine")
            return self.trans_to_inputs(self._acc_trans_seq[state])
        else:
            return {state:self.trans_to_inputs(self._acc_trans_seq[state]) for state in self.states()}

    def states(self):
        return list(self._states)

    def transitions(self, state, label=None):
        if label is None:
            return list(self._state_to_trans[state])
        else:
            return list([trans for trans in self._state_to_trans[state] if trans.start_label == label])

    def state(self, trace):
        """state function which also provides a basic implementation"""
        crt_state = self.start_state()
        for symbol in trace:
            transitions = self.transitions(crt_state, symbol)
            fired_transitions = [trans for trans in transitions if trans.start_label == symbol]

            # the number of fired transitions can be more than one since we could have multiple equalities
            if len(fired_transitions) == 0:
                raise Exception

            if len(fired_transitions) > 1:
                raise Exception

            fired_transition = fired_transitions[0]
            crt_state = fired_transition.end_state

        return crt_state


    def trans_to_inputs(self, transitions):
        """returns a unique sequence of inputs generated by execution traversing these transitions"""
        pass


    def inputs_to_trans(self, seq):
        """returns a unique sequence of transitions generated by execution of these inputs"""
        pass

    def input_labels(self):
        return set([trans.start_label for trans in self.transitions(self.start_state())])


    def output(self, trace):
        pass

    # Basic __str__ function which works for most FSMs.
    def __str__(self):
        str_rep = ""
        for (st, acc_seq) in self._acc_trans_seq.items():
            str_rep += "acc_seq("+ str(st) +") = " + " , ".join(list(map(str,acc_seq))) + "\n"
        for state in self.states():
            str_rep += str(state) + "\n"
            for tran in self.transitions(state):
                str_rep += "\t" + tran.__str__(shortened=True) + "\n"

        return str_rep
class NavigatorMixin(Automaton):
    def trans_to_inputs(self, transitions):
        return [trans.start_label for trans in transitions]

    def inputs_to_trans(self, seq):
        trans = []
        state = self.start_state()
        for inp in seq:
            next_trans = self.transitions(state, inp)
            trans.append(next_trans[0])
            state = next_trans[0].end_state
        return trans
class Acceptor(Automaton):
    def __init__(self, states, state_to_trans, state_to_acc, acc_trans_seq={}):
        super().__init__(states, state_to_trans, acc_trans_seq)
        self._state_to_acc = state_to_acc

    def is_accepting(self, state):
        return self._state_to_acc[state]

    def accepts(self, trace):
        state = self.state(trace)
        is_acc = self.is_accepting(state)
        return is_acc

    def output(self, trace):
        self.accepts(trace)

    def __str__(self):
        return str(self._state_to_acc) + "\n" + super().__str__()

class DFA(Acceptor, NavigatorMixin):
    def __init__(self, states, state_to_trans, state_to_acc, acc_trans_seq={}):
        super().__init__(states, state_to_trans, state_to_acc, acc_trans_seq)

    def transitions(self, state, label=None):
        return super().transitions(state, label)

    def state(self, trace):
        crt_state = super().state(trace)
        return crt_state

class MutableDFA(DFA, MutableAcceptorMixin, NavigatorMixin):
    def __init__(self):
        super().__init__([], {}, {})

    def _runner(self):
        return None

    def to_immutable(self) -> DFA:
        return DFA(self._states, self._state_to_trans, self._state_to_acc, self.acc_trans_seq())



def get_trans_acc_seq(aut, from_state=None):
    """Generates transition access sequences for a given automaton"""
    ptree = get_prefix_tree(aut, from_state=from_state)
    acc_seq = dict()
    states = list(aut.states())
    for state in states:
        pred = lambda x: (x.state == state)
        node = ptree.find_node(pred)
        if node is None:
            print("Could not find state {0} in tree {1} \n for model \n {2}".format(state, ptree, aut))
            continue
            # print("Could not find state {0} in tree {1} \n for model \n {2}".format(state, ptree, self))
            # raise InvalidAutomaton
        acc_seq[state] = node.path()
    return acc_seq

def get_prefix_tree(aut, from_state=None):
    """Generates a transition prefix tree for a given automaton"""
    visited  = set()
    to_visit = set()
    if from_state is None:
        from_state = aut.start_state()
    root = PrefixTree(from_state)
    to_visit.add(root)
    while len(to_visit) > 0:
        crt_node = to_visit.pop()
        visited.add(crt_node.state)
        transitions = aut.transitions(crt_node.state)
        for trans in transitions:
            if trans.end_state not in visited:
                child_node = PrefixTree(trans.end_state)
                crt_node.add_child(trans, child_node)
                to_visit.add(child_node)
    return root

class PrefixTree():
    def __init__(self, state):
        self.state = state
        self.tr_tree:dict = {}
        self.parent:PrefixTree = None

    def add_child(self, trans, tree):
        self.tr_tree[trans] = tree
        self.tr_tree[trans].parent = self

    def path(self):
        if self.parent is None:
            return []
        else:
            for (tr, node) in self.parent.tr_tree.items():
                if node is self:
                    return self.parent.path()+[tr]
            raise Exception("Miscontructed tree")

    def find_node(self, predicate):
        if predicate(self):
            return self
        elif len(self.tr_tree) == 0:
            return None
        else:
            for (tran, child) in self.tr_tree.items():
                node = child.find_node(predicate)
                if node is not None:
                    return node
            return None

    def __str__(self, tabs=0):
        space = "".join(["\t" for _ in range(0, tabs)])
        tree = "(n_{0}".format(self.state)
        for (tr, node) in self.tr_tree.items():
            tree += "\n" + space + " {0} -> {1}".format(tr, node.__str__(tabs=tabs + 1))
        tree += ")"
        return tree