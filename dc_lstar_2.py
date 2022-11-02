from aalpy.learning_algs import run_Lstar
from dc_oracle import DCOracle
from dc_sul import DCSUL
from dc_dfa import find_minimal_consistent_dfa

def run_dc_lstar(alphabet: list, sul: DCSUL, oracle: DCOracle):
    dfa3 = run_Lstar(alphabet, sul, oracle, automaton_type='moore', cex_processing='longest_prefix')
    return find_minimal_consistent_dfa(dfa3)
