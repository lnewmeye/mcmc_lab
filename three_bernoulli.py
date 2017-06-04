# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

import numpy as np
from network import Network
from node import *

# Set parameters for simulation
N = 10000

# Create nodes in order of heiarchy
A = BernoulliNode([], [0.9])
B = BernoulliNode([A], [None, 0.9, 0.1])
C = BernoulliNode([A], [None, 0.8, 0.2])

# Add children to nodes
A.add_child(B)
A.add_child(C)

# Add nodes to network
network = Network(1000, 10)
network.add_nodes([A, B, C])

# Simulate conditional distribution for B=True, C=True
if False:
    B.set_fixed(True)
    C.set_fixed(True)
    network.burn()
    network.sample(N)
    probability = network.estimate_probability([1, 1, 1])
    print('P(A=true|C=true,B=true) =', probability)

# Simulate conditional distribution for B=True
if True:
    B.set_unkown()
    C.set_fixed(True)
    network.burn()
    network.sample(N)
    probability = network.estimate_probability([1, 1, 1]) + \
            network.estimate_probability([1, 0, 1])
    print('P(A=true|C=true) =', probability)

# Simultae joint distribution
if False:
    B.set_unkown()
    C.set_unkown()
    network.burn()
    network.sample(N)
    probability = network.estimate_probability([1, 1, 1])
    print('P(A=true,B=false,C=false) =', probability)

print('A =', A)
print('B =', B)
print('C =', C)
