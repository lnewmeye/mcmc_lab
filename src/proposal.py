# CS 677 - Baysian Methods in CS
# MCMC Labs Proposal class
# Luke Newmeyer

# Import required modules
from scipy import stats

class Proposal(object):
    def __init__(self):
        pass

class NormalProposal(Proposal):

    def __init__(self, variance):

        # Set object parameters
        self.variance = variance
        self.sigma = variance**(1/2)

    def sample(self, value):

        # Return sample using given value as mean
        return stats.norm.rvs(value, self.sigma)

class DiscreteProposal(Proposal):

    def __init__(self, variance):

        # Set object parameters
        self.variance = variance
        self.sigma = variance**(1/2)

    def sample(self, value):

        # Return sample using given value as mean
        continuous = stats.norm.rvs(value, self.sigma)
        return int(round(continuous))
