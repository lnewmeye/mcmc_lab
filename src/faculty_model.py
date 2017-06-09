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
network.sample(200)

# Retrieve data from network
burn = np.array(network.burn_history)
mixing = np.array(network.sample_history)
samples = np.array(network.samples)

# Plot burn in of prior_mean
mean_burn = burn[:,0]
plt.plot(mean_burn, label='Prior Mean Burn')
plt.title('Prior Mean Burn History')
plt.xlabel('Sample')
plt.ylabel('Sample Value')
plt.savefig('../img/faculty/prior_mean_burn.png')
plt.show()
plt.clf()

# Plot mixing of prior_mean
mean_mixing = mixing[:,0]
plt.plot(mean_mixing, label='Prior Mean Mixing')
plt.title('Prior Mean Mixing')
plt.xlabel('Sample')
plt.ylabel('Sample Value')
plt.savefig('../img/faculty/prior_mean_mixing.png')
plt.show()
plt.clf()

# Plot burn in of prior_variance
var_burn = burn[:,1]
plt.plot(var_burn, label='Prior Variance Burn')
plt.title('Prior Variance Burn History')
plt.xlabel('Sample')
plt.ylabel('Sample Value')
plt.savefig('../img/faculty/prior_variance_burn.png')
plt.show()
plt.clf()

# Plot mixing of prior_variance
var_mixing = mixing[:,1]
plt.plot(var_mixing, label='Prior Variance Mixing')
plt.title('Prior Variance Mixing')
plt.xlabel('Sample')
plt.ylabel('Sample Value')
plt.savefig('../img/faculty/prior_variance_mixing.png')
plt.show()
plt.clf()

# Plot histogram for prior_mean
mean_samples = samples[:,0]
plt.hist(mean_samples, bins=15, normed=True)
x_axis = np.arange(4, 6, 0.01)
y_axis = prior_mean.probability_density(x_axis)
plt.plot(x_axis, y_axis)
plt.show()

# Plot histogram for prior_variance
var_samples = samples[:,1]
plt.hist(var_samples, bins=15, normed=True)
x_axis = np.arange(0, 1, 0.005)
y_axis = prior_variance.probability_density(x_axis)
plt.plot(x_axis, y_axis)
plt.show()

# Print statistics
print('Average of variance node:', np.mean(var_samples))
print('Average of mean node:', np.mean(mean_samples))
print('Variance of data:', np.var(data))
print('Mean of data:', np.mean(data))

# Return estimates
#prior_mean_estimate = network.estimate_mean(0)
#print('prior_mean_estimate =', prior_mean_estimate)
