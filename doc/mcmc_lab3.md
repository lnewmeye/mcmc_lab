# MCMC Part 3: Learning

## Faculty Learning

The following plots show the joint distribution of the parameters for mean and variance in the Faculty Evaluations Model as hyper-parameters are added. The initial figure shows the joint disbritution with no hyper-parameters. The figure after shows hyper-parameters being added in the following order: mean-mean, mean-variance, variance-alpha, variance-beta. The hyper-parameters used have the following fixed parameters

- Mean-Mean: Normal(5, 1.5)
- Mean-Variance: Inverse Gamma(alpha=2, beta=1/9)
- Variance-Alpha:
- Variance-Beta:

~~Add axis labels and title~~
![Joint Distribution - No Hyper-parameters](../img/learning/faculty_joint_none.png)

~~Add axis labels and title~~
![Joint Distribution - Hyper-parameterrs](../img/learning/faculty_joint_hyper.png)

The histograms of added hyper-parameters trent to become slightly more spread out than the original histogram. The fixed parameters used in the hyper-parameters were chosen to have a means that mimic the previous mean and variance. If instead more "off" fixed parameters are chosen for the hyper-parameters The following results as they are added one-by-one.

~~Add axis labels and title~~
![Joint Distribution - Off Hyper-parameters](../img/learning/faculty_joint_off.png)

~~Results from 'off' hyper-parameters~~

~~Report on how distributions are affected~~

~~Test using more hyper-parameters?~~

~~Remeber to increase run parameters before runing final simulation~~

Interesting things to show:
- Eliminating data from the model
- Adding additional, unobserved, nodes to see how results change
- Add parent nodes and watch how they learn
	- What to look for?
	- Maybe watch for how estimates of mean and variance are affected

## Alarm Learning

Steps to completion:
- Change probabilities and produce data (in new file: alarm_data.py)
- Modify alarm code to create nodes based on data (in new file: alarm_learning.py)
- 
