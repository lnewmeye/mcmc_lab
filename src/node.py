# CS 677 - Baysian Methods in CS
# MCMC Labs Node class
# Luke Newmeyer

''' 
Instructions for use:
1. Create nodes in order of heiarchy. Each distribution requires that the
   parent nodes be given
2. In the case that the node has a defined complete conditional, the
   appropriate function should be called to initalize the conditional
'''

from scipy import stats
from bernoullitree import *

class Node(object):

    def __init__(self, value=None, fixed=False):

        # Define object attributes
        self.fixed = fixed
        self.children = []
        self.acceptance = 1e-36

        # Initialize value if no value passed
        if value == None:
            # Initialize randomly from distribution
            self.value = self.sample_distribution()
        else:
            # Set value to value provided to init function
            self.value == value

    def set_fixed(self, value):
        self.value = value
        self.fixed = True

    def set_unknown(self):
        self.fixed = False

    def add_child(self,  child):
        self.children.append(child)

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def sample_conditional(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Get proposed value from proposal distribution and find probability
        previous_value = self.value
        self.value = self.sample_proposal()
        new_acceptance = self.get_probability()

        # Iterate through children and compute running product
        for child in self.children:
            new_acceptance *= child.current_probability()

        # Compute acceptance ratio (alpha) from new and previous proportions
        alpha = new_acceptance / self.acceptance
        self.acceptance = new_acceptance

        # Find new value based on Metropolis algorithm
        if alpha < 1.0:
            if stats.bernoulli.rvs(alpha) == 0:
                self.value = previous_value

        return self.value

    def sample_proposal(self):
        #TODO: Finish this function
        pass



class NormalNode(Node):
    def __init__(self, value=None, fixed=False):
        super(BernoulliNode, self).__init__(value, fixed)
    def current_probability(self):
        pass
    def sample_distribution(self):
        pass



class GammaNode(Node):
    def __init__(self, value=None, fixed=False):
        super(BernoulliNode, self).__init__(value, fixed)
    def current_probability(self):
        pass
    def sample_distribution(self):
        pass



class InvGammaNode(Node):
    def __init__(self, value=None, fixed=False):
        super(BernoulliNode, self).__init__(value, fixed)
    def current_probability(self):
        pass
    def sample_distribution(self):
        pass



class PoissonNode(Node):
    def __init__(self, value=None, fixed=False):
        super(BernoulliNode, self).__init__(value, fixed)
    def current_probability(self):
        pass
    def sample_distribution(self):
        pass



class BetaNode(Node):
    def __init__(self, value=None, fixed=False):
        super(BernoulliNode, self).__init__(value, fixed)
    def current_probability(self):
        pass
    def sample_distribution(self):
        pass



#class BinomialNode(Node):
    '''def __init__(self, value=None, fixed=False):
        super(BernoulliNode, self).__init__(value, fixed)
    def current_probability(self):
        pass
    def sample_distribution(self):
        pass'''



class BernoulliNode(Node):

    # Initalization of object
    def __init__(self, dependencies, probabilities, value=None, fixed=False):
        ''' Initialize object given a list of dependent nodes and a list of 
        probabilities for a tree structure from the dependencies '''

        # Define distribution as a BernoulliTree from the given dependencies
        self.parents = dependencies
        self.distribution = BernoulliTree(probabilities)

        # Call super node's init function
        super(BernoulliNode, self).__init__(value, fixed)

    def current_probability(self):

        # Get value for each dependency and append to array
        parent_values = []
        for parent in self.parents:
            parent_values.append(parent.value)

        # Save sample in object and return
        probability = self.distribution.get_probability(parent_values)
        if self.value == True:
            return probability
        return 1 - probability

    def sample_distribution(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Get probability of distribution
        self.value = True
        probability = self.current_probability()

        # Save sample in object and return
        self.value = stats.bernoulli.rvs(probability)
        return self.value

    def sample_conditional(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Initalize numerator and denominator with current distribution
        self.value = True
        numerator = self.current_probability()
        denominator = 1 - numerator

        # Iterate through children and compute running product
        for child in self.children:

            # Spoof children by setting value to true and compute probability
            self.value = True
            numerator *= child.current_probability()

            # Spoof children by setting value to false and compute probability
            self.value = False
            denominator *= child.current_probability()

        # Find probaility from bayes law
        denominator += numerator
        probability = numerator / denominator

        # Save sample value in object and return
        self.value = stats.bernoulli.rvs(probability)
        return self.value

    # Set complete conditional distribution for object
    def set_conditional(self, dependencies, probabilities):

        # Define conditional as a BernoulliTree from the given dependencies
        self.dependencies = dependencies
        self.conditional = BernoulliTree(probabilities)



