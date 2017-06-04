# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

import numpy as np
from network import Network
from node import *

# Set parameters for simulation
N = 1000

# Create nodes in order of heiarchy
A = BernoulliNode([], [0.5])
B = BernoulliNode([A], [None, 0.2, 0.3])

# Add children to nodes
A.add_child(B)

# Add nodes to network
network = Network(1000, 100)
network.add_nodes([A, B])

# Simulate joint distribution
network.burn()
network.sample(N)

# Print probabilities
probability = network.estimate_probability([1, 1])
print('P(A=true, B=true) ~=', probability)
probability = network.estimate_probability([1, 0])
print('P(A=true, B=false) ~=', probability)
probability = network.estimate_probability([0, 1])
print('P(A=false, B=true) ~=', probability)
probability = network.estimate_probability([0, 0])
print('P(A=false, B=false) ~=', probability)
probability = network.estimate_probability([1, 1]) + \
        network.estimate_probability([1, 0])
print('P(A=true) ~=', probability)
probability = network.estimate_probability([1, 1]) + \
        network.estimate_probability([0, 1])
print('P(B=true) ~=', probability)

'''# Simulate conditional distribution given A is True
A.set_fixed(True)
network.sample(N)
probability = network.estimate_probability([1, 1])
print('P(B=true|A=true) =', probability)

# Simulate conditional distribution given A is False
A.set_fixed(False)
network.sample(N)
probability = network.estimate_probability([0, 1])
print('P(B=true|A=false) =', probability)

# Simulate conditional distribution given B is True
#A.set_unkown()
B.set_fixed(True)
network.sample(N)
probability = network.estimate_probability([1, 1])
print('P(A=true|B=true) =', probability)'''

B.set_fixed(False)
network.burn()
network.sample(N)
probability = network.estimate_probability([1, 0])
print('P(A=true|B=false) =', probability)
