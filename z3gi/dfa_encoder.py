import z3
import itertools
from z3gi.tree import Tree
from z3gi.dfa import DFA
from z3gi.mapper import Mapper


class DFAEncoder:
    def __init__(self):
        self.tree = Tree(itertools.count(0))
        self.cache = {}
        self.labels = set()

    def add(self, trace):
        seq, accept = trace
        node = self.tree[seq]
        self.cache[node] = accept
        self.labels.update(seq)

    def build(self, num_states, num_transitions_first, num_transitions_second):
        dfa = DFA(list(self.labels), num_states)
        mapper = Mapper(dfa)
        constraints = self.axioms(dfa, mapper)
        constraints += self.node_constraints(dfa, mapper)
        constraints += self.transition_constraints(dfa, mapper)
        # constraints += self.suffix_closed_constraints(dfa, mapper)
        # constraints += self.rejecting_sink_constraints(dfa, mapper)
        # constraints += self.first_transition_constraints(dfa, mapper, num_transitions_first)
        # constraints += self.second_transition_constraints(dfa, mapper, num_transitions_second)
        return dfa, constraints

    def axioms(self, dfa, mapper):
        return [
            z3.And([z3.And([z3.Or([dfa.transition(state, label) == to_state
                                   for to_state in dfa.states]) for state in dfa.states])
                    for label in dfa.labels.values()]),
            z3.Distinct(list(dfa.labels.values())),
            z3.Distinct(list(dfa.states)),
            z3.Distinct([mapper.element(node.id) for node in self.cache]),
        #    z3.And([z3.Or([mapper.map(mapper.element(node.id)) == q for node in self.cache]) for q in dfa.states])
        ]

    def node_constraints(self, dfa, mapper):
        constraints = []
        for node in self.cache:
            accept = self.cache[node]
            n = mapper.element(node.id)
            constraints.append(dfa.output(mapper.map(n)) == accept)
        return constraints

    def transition_constraints(self, dfa, mapper):
        constraints = [dfa.start == mapper.map(mapper.start)]
        for node, label, child in self.tree.transitions():
            n = mapper.element(node.id)
            l = dfa.labels[label]
            c = mapper.element(child.id)
            constraints.append(dfa.transition(mapper.map(n), l) == mapper.map(c))
        #print(len(constraints))
        #print(constraints[1])
        return constraints

    def suffix_closed_constraints(self, dfa, mapper):
        return [z3.And([z3.And([z3.Implies(dfa.output(state), dfa.output(dfa.transition(state, label))) for state in dfa.states]) for label in dfa.labels.values()])]

    def rejecting_sink_constraints(self, dfa, mapper):
        return [z3.And([z3.Not(dfa.output(dfa.states[-1]))] + [dfa.transition(dfa.states[-1], label) == dfa.states[-1] for label in dfa.labels.values()])]

    def first_transition_constraints(self, dfa, mapper, num_transitions):
        return [z3.Sum([z3.If(dfa.transition(state, label) == dfa.states[-1], 0, 1) for state in dfa.states for label in dfa.labels.values()]) <= num_transitions]

    def second_transition_constraints(self, dfa, mapper, num_transitions):
        return [z3.Sum([z3.If(dfa.transition(state, label) == state, 0, 1) for state in dfa.states for label in dfa.labels.values()]) <= num_transitions]
