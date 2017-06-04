# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

import numpy as np
from network import Network
from node import *

# Set simulation parameters
N = 2000

# Create nodes in order of heiarchy
is_republican = BernoulliNode([], [0.5])
republican_nomination = BernoulliNode([is_republican], [None, 0.7, 0.01])
endorsed_carson = BernoulliNode([republican_nomination], [None, 0.8, 0.1])
endorsed_cruz = BernoulliNode([republican_nomination], [None, 0.5, 0.01])
democratic_nomination = BernoulliNode([is_republican], [None, 0.001, 0.6])
endorsed_sanders = BernoulliNode([democratic_nomination], [None, 0.5, 0.001])
endorsed_clinton = BernoulliNode([democratic_nomination], [None, 0.6, 0.01])
wins_election = BernoulliNode(
        [endorsed_carson, endorsed_cruz, endorsed_sanders, endorsed_clinton],
        [None, None, None, None, None, None, None, None, None, None, None,
         None, None, None, None, 0.999, 0.98, 0.99, 0.7, 0.8, 0.8, 0.5, 
         0.5, 0.3, 0.5, 0.3, 0.01, 0.1, 0.01, 0.001, 0.0001])

# Add children to nodes
is_republican.add_children([republican_nomination, democratic_nomination])
republican_nomination.add_children([endorsed_carson, endorsed_cruz])
endorsed_carson.add_children([wins_election])
endorsed_cruz.add_children([wins_election])
democratic_nomination.add_children([endorsed_sanders, endorsed_clinton])
endorsed_sanders.add_children([wins_election])
endorsed_clinton.add_children([wins_election])

network = Network(5000, 100)
network.add_nodes([is_republican, republican_nomination, endorsed_carson,
        endorsed_cruz, democratic_nomination, endorsed_sanders,
        endorsed_clinton, wins_election])

# Simulate probability of is_republican given wins_election
wins_election.set_fixed(True)
network.sample(N)
probability = network.estimate_probability([1, None, None, None, None,
        None, None, None, None])
print('P(Is Republican=true|Wins Election=true) =', probability)
probability = network.estimate_probability([None, 1, None, None, None,
        None, None, None, None])
print('P(Republican Nomination=true|Wins Election=true) =', probability)
