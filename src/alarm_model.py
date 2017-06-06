# CS 677 - Baysian Methods in CS
# MCMC Labs (parts kept in revisions)
# Luke Newmeyer

import numpy as np
from network import Network
from node import *

# Set simulation parameters
N = 2000

# Create nodes in order of heiarchy
burglary = BernoulliNode([], [0.001])
earthquake = BernoulliNode([], [0.002])
alarm = BernoulliNode([burglary, earthquake], 
        [None, None, None, 0.95, 0.94, 0.29, 0.001])
john = BernoulliNode([alarm], [None, 0.9, 0.05])
mary = BernoulliNode([alarm], [None, 0.7, 0.01])

# Add children to nodes
burglary.add_child(alarm)
earthquake.add_child(alarm)
alarm.add_children([john, mary])

# Add nodes to probability network
network = Network(5000, 100)
network.add_nodes([burglary, earthquake, alarm, john, mary])

# Simulate Russell and Norving's conclusion
john.set_fixed(True)
mary.set_fixed(True)
network.burn()
network.sample(N)
probability = network.estimate_probability([1, None, None, None, None])
print('P(Burglary=true|John=true,Mary=true) =', probability)

# Simulate Alarm given Mary and John (partially completed already)
probability = network.estimate_probability([None, None, 1, None, None])
print('P(Alarm=true|John=true,Mary=true) =', probability)

# Simulate Earthquake given Mary and John (partially completed already)
probability = network.estimate_probability([None, 1, None, None, None])
print('P(Earthqake=true|John=true,Mary=true) =', probability)

# Simulate Burglary given given not Mary and not John
john.set_fixed(False)
mary.set_fixed(False)
network.burn()
network.sample(N)
probability = network.estimate_probability([1, None, None, None, None])
print('P(Burglary=true|John=false,Mary=false) =', probability)

# Simulate Burglary given given John and not Mary
john.set_fixed(True)
mary.set_fixed(False)
network.burn()
network.sample(N)
probability = network.estimate_probability([1, None, None, None, None])
print('P(Burglary=true|John=true,Mary=false) =', probability)

# Simulate Burglary given given John
john.set_fixed(True)
mary.set_unknown()
network.burn()
network.sample(N)
probability = network.estimate_probability([1, None, None, None, None])
print('P(Burglary=true|John=true) =', probability)

# Simulate Burglary given given John and not Mary
john.set_unknown()
mary.set_fixed(True)
network.burn()
network.sample(N)
probability = network.estimate_probability([1, None, None, None, None])
print('P(Burglary=true|Mary=true) =', probability)
