# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

# Import required modules
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import os

# Import my classes
from node import *
from network import Network
from proposal import NormalProposal

# Set simulation parameters
nburn = 300
ndump = 50
nsample = 10000

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
network = Network(nburn, ndump)
network.add_node(prior_mean)
network.add_node(prior_variance)
network.add_nodes(observations)

# Burn off samples
network.burn(nburn)
network.sample(nsample)

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

# Plot joint distribution for prior_mean and prior_varinace
fig, (ax) = plt.subplots(1, 1, figsize=(9,6))
ax.hist2d(mean_samples, var_samples, bins=40, norm=LogNorm())
plt.savefig('../img/learning/faculty_joint_none.png', dpi=40)



# Start and run network with additional hyper-parameter
hyper_mean_mean = NormalNode(5, 1.5, NormalProposal(0.01))
#hyper_mean_mean = NormalNode(18, 1.5, NormalProposal(0.01))
prior_mean.set_mean(hyper_mean_mean)
hyper_mean_mean.add_child(prior_mean)
network.add_node(hyper_mean_mean)

# Run network with added hyper-parameter
network.burn(nburn)
network.sample(nsample)

# Save data for hyper-parameter
burn1 = np.array(network.burn_history)
mixing1 = np.array(network.sample_history)
samples1 = np.array(network.samples)
mean_samples1 = samples1[:,0]
var_samples1 = samples1[:,1]



# Start and run network with additional hyper-parameter
hyper_mean_var = InvGammaNode(2, 1/9, NormalProposal(0.005))
#hyper_mean_var = InvGammaNode(4, 1/19, NormalProposal(0.01))
prior_mean.set_variance(hyper_mean_var)
hyper_mean_var.add_child(prior_mean)
network.add_node(hyper_mean_var)

# Run network with added hyper-parameter
network.burn(nburn)
network.sample(nsample)

# Save data for hyper-parameter
burn2 = np.array(network.burn_history)
mixing2 = np.array(network.sample_history)
samples2 = np.array(network.samples)
mean_samples2 = samples2[:,0]
var_samples2 = samples2[:,1]



# Start and run network with additional hyper-parameter
hyper_var_alpha = GammaNode(3, 3/11, NormalProposal(0.4))
#hyper_var_alpha = GammaNode(8, 1/21, NormalProposal(0.4))
prior_variance.set_alpha(hyper_var_alpha)
hyper_var_alpha.add_child(prior_variance)
network.add_node(hyper_var_alpha)

# Run network with added hyper-parameter
network.burn(nburn)
network.sample(nsample)

# Save data for hyper-parameter
burn3 = np.array(network.burn_history)
mixing3 = np.array(network.sample_history)
samples3 = np.array(network.samples)
mean_samples3 = samples3[:,0]
var_samples3 = samples3[:,1]



# Start and run network with additional hyper-parameter
hyper_var_beta = GammaNode(1, 1/2.5, NormalProposal(0.1))
#hyper_var_beta = GammaNode(2, 1/5.5, NormalProposal(0.1))
prior_variance.set_beta(hyper_var_beta)
hyper_var_beta.add_child(prior_variance)
network.add_node(hyper_var_beta)

# Run network with added hyper-parameter
network.burn(nburn)
network.sample(nsample)

# Save data for hyper-parameter
burn4 = np.array(network.burn_history).T
mixing4 = np.array(network.sample_history).T
samples4 = np.array(network.samples).T
mean_samples4 = samples4[0]
var_samples4 = samples4[1]




# Plot joint distribution with hyper-parameters included
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(18,6))
ax1.hist2d(mean_samples1, var_samples1, bins=40, norm=LogNorm())
ax1.set_xlim(5.0, 6.5)
ax1.set_ylim(0.1, 0.6)
ax2.hist2d(mean_samples2, var_samples2, bins=40, norm=LogNorm())
ax2.set_xlim(5.0, 6.5)
ax2.set_ylim(0.1, 0.6)
ax3.hist2d(mean_samples3, var_samples3, bins=40, norm=LogNorm())
ax3.set_xlim(5.0, 6.5)
ax3.set_ylim(0.1, 0.6)
ax4.hist2d(mean_samples4, var_samples4, bins=40, norm=LogNorm())
ax4.set_xlim(5.0, 6.5)
ax4.set_ylim(0.1, 0.6)
plt.savefig('../img/learning/faculty_joint_hyper.png', dpi=40)
#plt.savefig('../img/learning/faculty_joint_off.png', dpi=40)

# Analyze the mixing for the hyper-pparameters
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(18,6))
ax1.plot(mixing4[-4])
ax2.plot(mixing4[-3])
ax3.plot(mixing4[-2])
ax4.plot(mixing4[-1])
plt.savefig('../img/tmp/hyper_mixing.png')
