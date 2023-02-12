from aalpy.oracles import RandomWMethodEqOracle, BreadthFirstExplorationEqOracle

from bfe_oracle import BFEOracle
from dc_lstar import run_Lstar
from aalpy.base import SUL
from aalpy.utils import visualize_automaton
# class FaultInjectedCoffeeMachineSUL(SUL):
#     def __init__(self):
#         super().__init__()
#         self.coffee_machine = DeterministicFaultInjectedCoffeeMachine()
#
#     def pre(self):
#         self.coffee_machine.counter = 0
#         self.coffee_machine.fault = None
#
#     def post(self):
#         pass
#
#     def step(self, letter):
#         if letter == 'coin':
#             return self.coffee_machine.add_coin()
#         elif letter == 'button':
#             return self.coffee_machine.button()
#         else:
#             return self.coffee_machine.inject_fault(letter)
# class DeterministicFaultInjectedCoffeeMachine:
#     def __init__(self):
#         self.counter = 0
#         self.fault = None
#         self.possible_faults = ['coin_double_value', 'button_no_effect']
#
#     def inject_fault(self, fault):
#         assert fault in self.possible_faults
#         if self.fault:
#             return 'False'
#         else:
#             self.fault = fault
#             return 'True'
#
#     def add_coin(self):
#         if self.counter == 3:
#             return 'CoinsFull'
#         if self.fault == 'coin_double_value':
#             self.counter = min(self.counter + 2, 3)
#         else:
#             self.counter = min(self.counter + 1, 3)
#         return 'CoinAdded'
#
#     def button(self):
#         if self.fault == 'button_no_effect':
#             return 'NoAction'
#         if self.counter >= 2:
#             self.counter -= 2
#             return 'Coffee'
#         else:
#             return 'NoAction'
# def learn_coffee_machine_mbd(visualize=False):
#     sul = FaultInjectedCoffeeMachineSUL()
#     alphabet = ['coin', 'button', 'coin_double_value', 'button_no_effect']
#
#     eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=5000, walk_len=20)
#
#     learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='mealy', cache_and_non_det_check=False)
#
#     if visualize:
#         visualize_automaton(learned_model, display_same_state_trans=True)
#
#     return learned_model

class DeterministicCoffeeMachineDFA:
    def __init__(self):
        self.counter = 0
        self.correct_counter = 0

    def add_coin(self):
        if self.counter == 3:
            return False
        self.counter = min(self.counter + 1, 3)
        self.correct_counter = min(self.correct_counter + 1, 3)
        return False

    def button(self):
        # property_violation = self.counter >= 2 and self.correct_counter < 2
        # if self.counter == 3:
        #     self.counter -= 1
        #     self.correct_counter = max(self.correct_counter - 2, 0)
        # elif self.correct_counter == 2:
        #     self.counter -= 2
        #     self.correct_counter = max(self.correct_counter - 2, 0)
        # return property_violation
        property_violation = self.counter >= 2 and self.correct_counter < 2
        if self.counter == 3:
            self.counter -= 1
            self.correct_counter = max(self.correct_counter - 2, 0)
        elif self.counter == 2:
            self.counter -= 2
            self.correct_counter = max(self.correct_counter - 2, 0)
        return property_violation


class FaultyCoffeeMachineSULDFA(SUL):
    def __init__(self):
        super().__init__()
        self.coffee_machine = DeterministicCoffeeMachineDFA()

    def pre(self):
        self.coffee_machine.counter = 0
        self.coffee_machine.correct_counter = 0

    def post(self):
        pass

    def step(self, letter):
        if letter == 'coin':
            return self.coffee_machine.add_coin()
        else:
            return self.coffee_machine.button()

    # def query(self, word: tuple):
    #     self.pre()
    #     l = []
    #     for letter in word:
    #         l.append(self.step(letter))
    #     self.post()
    #     return l



def learn_language_of_coffee_machine_error(visualize=False):
    sul = FaultyCoffeeMachineSULDFA()
    alphabet = ['coin', 'button']
    #sul.query(['coin', 'coin', 'coin', 'button', 'button', 'coin'])

    #eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=5000, walk_len=8)
    eq_oracle = BFEOracle(alphabet, sul, depth=8)

    learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='dfa', cache_and_non_det_check=True)

    if visualize:
        visualize_automaton(learned_model, display_same_state_trans=True)

    return learned_model



learn_language_of_coffee_machine_error(visualize=True)