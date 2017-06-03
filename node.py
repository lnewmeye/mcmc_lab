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

    def set_unkown(self):
        # TODO: add option to provide value?
        self.fixed = False

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def add_child(self,  child):
        self.children.append(child)

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def get_children(self):
        return self.children



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

    def get_probability(self):

        # Get value for each dependency and append to array
        parent_values = []
        for parent in self.parents:
            parent_values.append(parent.get_value())

        # Save sample in object and return
        probability = self.distribution.get_probability(parent_values)
        return probability

    def sample_distribution(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Get probability of distribution
        probability = self.get_probability()

        # Save sample in object and return
        self.value = stats.bernoulli.rvs(probability)
        return self.value

    def sample_conditional(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Initalize numerator and denominator with current distribution
        numerator = self.get_probability()
        denominator = 1 - numerator

        # Iterate through children and make running product
        for child in self.children:

            # Find probability of current state
            numerator *= child.get_probability()

            # Fake by switching current value and find probability
            self.set_value(not self.get_value())
            denominator *= child.get_probability()
            self.set_value(not self.get_value())

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

    def sample_set_conditional(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Get value for each dependency and append to array
        dependency_values = []
        for dependency in self.dependencies:
            dependency_values.append(dependency.get_value())

        # Save sample in object and return
        probability = self.conditional.get_probability(dependency_values)
        self.value = stats.bernoulli.rvs(probability)
        return self.value
