from aalpy.learning_algs import run_Lstar
from dc_oracle import DCOracle
from aalpy.oracles import StatePrefixEqOracle
from dc_sul import DCSUL
from dc_dfa import find_minimal_consistent_dfa


def run_dc_lstar(alphabet: list, sul: DCSUL, oracle: DCOracle):
    state_origin_eq_oracle = StatePrefixEqOracle(alphabet, sul, walks_per_state=15, walk_len=20)
    dfa3 = run_Lstar(alphabet, sul, state_origin_eq_oracle, cex_processing='rs', closing_strategy='single', automaton_type='moore', cache_and_non_det_check=False)
    return find_minimal_consistent_dfa(dfa3)



if __name__ == "__main__":
    from magento_sul import MagentoSUL
    from aalpy.utils import save_automaton_to_file
    magento_sul = MagentoSUL()
    alphabet = ["L1", "L2", "A", "C"]
    hypothesis = run_dc_lstar(alphabet, magento_sul, DCOracle(alphabet, magento_sul, depth=6))
    save_automaton_to_file(hypothesis, path="magento")
