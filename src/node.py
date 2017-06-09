# CS 677 - Baysian Methods in CS
# MCMC Labs Node class
# Luke Newmeyer

''' 
Instructions for use:
1. Create nodes in order of heiarchy. Each distribution requires that the
   parent nodes be given
2. In the case that the node has a defined complete conditional, the
   appropriate function should be called to initalize the conditional
'''

from scipy import stats
from scipy.special import gammaln
from bernoullitree import *
import numpy as np

class Node(object):

    def __init__(self, value=None, fixed=False):

        # Define object attributes
        self.fixed = fixed
        self.children = []
        self.likelihood = None

        # Initialize value if no value passed
        if value == None:
            # Initialize randomly from distribution
            self.value = self.sample_distribution()
        else:
            # Set value to value provided to init function
            self.value == value

    def set_fixed(self, value):
        self.value = value
        self.fixed = True

    def set_unknown(self):
        self.fixed = False

    def add_child(self,  child):
        self.children.append(child)

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def sample_conditional(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Compute likelihood (if first iteration)
        self.likelihood = self.current_likelihood() #TODO: Remove this and adjust to user previous value
        for child in self.children:
            self.likelihood += child.current_likelihood()
        #print('self.likelihood =', self.likelihood)
        #self.probability = self.current_probability() #TODO: Remove this and adjust to user previous value
        #for child in self.children:
            #self.probability += child.current_probability()
        #print('self.probability =', self.probability)

        # Get proposed value from proposal distribution and find probability
        previous_value = self.value
        self.value = self.proposal.sample(previous_value)
        #new_probability = self.current_probability()
        #if new_probability < 0.0:
            #for child in self.childern:
                #new_probability *= child.current_probability()
        new_likelihood = self.current_likelihood()
        if np.isfinite(new_likelihood):

            # Iterate through children and compute running product
            for child in self.children:
                #print('\tnew_acceptance =', new_likelihood)
                new_likelihood += child.current_likelihood()
            #print('new_probability =', new_probability)
            #print('new_likelihood =', new_likelihood)

            #print('difference =', new_likelihood - self.likelihood)
            alpha = np.exp(new_likelihood - self.likelihood)
            #print('old_alpha =', new_probability / self.probability)
            #print('alpha =', alpha)
            self.likelihood = new_likelihood

            # Find new value based on Metropolis algorithm
            if alpha < 1.0:
                if stats.bernoulli.rvs(alpha) == 0:
                    self.value = previous_value

        else:
            #print('value not finite:', new_likelihood)
            self.value = previous_value

        # Compute likelihood ratio (alpha) from new and previous proportions
        #print('new_likelihood =', new_likelihood)
        #print('self.likelihood =', self.likelihood)

        #print('Alpha:', alpha)
        #print('self.value =', self.value)
        #print('previous_value =', previous_value)
        return self.value



class NormalNode(Node):

    def __init__(self, mean, variance, proposal, value=None, fixed=False):
        ''' Initialize object given mean and variance nodes or numbers '''

        # Create dictionary for parents
        self.parents = {}

        # Check if mean is object or value and set appropriately
        if isinstance(mean, Node):
            self.parents['mean'] = mean
        else:
            self.mean = mean
        self.original_mean = mean

        # Check if variance is object or value and set appropriately
        if isinstance(variance, Node):
            self.parents['variance'] = variance
        else:
            self.variance = variance
        self.original_variance = variance

        # Save proposal distribution to object
        self.proposal = proposal

        # Call super node's init function
        super(NormalNode, self).__init__(value, fixed)

    def current_likelihood(self):

        # Get mean and variance from parents (if they exist)
        if 'mean' in self.parents:
            self.mean = self.parents['mean'].value
        if 'variance' in self.parents:
            self.variance = self.parents['variance'].value

        likelihood = -1/2 * (np.log(self.variance) + \
                (self.value - self.mean)**2 / self.variance)
        return likelihood

    def current_probability(self):

        # Get mean and variance from parents (if they exist)
        if 'mean' in self.parents:
            self.mean = self.parents['mean'].value
        if 'variance' in self.parents:
            self.variance = self.parents['variance'].value

        # Find probability for current value with current mean and variance
        #print('\t\tself.varinace =', self.variance)
        #print('\t\tnp.sqrt(self.varinace) =', np.sqrt(self.variance))
        probability = stats.norm.pdf(self.value, self.mean, 
                np.sqrt(self.variance))
        return probability

    def sample_distribution(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Get mean and variance from parents (if they exist)
        if 'mean' in self.parents:
            self.mean = self.parents['mean'].value
        if 'variance' in self.parents:
            self.variance = self.parents['variance'].value

        # Sample distribution for given mean and variance
        self.value = stats.norm.rvs(self.mean, np.sqrt(self.variance))
        return self.value

    def probability_density(self, linspace):
        return stats.norm.pdf(linspace, self.original_mean, 
                np.sqrt(self.original_variance))



class GammaNode(Node):

    def __init__(self, alpha, beta, proposal, value=None, fixed=False):
 
        # Create dictionary for parents
        self.parents = {}

        # Check if alpha is object or value and set appropriately
        if isinstance(alpha, Node):
            self.parents['alpha'] = alpha
        else:
            self.alpha = alpha
        self.original_alpha = alpha

        # Check if beta is object or value and set appropriately
        if isinstance(beta, Node):
            self.parents['beta'] = beta
        else:
            self.beta = beta
        self.original_beta = beta

        # Save proposal distribution to object
        self.proposal = proposal

        # Call super node's init function
        super(GammaNode, self).__init__(value, fixed)

    def current_likelihood(self):

        # Get alpha and beta from parents (if they exist)
        if 'alpha' in self.parents:
            self.alpha = self.parents['alpha'].value
        if 'beta' in self.parents:
            self.beta = self.parents['beta'].value

        # Find probability for current value with current mean and variance
        likelihood = self.alpha * np.log(self.beta) - gammaln(self.alpha) + \
                (self.alpha + 1) * np.log(self.value) - self.beta * self.value
        return likelihood

    def current_probability(self):

        # Get alpha and beta from parents (if they exist)
        if 'alpha' in self.parents:
            self.alpha = self.parents['alpha'].value
        if 'beta' in self.parents:
            self.beta = self.parents['beta'].value

        # Find probability for current value with current mean and variance
        probability = stats.gamma.pdf(self.value, self.alpha,
                scale=1/self.beta)
        return probability

    def sample_distribution(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Get alpha and beta from parents (if they exist)
        if 'alpha' in self.parents:
            self.alpha = self.parents['alpha'].value
        if 'beta' in self.parents:
            self.beta = self.parents['beta'].value

        # Sample distribution for given mean and variance
        self.value = stats.gamma.rvs(self.alpha, scale=1/self.beta)
        return self.value

    def probability_density(self, linspace):
        return stats.gamma.pdf(linspace, self.original_alpha, 
                scale=1/self.original_beta)



class InvGammaNode(Node):

    def __init__(self, alpha, beta, proposal, value=None, fixed=False):

        # Create dictionary for parents
        self.parents = {}

        # Check if alpha is object or value and set appropriately
        if isinstance(alpha, Node):
            self.parents['alpha'] = alpha
        else:
            self.alpha = alpha
        self.original_alpha = alpha

        # Check if beta is object or value and set appropriately
        if isinstance(beta, Node):
            self.parents['beta'] = beta
        else:
            self.beta = beta
        self.original_beta = beta

        # Save proposal distribution to object
        self.proposal = proposal

        # Call super node's init function
        super(InvGammaNode, self).__init__(value, fixed)

    def current_likelihood(self):

        # Get alpha and beta from parents (if they exist)
        if 'alpha' in self.parents:
            self.alpha = self.parents['alpha'].value
        if 'beta' in self.parents:
            self.beta = self.parents['beta'].value

        # Find probability for current value with current mean and variance
        likelihood = self.alpha * np.log(self.beta) - gammaln(self.alpha) - \
                (self.alpha + 1) * np.log(self.value) - self.beta / self.value
        return likelihood

    def current_probability(self):

        # Get alpha and beta from parents (if they exist)
        if 'alpha' in self.parents:
            self.alpha = self.parents['alpha'].value
        if 'beta' in self.parents:
            self.beta = self.parents['beta'].value

        # Find probability for current value with current mean and variance
        probability = stats.invgamma.pdf(self.value, self.alpha,
                scale=self.beta)
        return probability

    def sample_distribution(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Get alpha and beta from parents (if they exist)
        if 'alpha' in self.parents:
            self.alpha = self.parents['alpha'].value
        if 'beta' in self.parents:
            self.beta = self.parents['beta'].value

        # Sample distribution for given mean and variance
        self.value = stats.invgamma.rvs(self.alpha, scale=self.beta)
        return self.value

    def probability_density(self, linspace):
        return stats.invgamma.pdf(linspace, self.original_alpha, 
                scale=self.original_beta)




class PoissonNode(Node):

    def __init__(self, theta, proposal, value=None, fixed=False):

        # Create dictionary for parents
        self.parents = {}

        # Check if alpha is object or value and set appropriately
        if isinstance(theta, Node):
            self.parents['theta'] = theta
        else:
            self.theta = theta
        self.original_theta = theta

        # Save proposal distribution to object
        self.proposal = proposal

        # Call super node's init function
        super(PoissonNode, self).__init__(value, fixed)

    def current_likelihood(self):

        # Get theta from parent (if it exists)
        if 'theta' in self.parents:
            self.theta = self.parents['theta'].value

        # Find probability for current value with current mean and variance
        likelihood = -self.theta + self.value * np.log(self.theta) - \
                gammaln(self.value + 1)
        return likelihood

    def current_probability(self):

        # Get theta from parent (if it exists)
        if 'theta' in self.parents:
            self.theta = self.parents['theta'].value

        # Find probability for current value with current mean and variance
        probability = stats.poisson.pmf(self.value, self.theta)
        return probability

    def sample_distribution(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Get theta from parent (if it exists)
        if 'theta' in self.parents:
            self.theta = self.parents['theta'].value

        # Sample distribution for given mean and variance
        self.value = stats.poisson.rvs(self.theta)
        return self.value

    def probability_density(self, linspace):
        return stats.poisson.pmf(linspace, self.original_theta)



class BetaNode(Node):

    def __init__(self, alpha, beta, proposal, value=None, fixed=False):

        # Create dictionary for parents
        self.parents = {}

        # Check if alpha is object or value and set appropriately
        if isinstance(alpha, Node):
            self.parents['alpha'] = alpha
        else:
            self.alpha = alpha
        self.original_alpha = alpha

        # Check if beta is object or value and set appropriately
        if isinstance(beta, Node):
            self.parents['beta'] = beta
        else:
            self.beta = beta
        self.original_beta = beta

        # Save proposal distribution to object
        self.proposal = proposal

        # Call super node's init function
        super(BetaNode, self).__init__(value, fixed)

    def current_likelihood(self):

        # Get alpha and beta from parents (if they exist)
        if 'alpha' in self.parents:
            self.alpha = self.parents['alpha'].value
        if 'beta' in self.parents:
            self.beta = self.parents['beta'].value

        # Find probability for current value with current mean and variance
        likelihood = gammaln(self.alpha + self.beta) + \
                (self.alpha - 1) * np.log(self.value) + \
                (self.beta - 1) * np.log(1 - self.value) - \
                gammaln(self.alpha) - gammaln(self.beta)
        return likelihood


    def current_probability(self):

        # Get alpha and beta from parents (if they exist)
        if 'alpha' in self.parents:
            self.alpha = self.parents['alpha'].value
        if 'beta' in self.parents:
            self.beta = self.parents['beta'].value

        # Find probability for current value with current mean and variance
        probability = stats.beta.pdf(self.value, self.alpha, self.beta)
        return probability

    def sample_distribution(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Get alpha and beta from parents (if they exist)
        if 'alpha' in self.parents:
            self.alpha = self.parents['alpha'].value
        if 'beta' in self.parents:
            self.beta = self.parents['beta'].value

        # Sample distribution for given mean and variance
        self.value = stats.beta.rvs(self.alpha, self.beta)
        return self.value

    def probability_density(self, linspace):
        return stats.invgamma.pdf(linspace, self.original_alpha, 
                self.original_beta)



class BernoulliNode(Node):

    # Initalization of object
    def __init__(self, dependencies, probabilities, value=None, fixed=False):
        ''' Initialize object given a list of dependent nodes and a list of 
        probabilities for a tree structure from the dependencies '''

        # Define distribution as a BernoulliTree from the given dependencies
        self.parents = dependencies
        self.distribution = BernoulliTree(probabilities)

        # Call super node's init function
        super(BernoulliNode, self).__init__(value, fixed)

    def current_probability(self):

        # Get value for each dependency and append to array
        parent_values = []
        for parent in self.parents:
            parent_values.append(parent.value)

        # Save sample in object and return
        probability = self.distribution.get_probability(parent_values)
        if self.value == True:
            return probability
        return 1 - probability

    def sample_distribution(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Get probability of distribution
        self.value = True
        probability = self.current_probability()

        # Save sample in object and return
        self.value = stats.bernoulli.rvs(probability)
        return self.value

    def sample_conditional(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Initalize numerator and denominator with current distribution
        self.value = True
        numerator = self.current_probability()
        denominator = 1 - numerator

        # Iterate through children and compute running product
        for child in self.children:

            # Spoof children by setting value to true and compute probability
            self.value = True
            numerator *= child.current_probability()

            # Spoof children by setting value to false and compute probability
            self.value = False
            denominator *= child.current_probability()

        # Find probaility from bayes law
        denominator += numerator
        probability = numerator / denominator

        # Save sample value in object and return
        self.value = stats.bernoulli.rvs(probability)
        return self.value

    # Set complete conditional distribution for object
    def set_conditional(self, dependencies, probabilities):

        # Define conditional as a BernoulliTree from the given dependencies
        self.dependencies = dependencies
        self.conditional = BernoulliTree(probabilities)



class NormalNodeSum(Node):

    def __init__(self, mean1, mean2, variance, proposal, value=None, fixed=False):
        ''' Initialize object given mean and variance nodes or numbers '''

        # Create dictionary for parents
        self.parents = {}

        # Check if mean1 is object or value and set appropriately
        if isinstance(mean1, Node):
            self.parents['mean1'] = mean1
        else:
            self.mean1 = mean1
        self.original_mean1 = mean1

        # Check if mean2 is object or value and set appropriately
        if isinstance(mean2, Node):
            self.parents['mean2'] = mean2
        else:
            self.mean2 = mean2
        self.original_mean2 = mean2

        # Check if variance is object or value and set appropriately
        if isinstance(variance, Node):
            self.parents['variance'] = variance
        else:
            self.variance = variance
        self.original_variance = variance

        # Save proposal distribution to object
        self.proposal = proposal

        # Call super node's init function
        super(NormalNodeSum, self).__init__(value, fixed)

    def current_likelihood(self):

        # Get mean and variance from parents (if they exist)
        if 'mean1' in self.parents:
            self.mean1 = self.parents['mean1'].value
        if 'mean2' in self.parents:
            self.mean2 = self.parents['mean2'].value
        if 'variance' in self.parents:
            self.variance = self.parents['variance'].value

        likelihood = -1/2 * (np.log(self.variance) + \
                (self.value - (self.mean1 + self.mean2))**2 / self.variance)
        return likelihood

    def current_probability(self):

        # Get mean and variance from parents (if they exist)
        if 'mean1' in self.parents:
            self.mean1 = self.parents['mean1'].value
        if 'mean2' in self.parents:
            self.mean2 = self.parents['mean2'].value
        if 'variance' in self.parents:
            self.variance = self.parents['variance'].value

        # Find probability for current value with current mean and variance
        #print('\t\tself.varinace =', self.variance)
        #print('\t\tnp.sqrt(self.varinace) =', np.sqrt(self.variance))
        probability = stats.norm.pdf(self.value, self.mean1 + self.mean2,
                np.sqrt(self.variance))
        return probability

    def sample_distribution(self):

        # If node set to fixed, return value and exit
        if self.fixed == True:
            return self.value

        # Get mean and variance from parents (if they exist)
        if 'mean1' in self.parents:
            self.mean1 = self.parents['mean1'].value
        if 'mean2' in self.parents:
            self.mean2 = self.parents['mean2'].value
        if 'variance' in self.parents:
            self.variance = self.parents['variance'].value

        # Sample distribution for given mean and variance
        self.value = stats.norm.rvs(self.mean1+self.mean2, 
                np.sqrt(self.variance))
        return self.value

    def probability_density(self, linspace):
        return stats.norm.pdf(linspace, self.original_mean1 + \
                self.original_mean2, np.sqrt(self.original_variance))


