import random
import operator
import numpy as np

# function to compute cumulative detection likelihood
def cumulative_probability(sim_ind, list nodes, int length_monitoring, int nsim):
    cdef int norm = len(sim_ind.keys()) * length_monitoring * nsim
    sets = [sim_ind[s] for s in nodes]
    return len(set.union(*sets))/float(norm)

# function to compute marginal detection likelihood
def marginal_probability(sim_ind, covered_sim, node):
    sim_node = sim_ind[node]
    marg_gain = sim_node.difference(covered_sim)
    return marg_gain

# function to greedily optimize
def greedy_max(list nodes, sim_ind, int length_monitoring, int nsensors, int nsim):

    # define variables
    cdef int node
    cdef int v
    cdef int max_val
    cdef list max_keys
    cdef (int, int) new
	
    # initialize counter
    cdef int it = 1
	
    # normalization constant
    cdef int norm = len(sim_ind.keys()) * length_monitoring * nsim
	
    # empty list of optimal observers
    cdef list optimal_observers = []
	
    # empty set for covered simulations
    covered_sim = set()
	
    # dict for marginal gains
    cdef dict marginal_gain_dict = {}
	
    # iterate over all possible nodes and find marginal gain
    for node in nodes:
        marginal_gain_dict[node] = len(marginal_probability(sim_ind, covered_sim, node))
    
    # sort and get list of tuples
    cdef list marginal_gain = sorted(marginal_gain_dict.items(), key=operator.itemgetter(1), reverse=True)

    # print first node to be chosen
    print('Optimal observers:')
    print('{}: {} (marginal increase: {})'.format(it, marginal_gain[0][0], np.round(marginal_gain[0][1]/norm, 4)))
	
    # update counter
    it += 1
	
    # find simulation runs of optimal node
    casc_optimal = sim_ind[marginal_gain[0][0]]
	
    # add to covered_sim
    covered_sim.update(casc_optimal)
	
    # add top node to list of optimal observers
    optimal_observers.append(marginal_gain.pop(0)[0])
	
    # empty list to temporarily store activated nodes
    cdef list active = []
	
    # loop as long as we have not found enough sensors
    while len(optimal_observers) < nsensors:
	
        # get top node from list
        v = marginal_gain.pop(0)[0]
		
        # compute marginal gain
        marg = marginal_probability(sim_ind, covered_sim, v)
		
        # add newly computed marginal gain back to list
        marginal_gain.append((v, len(marg)))
		
        # resort list
        marginal_gain = sorted(marginal_gain, key=lambda tup: tup[1], reverse=True)
		
        # if top node is still the same, then add to optimal set
        if marginal_gain[0][0] == v:
		
            # print chosen node
            print('{}: {} (marginal increase: {})'.format(it, marginal_gain[0][0], np.round(marginal_gain[0][1]/norm, 4)))
			
            # update counter
            it += 1
			
            # update list of covered simulations
            covered_sim.update(marg)
			
            # add top node to list of optimal observers
            optimal_observers.append(marginal_gain.pop(0)[0])
			
            # clear active
            active.clear()
			
        else:
            if v not in active:
			
                # if v is not activated yet, add it to list and continue loop
                active.append(v)
                continue

            else:
                # if v is activated already, get all keys where value is maximal
                max_val = marginal_gain[0][1]
                max_keys = [i for i in marginal_gain if i[1] == max_val]
				
                # randomly select a key from keys with max value
                new = random.choice(max_keys)
					
                # remove chosen key from max_keys and marginal gains list
                marginal_gain.remove(new)
					
                # compute marginal gain
                marg = marginal_probability(sim_ind, covered_sim, new[0])
					
                # update list of covered simulations
                covered_sim.update(marg)
					
                # add node to optimal observers
                optimal_observers.append(new[0])
					
                # print chosen node
                print('{}: {} (marginal increase: {})'.format(it, new[0], np.round(new[1]/float(norm), 4)))
					
                # update counter
                it += 1

                # clear active
                active.clear()

    # return output
    return optimal_observers