# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

# Import required modules
from matplotlib import pyplot as plt
import numpy as np
import os

# Import my classes
from node import *
from network import *
from proposal import *

# Set parameters for for 
nburn = 3000
nsamples = 300
ndump = 100

# Create nodes in network
A = NormalNode(0.3, 0.2, NormalProposal(0.4))
B = InvGammaNode(11.0, 0.5, NormalProposal(0.002))
C = NormalNode(A, B, NormalProposal(0.1))
D = BetaNode(10.0, 1.0, NormalProposal(0.02))
E = NormalNode(D, C, NormalProposal(0.01))

# Add children to parents
A.add_child(C)
B.add_child(C)
C.add_child(E)
D.add_child(E)

# Set evidence nodes
E.set_fixed(0.6)

# Add nodes to network
network = Network(1000, ndump)
network.add_nodes([A, B, C, D, E])

# Burn and sample
network.burn(nburn)
network.sample(nsamples)

# Get data from network
burn = np.array(network.burn_history).T
mixing = np.array(network.sample_history).T
samples = np.array(network.samples).T

# Plot burn, mixing, and data for A
plot_burn = np.array(burn[0])
plot_mixing = np.array(mixing[0])
plot_samples = np.array(samples[0])
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,6))
ax1.plot(plot_burn)
ax1.set_title('Burn for A')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(plot_mixing)
ax2.set_title('Mixing for A')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
ax3.hist(plot_samples, bins=15, normed=True)
ax3.set_title('Histogram for A')
ax3.set_xlabel('Value')
ax3.set_ylabel('Density')
#plt.savefig('../img/jackson/a_subplot.png', dpi=40)

# Plot burn, mixing, and data for B
plot_burn = np.array(burn[1])
plot_mixing = np.array(mixing[1])
plot_samples = np.array(samples[1])
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,6))
ax1.plot(plot_burn)
ax1.set_title('Burn for B')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(plot_mixing)
ax2.set_title('Mixing for B')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
ax3.hist(plot_samples, bins=15, normed=True)
ax3.set_title('Histogram for B')
ax3.set_xlabel('Value')
ax3.set_ylabel('Density')
#plt.savefig('../img/jackson/b_subplot.png', dpi=40)

# Plot burn, mixing, and data for C
plot_burn = np.array(burn[2])
plot_mixing = np.array(mixing[2])
plot_samples = np.array(samples[2])
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,6))
ax1.plot(plot_burn)
ax1.set_title('Burn for C')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(plot_mixing)
ax2.set_title('Mixing for C')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
ax3.hist(plot_samples, bins=15, normed=True)
ax3.set_title('Histogram for C')
ax3.set_xlabel('Value')
ax3.set_ylabel('Density')
#plt.savefig('../img/jackson/c_subplot.png', dpi=40)

# Plot burn, mixing, and data for D
plot_burn = np.array(burn[3])
plot_mixing = np.array(mixing[3])
plot_samples = np.array(samples[3])
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,6))
ax1.plot(plot_burn)
ax1.set_title('Burn for D')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(plot_mixing)
ax2.set_title('Mixing for D')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
ax3.hist(plot_samples, bins=15, normed=True)
ax3.set_title('Histogram for D')
ax3.set_xlabel('Value')
ax3.set_ylabel('Density')
#plt.savefig('../img/jackson/d_subplot.png', dpi=40)

# Plot burn, mixing, and data for E
plot_burn = np.array(burn[4])
plot_mixing = np.array(mixing[4])
plot_samples = np.array(samples[4])
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,6))
ax1.plot(plot_burn)
ax1.set_title('Burn for E')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(plot_mixing)
ax2.set_title('Mixing for E')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
ax3.hist(plot_samples, bins=15, normed=True)
ax3.set_title('Histogram for E')
ax3.set_xlabel('Value')
ax3.set_ylabel('Density')
#plt.savefig('../img/jackson/e_subplot.png', dpi=40)
