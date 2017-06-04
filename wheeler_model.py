# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

import numpy as np
from network import Network
from node import *

# Set simulation parameters
N = 2000

# Create nodes in order of heiarchy
A = BernoulliNode([], [0.9])
B = BernoulliNode([A], [None, 0.8, 0.7])
C = BernoulliNode([B], [None, 0.6, 0.5])
D = BernoulliNode([A, B], [None, None, None, 0.4, 0.3, 0.2, 0.1])
E = BernoulliNode([B, C], [None, None, None, 0.2, 0.3, 0.4, 0.5])

# Add children to nodes
A.add_children([B, D])
B.add_children([C, D, E])
C.add_children([E])

# Add nodes to probability network
network = Network(5000, 100)
network.add_nodes([A, B, C, D, E])

# Simulate A given D and E
D.set_fixed(False)
E.set_fixed(False)
network.burn()
network.sample(N)
probability = network.estimate_probability([1, None, None, None, None])
print('P(A=true|D=false,E=false) =', probability)
