from aalpy.automata import DfaState, Dfa


class GeneratorBasedDFA(Dfa):
    def __init__(self, generator):
        self.generator = generator
        self.current = self.generator()
        initial_state = DfaState(0)
        super().__init__(initial_state, [initial_state])

    def step(self, letter):
        return self.current.send(letter)

    def reset_to_initial(self):
        self.current = self.generator()
        self.current.send(None)

    def execute_sequence(self, origin_state, seq):
        # ignore origin state and execute sequence from the beginning
        self.reset_to_initial()
        labels = []
        for letter in seq:
            labels.append(self.step(letter))
        self.reset_to_initial()
        return labels






