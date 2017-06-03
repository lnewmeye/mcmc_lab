# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

import numpy as np
from network import Network
from node import *

# Set simulation parameters
N = 500

# Create nodes in order of heiarchy
burglary = BernoulliNode([], [0.001])
earthquake = BernoulliNode([], [0.002])
alarm = BernoulliNode([burglary, earthquake], 
        [None, None, None, 0.95, 0.94, 0.29, 0.0001])
john = BernoulliNode([alarm], [None, 0.9, 0.05])
mary = BernoulliNode([alarm], [None, 0.7, 0.01])

# Add children to nodes
burglary.add_child(alarm)
earthquake.add_child(alarm)
alarm.add_children([john, mary])

# Add nodes to probability network
network = Network(5000, 20)
network.add_nodes([burglary, earthquake, alarm, john, mary])

# Simulate Russell and Norving's conclusion
john.set_fixed(True)
mary.set_fixed(True)

# Run network
network.burn()
network.sample(N)
#probability = network.estimate_probability([1, 1, 1, 1, 1]) + \
              #network.estimate_probability([1, 1, 0, 1, 1]) + \
              #network.estimate_probability([1, 0, 1, 1, 1]) + \
              #network.estimate_probability([1, 0, 0, 1, 1])
probability = network.estimate_probability([1, 1, 1, 1, 1]) + \
              network.estimate_probability([1, 0, 1, 1, 1]) + \
              network.estimate_probability([0, 1, 1, 1, 1]) + \
              network.estimate_probability([0, 0, 1, 1, 1])
print(probability)
