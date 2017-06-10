# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

# Import required modules
from matplotlib import pyplot as plt
from scipy.stats import norm
import numpy as np
import os

# Import my classes
from node import *
from network import Network
from proposal import NormalProposal

# Set parameters for simulation
nsamples = 500

# Create hyper nodes for network
observation_var = InvGammaNode(83, 1/0.0014, NormalProposal(0.05))
golfer_var = InvGammaNode(18, 1/0.015, NormalProposal(0.05))
tour_mean = NormalNode(72, 2, NormalProposal(0.04))
tour_var = InvGammaNode(18, 1/0.015, NormalProposal(0.03))

# Create structures to store golfer, tournament and observation nodes
golfers = {}
tours = {}
observations = []

# Get file path for golfer database
folder_name = '..' + os.sep + 'data'
file_name = 'golfdataR.dat'
file_path = os.path.join(folder_name, file_name)

# Read in data and create golfer, tournament, and observation nodes and link
data = [line.split() for line in open(file_path)]
for entry in data:

    # Get values from data entry
    name = entry[0]
    score = float(entry[1])
    number = float(entry[2])

    # Make golfer node (if not already created)
    if name not in golfers:
        golfer = NormalNode(0, golfer_var, NormalProposal(0.3), name=name)
        golfer_var.add_child(golfer)
        golfers[name] = golfer

    # Make tour node (if not already created)
    if number not in tours:
        tour = NormalNode(tour_mean, tour_var, NormalProposal(0.1))
        tour_mean.add_child(tour)
        tour_var.add_child(tour)
        tours[number] = tour

    # Create observation node and add as child to tour and golfer
    observation = NormalNodeSum(golfers[name], tours[number], 
            observation_var, NormalProposal(0.002))
    observation.set_fixed(score)
    observation_var.add_child(observation)
    golfers[name].add_child(observation)
    tours[number].add_child(observation)
    observations.append(observation)

# Create network and add nodes
network = Network(10, 100) #TODO: Make sure to change this back to 200 or so
network.add_node(observation_var)
network.add_node(golfer_var)
network.add_node(tour_mean)
network.add_node(tour_var)
[network.add_node(golfers[name]) for name in golfers]
[network.add_node(tours[number]) for number in tours]
network.add_nodes(observations)

# Burn off and sample
network.burn(2000)
network.sample(nsamples)

# Get golfer data
burn = np.array(network.burn_history).T
mixing = np.array(network.sample_history).T
samples = np.array(network.samples).T

ability = []
for i in range(len(golfers)):

    # Get samples for golfer
    golfer_samples = samples[4+i]
    golfer_samples.sort()
    name = network.nodes[4+i].name

    # Get stats from samples
    median = golfer_samples[nsamples/2] 
    low = golfer_samples[int(.05 * nsamples)]
    high = golfer_samples[int(.95 * nsamples)]
    ability.append( (name, low, median, high) )

ability.sort(key=lambda x: x[2])
out_file = open('../out/golfers.txt', 'w')
i = 1
for name, low, median, high in ability:
    print('%d: %s %f; 90%% interval: (%f, %f)' % (i, name, median, low, high))
    #out_file.write('%d: %s %f; 90%% interval: (%f, %f)\n' % (i, name, median, low, high))#TODO: Coment out by defaul
    i += 1

# Plot hyper-parameter burn plots
observation_var_burn = burn[0]
golfer_var_burn = burn[1]
tour_mean_burn = burn[2]
tour_var_burn = burn[3]
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(18,6))
ax1.plot(observation_var_burn)
ax1.set_title('Observation Variance Burn')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(golfer_var_burn)
ax2.set_title('Golfer Variance Burn')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
ax3.plot(tour_mean_burn)
ax3.set_title('Tour Mean Burn')
ax3.set_xlabel('Sample')
ax3.set_ylabel('Sample Value')
ax4.plot(tour_var_burn)
ax4.set_title('Tour Variance Burn')
ax4.set_xlabel('Sample')
ax4.set_ylabel('Sample Value')
#plt.savefig('../img/golfer/hyper_burn.png', dpi=40)#TODO: Coment out by defaul

# Plot hyper-parameter mixing plots
observation_var_mixing = mixing[0]
golfer_var_mixing = mixing[1]
tour_mean_mixing = mixing[2]
tour_var_mixing = mixing[3]
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(18,6))
ax1.plot(observation_var_mixing)
ax1.set_title('Observation Variance Mixing')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(golfer_var_mixing)
ax2.set_title('Golfer Variance Mixing')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
ax3.plot(tour_mean_mixing)
ax3.set_title('Tour Mean Mixing')
ax3.set_xlabel('Sample')
ax3.set_ylabel('Sample Value')
ax4.plot(tour_var_mixing)
ax4.set_title('Tour Variance Mixing')
ax4.set_xlabel('Sample')
ax4.set_ylabel('Sample Value')
#plt.savefig('../img/golfer/hyper_mixing.png', dpi=40)#TODO: Coment out by defaul

# Plot Golfer mixed plot
golfer_burn = np.array([burn[4], burn[4+155], burn[4+604-1]]).T
golfer_mixing = np.array([mixing[4], mixing[4+155], mixing[4+604-1]]).T
golfer_samples = np.array([samples[4], samples[4+155], samples[4+604-1]]).T
golfer_range = np.arange(-4, 4, 0.01)
golfer_density = norm.pdf(golfer_range, 0, (1/0.015)/(18-1))
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,6))
ax1.plot(golfer_burn)
ax1.set_title('Burn for 3 Golfers')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(golfer_mixing)
ax2.set_title('Mixing for 3 Golfers')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
ax3.hist(golfer_samples, bins=15, normed=True)
ax3.plot(golfer_range, golfer_density)
ax3.set_title('Density/Histogram for 3 Golfers')
ax3.set_xlabel('Golfer Average')
ax3.set_ylabel('Density')
#plt.savefig('../img/golfer/golfer_subplot.png', dpi=40)#TODO: Coment out by defaul

# Plot tournamnt mixed plot
tour_burn = np.array([burn[4+604], burn[4+604+35], burn[4+604+40-2]]).T
tour_mixing = np.array([mixing[4+604], mixing[4+604+35], mixing[4+604+40-2]]).T
tour_samples = np.array([samples[4+604], samples[4+604+35], samples[4+604+40-2]]).T
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,6))
ax1.plot(tour_burn)
ax1.set_title('Burn for 3 Tournaments')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Sample Value')
ax2.plot(tour_mixing)
ax2.set_title('Mixing for 3 Tournaments')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Sample Value')
ax3.hist(tour_samples, bins=15, normed=True)
ax3.set_title('Histogram for 3 Tournaments')
ax3.set_xlabel('Tour Average')
ax3.set_ylabel('Density')
#plt.savefig('../img/golfer/tour_subplot.png', dpi=40)#TODO: Coment out by defaul
