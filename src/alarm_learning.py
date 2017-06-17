# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

import numpy as np
from matplotlib import pyplot as plt
from network import Network
from node import *
from proposal import *

# Set simulation parameters
nsamples = 1000
ndata = 100

# Create hyper nodes
alarm_s1 = BetaNode(1, 1, NormalProposal(0.02))
alarm_s2 = BetaNode(1, 1, NormalProposal(0.02))
alarm_s3 = BetaNode(1, 1, NormalProposal(0.02))
alarm_s4 = BetaNode(1, 1, NormalProposal(0.02))
burglary_s1 = BetaNode(1, 1, NormalProposal(0.02))
earthquake_s1 = BetaNode(1, 1, NormalProposal(0.02))
john_s1 = BetaNode(1, 1, NormalProposal(0.02))
john_s2 = BetaNode(1, 1, NormalProposal(0.02))
mary_s1 = BetaNode(1, 1, NormalProposal(0.02))
mary_s2 = BetaNode(1, 1, NormalProposal(0.02))

# Add nodes to probability network
network = Network(5000, 100)
network.add_nodes([alarm_s1, alarm_s2, alarm_s3, alarm_s4])
network.add_node(burglary_s1)
network.add_node(earthquake_s1)
network.add_nodes([john_s1, john_s2])
network.add_nodes([mary_s1, mary_s2])

# Load in data and create nodes
#data = np.load('../data/alarm_modified.npy')[0:ndata]
data = np.load('../data/alarm_missing.npy')[0:ndata]
for datum in data:
    
    # Dreate nodes and add to network
    burglary = BernoulliNode([], [burglary_s1])
    earthquake = BernoulliNode([], [earthquake_s1])
    alarm = BernoulliNode([burglary, earthquake], 
            [None, None, None, alarm_s1, alarm_s2, alarm_s3, alarm_s4])
    john = BernoulliNode([alarm], [None, john_s1, john_s2])
    mary = BernoulliNode([alarm], [None, mary_s1, mary_s2])

    # Add children to data nodes
    burglary.add_child(alarm)
    earthquake.add_child(alarm)
    alarm.add_children([john, mary])

    # Add children to probability nodes
    alarm_s1.add_child(alarm)
    alarm_s2.add_child(alarm)
    alarm_s3.add_child(alarm)
    alarm_s4.add_child(alarm)
    burglary_s1.add_child(burglary)
    earthquake_s1.add_child(earthquake)
    john_s1.add_child(john)
    john_s2.add_child(john)
    mary_s1.add_child(mary)
    mary_s2.add_child(mary)

    # Set nodes as fixed according to data
    if np.isfinite(datum[0]):
        burglary.set_fixed(datum[0])
    if np.isfinite(datum[1]):
        earthquake.set_fixed(datum[1])
    if np.isfinite(datum[2]):
        alarm.set_fixed(datum[2])
    if np.isfinite(datum[3]):
        john.set_fixed(datum[3])
    if np.isfinite(datum[4]):
        mary.set_fixed(datum[4])

    # Add nodes to probability network
    network.add_nodes([burglary, earthquake, alarm, john, mary])

# Run simulation
network.burn()
network.sample(nsamples)

# Get data from network
samples = np.array(network.samples)
alarm_s1_samples = samples[:,0]
alarm_s2_samples = samples[:,1]
alarm_s3_samples = samples[:,2]
alarm_s4_samples = samples[:,3]
burglary_s1_samples = samples[:,4]
earthquake_s1_samples = samples[:,5]
john_s1_samples = samples[:,6]
john_s2_samples = samples[:,7]
mary_s1_samples = samples[:,8]
mary_s2_samples = samples[:,9]

# Compute statistics from network data
alarm_s1_mean = np.mean(alarm_s1_samples)
alarm_s2_mean = np.mean(alarm_s2_samples)
alarm_s3_mean = np.mean(alarm_s3_samples)
alarm_s4_mean = np.mean(alarm_s4_samples)
burglary_s1_mean = np.mean(burglary_s1_samples)
earthquake_s1_mean = np.mean(earthquake_s1_samples)
john_s1_mean = np.mean(john_s1_samples)
john_s2_mean = np.mean(john_s2_samples)
mary_s1_mean = np.mean(mary_s1_samples)
mary_s2_mean = np.mean(mary_s2_samples)

