from aalpy.base import SUL


class CompleteDCSUL(SUL):
    def __init__(self, M, B):
        super().__init__()
        self.M = M
        self.B = B
        self.membership_queries = 0
        self.system_queries = 0

    def query(self, word: tuple) -> list:
        self.M.reset_to_initial()
        self.B.reset_to_initial()
        m_labels = []
        b_labels = []
        if len(word) == 0:
            m_labels.append(self.M.initial_state.is_accepting)
            b_labels.append(self.B.initial_state.is_accepting)
        else:
            for letter in word:
                m_labels.append(self.M.step(letter))
                b_labels.append(self.B.step(letter))
        self.M.reset_to_initial()
        self.B.reset_to_initial()
        b_labels = ["+" if x else "-" for x in b_labels]
        final = [in_b if in_m else "?" for in_m, in_b in zip(m_labels, b_labels)]
        self.membership_queries += 1
        if final[-1] != "?":
            self.system_queries += 1
        return final

    def pre(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError

    def step(self, letter):
        raise NotImplementedError