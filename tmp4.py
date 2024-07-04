
class DFAEncoder(Encoder):
    def __init__(self):
        self.tree = Tree(itertools.count(0))
        self.cache = {}
        self.labels = set()

    def add(self, trace):
        seq, accept = trace
        node = self.tree[seq]
        self.cache[node] = accept
        self.labels.update(seq)

    def build(self, num_states):
        dfa = DFA(list(self.labels), num_states)
        mapper = Mapper(dfa)
        constraints = self.axioms(dfa, mapper)
        constraints += self.node_constraints(dfa, mapper)
        constraints += self.transition_constraints(dfa, mapper)
        return dfa, constraints

    def axioms(self, dfa: DFA, mapper: Mapper):
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
        return constraints

traces = [
    (["a", "b"], True),
    (["a", "b", "a", "b"], True),
    (["a"], False),
    (["b"], False),
    (["a", "b", "a"], False),
    (["a", "a"], False),
    (["a", "b", "b"], False),
    (["a", "b", "a", "a"], False)
]
