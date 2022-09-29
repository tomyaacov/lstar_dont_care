from dc_sul import DCSUL
from aalpy.automata.Dfa import Dfa


class MagentoSUL(DCSUL):

    def __init__(self):
        super().__init__()
        magento_traces = [
            (("L2", "L1", "A", "A", "A", "C"), False),
            (("L2",), False),
            (("L2", "L1"), False),
            (("L2", "L1", "A"), False),
            (("L2", "L1", "A", "A"), False),
            (("L2", "L1", "A", "A", "A"), False),
            (("L1", "L2", "A", "A", "A", "C"), False),
            (("L1",), False),
            (("L1", "L2"), False),
            (("L1", "L2", "A"), False),
            (("L1", "L2", "A", "A"), False),
            (("L1", "L2", "A", "A", "A"), False),
            (("L1", "A", "L2", "A", "A", "C"), True),
            (("L1", "A"), False),
            (("L1", "A", "L2"), True),
            (("L1", "A", "L2", "A"), True),
            (("L1", "A", "L2", "A", "A"), True),
            (("L1", "A", "A", "L2", "A", "C"), True),
            (("L1", "A", "A"), False),
            (("L1", "A", "A", "L2"), True),
            (("L1", "A", "A", "L2", "A"), True),
            (("L1", "A", "A", "A", "L2", "C"), True),
            (("L1", "A", "A", "A"), False),
            (("L1", "A", "A", "A", "L2"), True),
        ]
        self.traces = sorted(magento_traces, key=len)  # return minimal counter example. maybe not necessary
        self.current_state = tuple()  # keeps the current trace

    def check_soundness(self, hypothesis: Dfa, alphabet=None):
        for w, l in self.traces:
            hypothesis.reset_to_initial()
            for letter in enumerate(w):
                out_hyp = hypothesis.step(letter)
            if out_hyp != l:
                return w
        return None  # sound

    def pre(self):
        self.current_state = tuple()

    def post(self):
        pass

    def step(self, letter):
        self.current_state += (letter,)
        if (self.current_state, True) in self.traces:
            return "+"
        elif (self.current_state, False) in self.traces:
            return "-"
        else:
            return "?"



