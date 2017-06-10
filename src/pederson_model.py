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

# Create main nodes in network
A = NormalNode(5.0, 0.1, NormalProposal(0.9))
B = InvGammaNode(5.0, 1/0.1, NormalProposal(0.3))
C = GammaNode(A, 1/0.1, NormalProposal(0.01))
D = NormalSqVarNode(B, C, NormalProposal(0.2))

# Create observation nodes in network
Y = [GammaNode(D, 1/0.2, NormalProposal(0.1)),
     GammaNode(D, 1/0.2, NormalProposal(0.1)),
     GammaNode(D, 1/0.2, NormalProposal(0.1)),
     GammaNode(D, 1/0.2, NormalProposal(0.1)),
     GammaNode(D, 1/0.2, NormalProposal(0.1))]
Y[0].set_fixed(1.50)
Y[1].set_fixed(2.00)
Y[2].set_fixed(2.25)
Y[3].set_fixed(1.75)
Y[4].set_fixed(2.00)

# Set child relationships
A.add_child(C)
B.add_child(D)
C.add_child(D)
D.add_children(Y)

# Add nodes to network
network = Network(1000, ndump)
network.add_nodes([A, B, C, D])
network.add_nodes(Y)

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
#plt.savefig('../img/pederson/a_subplot.png', dpi=40)

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
#plt.savefig('../img/pederson/b_subplot.png', dpi=40)

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
#plt.savefig('../img/pederson/c_subplot.png', dpi=40)

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
#plt.savefig('../img/pederson/d_subplot.png', dpi=40)
