

class ProbabilityNode(object):

    def __init__(self, probability, true=None, false=None):
        self.probability = probability
        self.true = true
        self.false = false

    def set_probability(self, probability):
        self.probability = probability

    def get_probability(self):
        return self.probability

    def set_true(self, true):
        self.true = true

    def get_true(self):
        return self.true

    def set_false(self, false):
        self.false = false

    def get_false(self):
        return self.false

    def get_child(self, value):
        if value == True:
            return self.true
        return self.false

class BernoulliTree(object):

    def __init__(self, probabilities):
        ''' Nodes are created by providing a list of probabilities. Only valid
        numbers of probabilities should be given that fit a tree structure
        (i.e. 2^n - 1). The nodes will be inserted as the first node followed
        by the true and false condition of each following node '''

        # Add first node to tree and add to tail list
        node = ProbabilityNode(probabilities.pop(0))
        self.tree = node
        tail_nodes = [node]

        # Iterate through probabilities two at a time and add to tree parents
        probability_iter = iter(probabilities)
        for probability in probability_iter:

            # Create new node, connect to true case of tail, add to tail list
            previous_node = tail_nodes.pop(0)
            true_node = ProbabilityNode(probability)
            previous_node.set_true(true_node)
            tail_nodes.append(true_node)

            # create new node, connect to false case of tail, add to tail list
            false_node = ProbabilityNode(next(probability_iter))
            previous_node.set_false(false_node)
            tail_nodes.append(false_node)

    def get_probability(self, sequence):
        ''' Give the probability of the node following the sequence given '''

        # Traverse tree according to sequence
        node = self.tree
        for value in sequence:
            node = node.get_child(value)

        # Return probability of node at end of sequence
        return node.probability
