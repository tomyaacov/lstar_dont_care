from paper_sul import PaperSUL
from aalpy.utils import save_automaton_to_file
from dc_oracle import DCOracle
from dc_lstar import run_dc_lstar


paper_sul = PaperSUL()
alphabet = ["a", "b"]
hypothesis = run_dc_lstar(alphabet, paper_sul, DCOracle(alphabet, paper_sul, depth=6))
save_automaton_to_file(hypothesis, path="paper_dfa")