# Print statistics
print('Estimated Alarm TT:', alarm_s1_mean)
print('Estimated Alarm TF:', alarm_s2_mean)
print('Estimated Alarm FT:', alarm_s3_mean)
print('Estimated Alarm FF:', alarm_s4_mean)
print('Estimated Burgulary:', burglary_s1_mean)
print('Estimated Earthquake:', earthquake_s1_mean)
print('Estimated John T:', john_s1_mean)
print('Estimated John F:', john_s2_mean)
print('Estimated Mary T:', mary_s1_mean)
print('Estimated Mary F:', mary_s2_mean)

# Plot data for alarm hyper-nodes
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(18,6))
ax1.hist(alarm_s1_samples, bins=np.arange(0,1.05,0.05), 
        normed=True, label='posterior')
ax1.plot([0, 1], [1, 1], label='Prior')
ax1.plot(0.95, 1, 'oy', label='Ture')
ax1.plot(alarm_s1_mean, 1, 'or', label='Estimated')
ax1.set_title('Alarm Hyper TT')
ax2.hist(alarm_s2_samples, bins=np.arange(0,1.05,0.05), 
        normed=True, label='posterior')
ax2.plot([0, 1], [1, 1], label='Prior')
ax2.plot(0.94, 1, 'oy', label='Ture')
ax2.plot(alarm_s2_mean, 1, 'or', label='Estimated')
ax2.set_title('Alarm Hyper TF')
ax3.hist(alarm_s3_samples, bins=np.arange(0,1.05,0.05), 
        normed=True, label='posterior')
ax3.plot([0, 1], [1, 1], label='Prior')
ax3.plot(0.29, 1, 'oy', label='Ture')
ax3.plot(alarm_s3_mean, 1, 'or', label='Estimated')
ax3.set_title('Alarm Hyper FT')
ax4.hist(alarm_s4_samples, bins=np.arange(0,1.05,0.05), 
        normed=True, label='posterior')
ax4.plot([0, 1], [1, 1], label='Prior')
ax4.plot(0.001, 1, 'oy', label='Ture')
ax4.plot(alarm_s4_mean, 1, 'or', label='Estimated')
ax4.set_title('Alarm Hyper FF')
#plt.savefig('../img/learning/alarm_node_100.png', dpi=40)
plt.savefig('../img/learning/alarm_missing_alarm.png', dpi=40)

# Plot data for other hyper-nodes
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,6))
ax1.hist(burglary_s1_samples, bins=np.arange(0,1.05,0.05), 
        normed=True, label='posterior')
ax1.plot([0, 1], [1, 1], label='Prior')
ax1.plot(0.001, 1, 'oy', label='Ture')
ax1.plot(burglary_s1_mean, 1, 'or', label='Estimated')
ax1.set_title('Burglary')
ax2.hist(john_s2_samples, bins=np.arange(0,1.05,0.05), 
        normed=True, label='posterior')
ax2.plot([0, 1], [1, 1], label='Prior')
ax2.plot(0.05, 1, 'oy', label='Ture')
ax2.plot(john_s2_mean, 1, 'or', label='Estimated')
ax2.set_title('John F')
ax3.hist(mary_s1_samples, bins=np.arange(0,1.05,0.05), 
        normed=True, label='posterior')
ax3.plot([0, 1], [1, 1], label='Prior')
ax3.plot(0.7, 1, 'oy', label='Ture')
ax3.plot(mary_s1_mean, 1, 'or', label='Estimated')
ax3.set_title('Mary T')
#plt.savefig('../img/learning/alarm_nodes_various_100.png', dpi=40)
plt.savefig('../img/learning/alarm_missing_various.png', dpi=40)

# Plot burn-in (for verification purposes only)
mixing = np.array(network.sample_history)
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(18,6))
ax1.plot(mixing[:,0])
ax2.plot(mixing[:,1])
ax3.plot(mixing[:,2])
ax4.plot(mixing[:,3])
plt.savefig('../img/tmp/alarm_burn.png', dpi=40)

# Plot mixing (for verification purposes only)
burn = np.array(network.burn_history)
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(18,6))
ax1.plot(burn[:,0])
ax2.plot(burn[:,1])
ax3.plot(burn[:,2])
ax4.plot(burn[:,3])
plt.savefig('../img/tmp/alarm_mixing.png', dpi=40)
