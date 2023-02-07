from aalpy.SULs import DfaSUL
from aalpy.oracles import RandomWalkEqOracle
from aalpy.learning_algs import run_Lstar
from aalpy.utils import get_Angluin_dfa, save_automaton_to_file, load_automaton_from_file

example = "gearbox"
dfa = load_automaton_from_file('data/models/' + example + 'FaultLanguage.dot', automaton_type='dfa')

alphabet = dfa.get_input_alphabet()

sul = DfaSUL(dfa)
eq_oracle = RandomWalkEqOracle(alphabet, sul, 30000)

learned_dfa = run_Lstar(alphabet, sul, eq_oracle, automaton_type='dfa',
                        cache_and_non_det_check=True, cex_processing=None, print_level=3)

save_automaton_to_file(learned_dfa, path="output/tmp")