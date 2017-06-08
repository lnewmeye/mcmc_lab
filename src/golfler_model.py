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

# Get file path for golfer database
folder_name = '..' + os.sep + 'data'
file_name = 'golfdataR.dat'
file_path = os.path.join(folder_name, file_name)

# Read in data

# Create hyper nodes for network
hyperobsvar = InvGammaNode(83, 1/0.0014, NormalProposal(0.002))
hypergolfervar = InvGammaNode(18, 1/0.015, NormalProposal(0.002))
hypertourmean = NormalNode(72, 2, NormalProposal(0.005))
hypertourvar = InvGammaNode(18, 1/0.015, NormalProposal(0.002))

# Create golfer, tournament, and observation nodes
# Set obervation nodes as fixed
# Add each to list
# Add as observations as children to golfer and tour

#prior_mean = NormalNode(5, 1/9, NormalProposal(0.005))
#prior_variance = InvGammaNode(11, 2.5, NormalProposal(0.002))

# Add nodes as children

# Add all nodes to network

# Burn off and sample

# Plot burn in of prior_mean

# Plot mixing of prior_mean

# Plot burn in of prior_variance

# Plot mixing of prior_variance

# Return estimates
