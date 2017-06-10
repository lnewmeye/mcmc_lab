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
nburn = 10000
nsamples = 300
ndump = 20

# Create nodes in network
A = NormalNode(20, 1, NormalProposal(1.3))
APi = NormalNodePi(A)
E = BetaNode(1, 1, NormalProposal(0.1))
B = GammaNode(APi, 7, NormalProposal(0.5))
D = BetaNode(A, E, NormalProposal(0.03))
C = BernoulliNode([], [D])
F = PoissonNode(D, DiscreteProposal(1.2))
G = NormalNode(E, F, NormalProposal(10000))

# Add children to parents
A.add_children([B, D])
E.add_children([D, G])
D.add_children([C, F])
F.add_child(G)

# Create network and add nodes
network = Network(10, ndump)
network.add_nodes([A, APi, E, B, D, C, F, G])

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
plt.savefig('../img/wacky/a_subplot.png', dpi=40)

# Plot burn, mixing, and data for E
plot_burn = np.array(burn[2])
plot_mixing = np.array(mixing[2])
plot_samples = np.array(samples[2])
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
plt.savefig('../img/wacky/e_subplot.png', dpi=40)

# Plot burn, mixing, and data for B
plot_burn = np.array(burn[3])
plot_mixing = np.array(mixing[3])
plot_samples = np.array(samples[3])
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
plt.savefig('../img/wacky/b_subplot.png', dpi=40)

# Plot burn, mixing, and data for D
plot_burn = np.array(burn[4])
plot_mixing = np.array(mixing[4])
plot_samples = np.array(samples[4])
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
plt.savefig('../img/wacky/d_subplot.png', dpi=40)

# Plot burn, mixing, and data for C
plot_burn = np.array(burn[5])
plot_mixing = np.array(mixing[5])
plot_samples = np.array(samples[5])
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
plt.savefig('../img/wacky/c_subplot.png', dpi=40)

# Plot burn, mixing, and data for F
plot_burn = np.array(burn[6])
plot_mixing = np.array(mixing[6])
plot_samples = np.array(samples[6])
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,6))
ax1.plot(plot_burn)
ax1.set_title('Burn for F')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(plot_mixing)
ax2.set_title('Mixing for F')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
ax3.hist(plot_samples, bins=15, normed=True)
ax3.set_title('Histogram for F')
ax3.set_xlabel('Value')
ax3.set_ylabel('Density')
plt.savefig('../img/wacky/f_subplot.png', dpi=40)

# Plot burn, mixing, and data for G
plot_burn = np.array(burn[7])
plot_mixing = np.array(mixing[7])
plot_samples = np.array(samples[7])
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,6))
ax1.plot(plot_burn)
ax1.set_title('Burn for G')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(plot_mixing)
ax2.set_title('Mixing for G')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
ax3.hist(plot_samples, bins=15, normed=True)
ax3.set_title('Histogram for G')
ax3.set_xlabel('Value')
ax3.set_ylabel('Density')
plt.savefig('../img/wacky/g_subplot.png', dpi=40)

# Set evidence nodes
G.set_fixed(5)

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
plt.savefig('../img/wacky/a_evidence.png', dpi=40)

# Plot burn, mixing, and data for E
plot_burn = np.array(burn[2])
plot_mixing = np.array(mixing[2])
plot_samples = np.array(samples[2])
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
plt.savefig('../img/wacky/e_evidence.png', dpi=40)

# Plot burn, mixing, and data for B
plot_burn = np.array(burn[3])
plot_mixing = np.array(mixing[3])
plot_samples = np.array(samples[3])
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
plt.savefig('../img/wacky/b_evidence.png', dpi=40)

# Plot burn, mixing, and data for D
plot_burn = np.array(burn[4])
plot_mixing = np.array(mixing[4])
plot_samples = np.array(samples[4])
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
plt.savefig('../img/wacky/d_evidence.png', dpi=40)

# Plot burn, mixing, and data for C
plot_burn = np.array(burn[5])
plot_mixing = np.array(mixing[5])
plot_samples = np.array(samples[5])
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
plt.savefig('../img/wacky/c_evidence.png', dpi=40)

# Plot burn, mixing, and data for F
plot_burn = np.array(burn[6])
plot_mixing = np.array(mixing[6])
plot_samples = np.array(samples[6])
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,6))
ax1.plot(plot_burn)
ax1.set_title('Burn for F')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(plot_mixing)
ax2.set_title('Mixing for F')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
ax3.hist(plot_samples, bins=15, normed=True)
ax3.set_title('Histogram for F')
ax3.set_xlabel('Value')
ax3.set_ylabel('Density')
plt.savefig('../img/wacky/f_evidence.png', dpi=40)

# Plot burn, mixing, and data for G
plot_burn = np.array(burn[7])
plot_mixing = np.array(mixing[7])
plot_samples = np.array(samples[7])
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,6))
ax1.plot(plot_burn)
ax1.set_title('Burn for G')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(plot_mixing)
ax2.set_title('Mixing for G')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
ax3.hist(plot_samples, bins=15, normed=True)
ax3.set_title('Histogram for G')
ax3.set_xlabel('Value')
ax3.set_ylabel('Density')
plt.savefig('../img/wacky/g_evidence.png', dpi=40)
