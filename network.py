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

        # Add node to list
        self.nodes.append(node)

    def burn():
        pass
        ''' Burn self.burn_samples in network '''

    def sample():
        pass
        ''' Run network for self.run_samples and return sample '''
