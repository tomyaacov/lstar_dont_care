import random

from aalpy.automata import Onfsm, Mdp, StochasticMealyMachine
from aalpy.base import Oracle, SUL
from aalpy.oracles import RandomWalkEqOracle
automaton_dict = {Onfsm: 'onfsm', Mdp: 'mdp', StochasticMealyMachine: 'smm'}


class RandomWalkOracle(RandomWalkEqOracle):

    def find_cex(self, hypothesis):
        if not self.automata_type:
            self.automata_type = automaton_dict.get(type(hypothesis), 'det')

        inputs = []
        outputs = []
        self.reset_hyp_and_sul(hypothesis)

        while self.random_steps_done < self.step_limit:
            self.num_steps += 1
            self.random_steps_done += 1

            if random.random() <= self.reset_prob:
                self.reset_hyp_and_sul(hypothesis)
                inputs.clear()
                outputs.clear()

            inputs.append(random.choice(self.alphabet))

            out_sul = self.sul.query(inputs)[-1]#self.sul.step(inputs[-1])
            outputs.append(out_sul)

            if self.automata_type == 'det':
                out_hyp = hypothesis.step(inputs[-1])
            else:
                out_hyp = hypothesis.step_to(inputs[-1], out_sul)

            if self.automata_type == 'det' and out_sul != out_hyp:
                if self.reset_after_cex:
                    self.random_steps_done = 0

                self.sul.post()
                return inputs
            elif out_hyp is None:
                if self.reset_after_cex:
                    self.random_steps_done = 0
                self.sul.post()

                if self.automata_type == 'onfsm':
                    return inputs, outputs
                else:
                    # hypothesis is MDP or SMM
                    cex = [hypothesis.initial_state.output] if self.automata_type == 'mdp' else []
                    for i, o in zip(inputs, outputs):
                        cex.extend([i, o])
                    return cex

        return None
