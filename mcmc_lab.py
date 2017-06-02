# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

import numpy as np
from network import Network
from node import *

# Create nodes in order of heiarchy
burglary = BernoulliNode([], [0.001])
earthquake = BernoulliNode([], [0.002])
alarm = BernoulliNode([burglary, earthquake], 
        [None, None, None, 0.95, 0.94, 0.29, 0.0001])
john = BernoulliNode([alarm], [None, 0.9, 0.05])
mary = BernoulliNode([alarm], [None, 0.7, 0.01])

# Add complete conditionals to each node

# Add nodes to probability network
network = Network()
