from aalpy.learning_algs.deterministic.ObservationTable import ObservationTable
from magento_sul import DCSUL
from tabulate import tabulate


class DCObservationTable(ObservationTable):
    def __init__(self, alphabet: list, sul: DCSUL):
        super().__init__(alphabet, sul, "moore")
        self.alphabet = alphabet

    def __str__(self):
        return tabulate([["".join(x)] + list(self.T.get(x)) for x in self.S], headers=["prefix"] + list(["".join(x) for x in self.E]))
