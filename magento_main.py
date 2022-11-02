from magento_sul import MagentoSUL
from dc_lstar_2 import run_dc_lstar
from dc_oracle import DCOracle
from aalpy.utils import save_automaton_to_file



magento_sul = MagentoSUL()
alphabet = ["L1", "L2", "A", "C"]
hypothesis = run_dc_lstar(alphabet, magento_sul, DCOracle(alphabet, magento_sul, depth=6))
save_automaton_to_file(hypothesis, path="magento")

