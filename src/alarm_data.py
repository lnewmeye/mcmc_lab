# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

import numpy as np
from network import Network
from node import *

# Set simulation parameters
N = 1000

# Create nodes in order of heiarchy
burglary = BernoulliNode([], [0.2])
earthquake = BernoulliNode([], [0.3])
alarm = BernoulliNode([burglary, earthquake], 
        [None, None, None, 0.95, 0.94, 0.29, 0.2])
john = BernoulliNode([alarm], [None, 0.9, 0.2])
mary = BernoulliNode([alarm], [None, 0.7, 0.3])

# Add children to nodes
burglary.add_child(alarm)
earthquake.add_child(alarm)
alarm.add_children([john, mary])

# Add nodes to probability network
network = Network(5000, 100)
network.add_nodes([burglary, earthquake, alarm, john, mary])

# Simulate joint distribution
network.burn()
network.sample(N)

# Create routine for randomly replacing samples
def random_nan(samples):
    mask_rnd = np.random.randint(0,5,size=samples.shape)
    mask = mask_rnd >= 4
    values = np.empty(samples.shape)
    values[:,:] = np.nan
    samples[mask] = values[mask]
    return samples

# Save data to file
samples = np.array(network.samples, dtype=float)
#samples = random_nan(samples)
#np.save('../data/alarm_modified.npy', samples)
