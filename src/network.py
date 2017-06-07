# CS 677 - Baysian Methods in CS
# MCMC Labs Network class
# Luke Newmeyer

from random import shuffle
import numpy as np

class Network(object):

    def __init__(self, burn_samples=1000, run_samples=200):

        # Define object attributes
        self.nodes = []
        self.burn_samples = burn_samples
        self.run_samples = run_samples

    def add_node(self, node):
        self.nodes.append(node)

    def add_nodes(self, nodes):
        self.nodes.extend(nodes)

    def burn(self, burn_samples=1000):
        ''' Burn self.burn_samples in network '''

        # Set internal burn_samples
        self.burn_samples = burn_samples

        self.burn_history = []
        for i in range(self.burn_samples):
            row = []
            for node in self.nodes:
                row.append(node.sample_conditional())
            self.burn_history.append(row)

    def sample(self, samples):
        ''' Run network for self.run_samples and return sample '''

        self.sample_history = []
        self.samples = []
        for i in range(samples):
            for j in range(self.run_samples):
                row = [0] * len(self.nodes)
                indicies = [i for i in range(len(self.nodes))]
                shuffle(indicies)
                for idx in indicies:
                    row[idx] = self.nodes[idx].sample_conditional()
                #for node in random_nodes:
                    #row.append(node.sample_conditional())
                self.sample_history.append(row)
            self.samples.append(self.sample_history[-1])

        return self.samples

    def estimate_probability(self, sequence):

        # Find indicies of empty elements in sequence
        indicies = []
        for idx, value in enumerate(sequence):

            # Add index if value is None
            if value is not None:
                indicies.append(idx)

        # Form samples into columns without values None
        samples = np.array(self.samples)[:,indicies]
        sequence = np.array(sequence)[indicies]

        # Count samples matching sequence
        matches = (samples == sequence).all(axis=1)

        # Estimate probability by dividing count by total samples
        return matches.sum() / matches.size
