# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

import numpy as np
from network import Network
from node import *

# Set simulation parameters
N = 2000

# Create nodes in order of heiarchy
A = BernoulliNode([], [0.2])
B = BernoulliNode([A], [None, 0.3, 0.6])
C = BernoulliNode([A, B], [None, None, None, 0.4, 0.5, 0.6, 0.3])
D = BernoulliNode([A, B, C], [None, None, None, None, None, None, None,
        0.01, 0.08, 0.31, 0.40, 0.01, 0.02, 0.001, 0.001])

# Add children to nodes
A.add_children([B, C, D])
B.add_children([C, D])
C.add_children([D])

# Add nodes to probability network
network = Network(5000, 100)
network.add_nodes([A, B, C, D])

# Simulate A given D
D.set_fixed(True)
network.burn()
network.sample(N)
probability = network.estimate_probability([1, None, None, None])
print('P(A=true|D=true) =', probability)

# Simulate D given A and B
A.set_fixed(True)
B.set_fixed(True)
D.set_unknown()
network.burn()
network.sample(N)
probability = network.estimate_probability([None, None, None, 1])
print('P(D=true|A=true,B=true) =', probability)
