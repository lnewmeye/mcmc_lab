# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

import numpy as np
from network import Network
from node import *

# Set parameters for simulation
N = 1000

# Create nodes in order of heiarchy
A = BernoulliNode([], [0.1])

# Add nodes to network
network = Network(1000, 100)
network.add_nodes([A])

network.burn()
network.sample(N)
probability = network.estimate_probability([1])
print('P(A=true) =', probability)
