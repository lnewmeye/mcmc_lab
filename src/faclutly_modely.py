# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

# Import required modules
import numpy as np
import os

# Read in faculty data
folder_name = '..' + os.sep + 'data'
file_name = 'faculty.dat'
file_path = os.path.join(folder_name, file_name)
data = np.genfromtxt(file_path)

