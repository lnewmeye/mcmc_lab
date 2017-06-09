# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

# Import required modules
from matplotlib import pyplot as plt
import numpy as np
import os

# Import my classes
from node import *
from network import Network
from proposal import NormalProposal

# Read in faculty data
folder_name = '..' + os.sep + 'data'
file_name = 'faculty.dat'
file_path = os.path.join(folder_name, file_name)
data = np.genfromtxt(file_path)

# Create nodes in network
prior_mean = NormalNode(5, 1/9, NormalProposal(0.005))
prior_variance = InvGammaNode(11, 2.5, NormalProposal(0.002))
observations = []
for datum in data:
    new_observation = NormalNode(prior_mean, prior_variance, None)
    new_observation.set_fixed(datum)
    observations.append(new_observation)

# Add nodes as children
prior_mean.add_children(observations)
prior_variance.add_children(observations)

# Add nodes to network
network = Network(100, 50)
network.add_node(prior_mean)
network.add_node(prior_variance)
network.add_nodes(observations)

# Burn off samples
network.burn(100)
network.sample(50)

# Plot burn in of prior_mean
samples = np.array(network.burn_history)[:,0]
plt.plot(samples, label='Prior Mean Burn')
plt.title('Prior Mean Burn History')
plt.show()

# Plot mixing of prior_mean
samples = np.array(network.sample_history)[:,0]
plt.plot(samples, label='Prior Mean Mixing')
plt.title('Prior Mean Mixing')
plt.show()

# Plot burn in of prior_variance
samples = np.array(network.burn_history)[:,1]
plt.plot(samples, label='Prior Variance Burn')
plt.title('Prior Variance Burn History')
plt.show()

# Plot mixing of prior_variance
samples = np.array(network.sample_history)[:,1]
plt.plot(samples, label='Prior Variance Mixing')
plt.title('Prior Variance Mixing')
plt.show()

# Return estimates
prior_mean_estimate = network.estimate_mean(0)
print('prior_mean_estimate =', prior_mean_estimate)
print(np.array(network.samples)[:,0])
