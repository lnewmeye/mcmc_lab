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

    def __init__(self, value=None, evidence=None):

        # Define object attributes
        self.evidence = evidence #if evidence is set do not sample randomly
        self.children = []

        # Initialize value if no value passed
        if value == None:
            # Initialize randomly from distribution
            self.value = self.sample_distribution()
        else:
            # Set value to value provided to init function
            self.value == value

    def set_evidence(self, evidence):
        self.evidence = evidence

    def get_evidence(self, evidence):
        return self.evidence

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def add_child(self, name, child):
        children.append(child)

class BernoulliNode(Node):

    # Initalization of object
    def __init__(self, dependencies, probabilities, value=None, evidence=None):
        ''' Initialize object given a list of dependent nodes and a list of 
        probabilities for a tree structure from the dependencies '''

        # Define distribution as a BernoulliTree from the given dependencies
        self.parents = dependencies
        self.distribution = BernoulliTree(probabilities)

        # Call super node's init function
        super(BernoulliNode, self).__init__(value, evidence)

    # Set complete conditional distribution for object
    def set_conditional(self, dependencies, probabilities):

        # Define conditional as a BernoulliTree from the given dependencies
        self.dependencies = dependencies
        self.conditional = BernoulliTree(probabilities)

    def sample_distribution(self):

         # Get value for each dependency and append to array
        parent_values = []
        for parent in self.parents:
            parent_values.append(parent.get_value())

        # Save sample in object and return
        probability = self.distribution.get_probability(parent_values)
        self.value = stats.bernoulli.rvs(probability)
        return self.value

    def sample_conditional(self):

        # Get value for each dependency and append to array
        dependency_values = []
        for dependency in self.dependencies:
            dependency_values.append(dependency.get_value())

        # Save sample in object and return
        probability = self.conditional.get_probability(dependency_values)
        self.value = stats.bernoulli.rvs(probability)
        return self.value
