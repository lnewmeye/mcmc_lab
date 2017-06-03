# CS 677 - Baysian Methods in CS
# MCMC Labs Network class
# Luke Newmeyer

class Network(object):

    def __init__(self, burn_samples=500, run_samples=200):

        # Define object attributes
        self.nodes = []
        self.burn_samples = burn_samples
        self.run_samples = run_samples

    def add_node(self, node):
        self.nodes.append(node)

    def add_nodes(self, nodes):
        self.nodes.extend(nodes)

    def burn(self):
        ''' Burn self.burn_samples in network '''

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
                row = []
                for node in self.nodes:
                    row.append(node.sample_conditional())
                self.sample_history.append(row)
            self.samples.append(self.sample_history[-1])

        return self.samples

    def estimate_probability(self, sequence):

        count = 0
        for sample in self.samples:
            if sample == sequence:
                count +=1

        return count / len(self.samples)
