from aalpy.oracles import BreadthFirstExplorationEqOracle, RandomWalkEqOracle, RandomWMethodEqOracle

from bfe_oracle import BFEOracle
from dc_lstar import run_Lstar
from aalpy.base import SUL
from aalpy.automata.Dfa import Dfa
from aalpy.automata.MealyMachine import MealyMachine
from dc_dfa import find_minimal_consistent_dfa
from aalpy.learning_algs.deterministic.ObservationTable import ObservationTable
import time
from aalpy.utils import load_automaton_from_file
from aalpy.utils import save_automaton_to_file
from aalpy.base.Oracle import Oracle
from aalpy.automata.MooreMachine import MooreMachine
from random import randint, choice
from aalpy.learning_algs import run_RPNI

example = "coffeeMachine"
#example = "gearbox"
def observation_table_to_data(observation_table: ObservationTable):
    data = []
    for prefix in observation_table.S:
        labels = observation_table.T[prefix]
        for i, label in enumerate(labels):
            if label == "?":
                continue
            data.append((prefix + observation_table.E[i], label == "+"))
    return data

def dfa3_to_data(dfa3: MooreMachine):
    from itertools import product
    data = []
    data.append((tuple(), False))  # empty word is not a bug
    for i in range(1, 8):
        for l in product(dfa3.get_input_alphabet(), repeat=i):
            result = dfa3.execute_sequence(dfa3.initial_state, l)
            if result[-1] != "?":
                data.append((l, result[-1] == "+"))
    return data



M = load_automaton_from_file('data/models/' + example + 'FaultModel.dot', automaton_type='mealy')
B = load_automaton_from_file('data/models/' + example + 'FaultLanguage.dot', automaton_type='dfa')

class TestSUL(SUL):

    def __init__(self, spec_dfa: MealyMachine, system_dfa: Dfa):
        super().__init__()
        self.spec_dfa = spec_dfa
        self.system_dfa = system_dfa
        self.num_queries = 0
        self.num_steps = 0
        self.system_queries = 0
        self.already_not_in_system = False
        self.already_failed_in_system = False
        self.prefix = []

    def query(self, word: tuple) -> list:
        if type(word) == list:
            word = tuple(word)
        self.num_queries += 1
        self.num_steps += len(word)
        if len(word) == 0:
            in_system = True
        else:
            l = [x for x in self.spec_dfa.execute_sequence(self.spec_dfa.initial_state, word)]
            l = ['NoAction' if x == 'NO_EFFECT' else x for x in l]
            in_system = 'NoAction' not in l
        if not in_system:
            return ["?"]
        self.system_queries += 1
        if len(word) == 0:
            failed_in_system = self.system_dfa.initial_state.is_accepting
        else:
            failed_in_system = any(self.system_dfa.execute_sequence(self.system_dfa.initial_state, word))
        if failed_in_system:
            return ["+"]
        else:
            return ["-"]


    def pre(self):
        self.spec_dfa.reset_to_initial()
        self.system_dfa.reset_to_initial()
        self.already_not_in_system = False
        self.already_failed_in_system = False
        self.prefix = []

    def post(self):
        pass

    def step(self, letter):
        self.num_steps += 1
        self.prefix.append(letter)
        l = self.spec_dfa.step(letter)
        in_system = l not in ['NoAction', 'NO_EFFECT']
        if (not in_system) or self.already_not_in_system:
            self.already_not_in_system = True
            return "?"
        self.system_queries += 1
        failed_in_system = self.system_dfa.step(letter)
        if failed_in_system or self.already_failed_in_system:
            self.already_failed_in_system = True
            return "+"
        else:
            return "-"

sul = TestSUL(M, B)

class TestOracle(Oracle):
    def __init__(self, alphabet, sul: TestSUL, sample_size=50, min_walk_len=5, max_sample_len=20):
        self.alphabet = alphabet
        self.sul = sul
        self.num_queries = 0
        self.num_steps = 0
        self.sample_size = sample_size
        self.min_walk_len = min_walk_len
        self.max_sample_len = max_sample_len

    def find_cex(self, hypothesis: MooreMachine):
        num_samples_done = 0
        sample_lengths = [randint(self.min_walk_len, self.max_sample_len) for _ in range(self.sample_size)]
        while num_samples_done < self.sample_size:
            inputs = []
            hypothesis.reset_to_initial()
            self.sul.spec_dfa.reset_to_initial()
            num_samples_done += 1
            num_steps = sample_lengths.pop(0)
            self.num_queries += 1
            for _ in range(num_steps):
                self.num_steps += 1
                inputs.append(choice(self.alphabet))
                out_spec = self.sul.spec_dfa.step(inputs[-1])
                out_hyp = hypothesis.step(inputs[-1])
                if out_spec and out_hyp == "+":
                    check = self.sul.query(tuple(inputs))
                    if check[0] != "+": # maybe should be less restrictive
                        return inputs

        num_samples_done = 0
        sample_lengths = [randint(self.min_walk_len, self.max_sample_len) for _ in range(self.sample_size)]
        while num_samples_done < self.sample_size:
            inputs = []
            hypothesis.reset_to_initial()
            self.sul.spec_dfa.reset_to_initial()
            num_samples_done += 1
            num_steps = sample_lengths.pop(0)
            self.num_queries += 1
            for _ in range(num_steps):
                self.num_steps += 1
                inputs.append(choice(self.alphabet))
                out_spec = self.sul.spec_dfa.step(inputs[-1])
                out_hyp = hypothesis.step(inputs[-1])
                if out_spec:
                    check = self.sul.query(tuple(inputs))
                    if check[0] != out_hyp: # maybe should be less restrictive
                        return inputs


#oracle = TestOracle(B.get_input_alphabet(), sul, sample_size=500, min_walk_len=1, max_sample_len=10)
#oracle = BFEOracle(B.get_input_alphabet(), sul, depth=7)
oracle = RandomWalkEqOracle(B.get_input_alphabet(), sul, num_steps=500)
oracle = RandomWMethodEqOracle(B.get_input_alphabet(), sul, walks_per_state=5000, walk_len=15)
dfa3, data = run_Lstar(B.get_input_alphabet(), sul, oracle, closing_strategy='longest_first', cex_processing=None,
                       automaton_type='moore', cache_and_non_det_check=False, return_data=True, print_level=0)
save_automaton_to_file(dfa3, path="output/" + example + "_dfa3")
#
opt_a_start = time.time()
dfa_a, mealy_a = find_minimal_consistent_dfa(dfa3)
opt_a_time = time.time() - opt_a_start
save_automaton_to_file(dfa_a, path="output/" + example + "_dfa_a")
save_automaton_to_file(mealy_a, path="output/" + example + "_mealy_a")

print("option b:")
opt_b_start = time.time()
rpni_data = dfa3_to_data(dfa3)
#rpni_data = observation_table_to_data(data["observation_table"])  # not working!!!
dfa_b = run_RPNI(rpni_data, automaton_type="dfa")
opt_b_time = time.time() - opt_b_start
save_automaton_to_file(dfa_b, path="output/" + example + "_dfa_b")
