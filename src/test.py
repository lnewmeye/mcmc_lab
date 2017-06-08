# Import required modules
import numpy as np
from matplotlib import pyplot as plt

# Import my classes
from node import *
from network import Network
from proposal import NormalProposal

# Start introductory network (for testing purposes)
proposal = NormalProposal(0.1)
test_node1 = NormalNode(0, 2, proposal)
test_node3 = NormalNode(0, 2, proposal)
test_node2 = NormalNode(test_node1, test_node3, proposal)

print('Mean/Varinace test')
samples = [test_node2.sample_distribution() for i in range(1000)]
print(test_node1.value)
print(np.mean(samples))
print(test_node3.value)
print(np.var(samples))

print('Value test')
print(test_node2.value)
print(test_node2.current_probability())

print('Conditional test')
print(test_node2.value)
print(test_node2.sample_conditional())
print(test_node2.sample_conditional())

print('Metropolis test')
samples = [test_node2.sample_conditional() for i in range(100000)]
print(np.mean(samples))
print(np.var(samples[::10]))

plt.plot(samples)
plt.show()
