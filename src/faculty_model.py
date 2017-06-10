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
network.burn(300)
network.sample(500)

# Retrieve data from network
burn = np.array(network.burn_history)
mixing = np.array(network.sample_history)
samples = np.array(network.samples)

# Plot histogram for prior_mean and prior_varinace
mean_samples = samples[:,0]
mean_range = np.arange(4, 6, 0.01)
var_samples = samples[:,1]
var_range = np.arange(0, 1, 0.005)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18,6))
ax1.hist(mean_samples, bins=15, normed=True)
ax1.plot(mean_range, prior_mean.probability_density(mean_range))
ax1.set_title('Prior Mean Probability Density')
ax1.set_xlabel('Rating')
ax1.set_ylabel('Density')
ax2.hist(var_samples, bins=15, normed=True)
ax2.plot(var_range, prior_variance.probability_density(var_range))
ax2.set_title('Prior Variance Probability Density')
ax2.set_xlabel('Rating Variance')
ax2.set_ylabel('Density')
#plt.savefig('../img/faculty/histogram.png', dpi=40)

# Plot birn-in for both prior_mean and prior_variance
mean_burn = burn[:,0]
var_burn = burn[:,1]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18,6))
ax1.plot(mean_burn)
ax1.set_title('Prior Mean Burn-in')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(var_burn)
ax2.set_title('Prior Variance Burn-in')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
#plt.savefig('../img/faculty/burn-in.png', dpi=40)

# Plot mixing plot for both prior_mean and prior_variance
mean_mixing = mixing[:,0]
var_mixing = mixing[:,1]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18,6))
ax1.plot(mean_mixing)
ax1.set_title('Prior Mean Mixing')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(var_mixing)
ax2.set_title('Prior Variance Mixing')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
#plt.savefig('../img/faculty/mixing.png', dpi=40)

# Print statistics
print('Average of variance node:', np.mean(var_samples))
print('Average of mean node:', np.mean(mean_samples))
print('Variance of data:', np.var(data))
print('Mean of data:', np.mean(data))
