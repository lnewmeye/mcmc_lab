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

# Create hyper nodes for network
observation_var = InvGammaNode(83, 1/0.0014, NormalProposal(0.01))
golfer_var = InvGammaNode(18, 1/0.015, NormalProposal(0.01))
tour_mean = NormalNode(72, 2, NormalProposal(0.01))
tour_var = InvGammaNode(18, 1/0.015, NormalProposal(0.015))

# Create structures to store golfer, tournament and observation nodes
golfers = {}
tours = {}
observations = []

# Get file path for golfer database
folder_name = '..' + os.sep + 'data'
file_name = 'golfdataR.dat'
file_path = os.path.join(folder_name, file_name)

#prior_mean = NormalNode(5, 1/9, NormalProposal(0.005))
#prior_variance = InvGammaNode(11, 2.5, NormalProposal(0.002))
# Read in data and create golfer, tournament, and observation nodes and link
data = [line.split() for line in open(file_path)]
for entry in data:

    # Get values from data entry
    name = entry[0]
    score = float(entry[1])
    number = float(entry[2])

    # Make golfer node (if not already created)
    if name not in golfers:
        golfer = NormalNode(0, golfer_var, NormalProposal(0.02))
        golfer_var.add_child(golfer)
        golfers[name] = golfer

    # Make tour node (if not already created)
    if number not in tours:
        tour = NormalNode(tour_mean, tour_var, NormalProposal(0.002))
        tour_mean.add_child(tour)
        tour_var.add_child(tour)
        tours[number] = tour

    # Create observation node and add as child to tour and golfer
    observation = NormalNodeSum(golfers[name], tours[number], 
            observation_var, NormalProposal(0.002))
    observation_var.add_child(observation)
    golfers[name].add_child(observation)
    tours[number].add_child(observation)
    observation.set_fixed(score)

# Create network and add nodes
network = Network(10, 2) #TODO: Make sure to change this back to 200 or so
network.add_node(observation_var)
network.add_node(golfer_var)
network.add_node(tour_mean)
network.add_node(tour_var)
[network.add_node(golfers[name]) for name in golfers]
[network.add_node(tours[number]) for number in tours]
network.add_nodes(observations)

# Burn off and sample
network.burn(700)

# Get network data
burn_history = np.array(network.burn_history)

# Plot history for various nodes
plt.plot(burn_history[:,0])
plt.title('observation_var')
plt.savefig('../img/observation_var.png')
plt.clf()
plt.plot(burn_history[:,1])
plt.title('golfer_var')
plt.savefig('../img/golfer_var.png')
plt.clf()
plt.plot(burn_history[:,2])
plt.title('tour_mean')
plt.savefig('../img/tour_mean.png')
plt.clf()
plt.plot(burn_history[:,3])
plt.title('tour_var')
plt.savefig('../img/tour_var.png')
plt.clf()
plt.plot(burn_history[:,5])
plt.title('golfer1')
plt.savefig('../img/golfer1.png')
plt.clf()
plt.plot(burn_history[:,6])
plt.title('golfer2')
plt.savefig('../img/golfer2.png')
plt.clf()
plt.plot(burn_history[:,7])
plt.title('golfer3')
plt.savefig('../img/golfer3.png')
plt.clf()
plt.plot(burn_history[:,4+len(golfers),+3])
plt.title('tour1')
plt.savefig('../img/tour1.png')
plt.clf()
plt.plot(burn_history[:,4+len(golfers),+4])
plt.title('tour2')
plt.savefig('../img/tour2.png')
plt.clf()
plt.plot(burn_history[:,4+len(golfers),+5])
plt.title('tour3')
plt.savefig('../img/tour3.png')
plt.clf()
plt.plot(burn_history[:,-1])
plt.title('oberved1')
plt.savefig('../img/observed1.png')
plt.clf()
