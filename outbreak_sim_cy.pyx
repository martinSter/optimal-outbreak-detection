import multiprocessing
import numpy as np
from itertools import compress
from joblib import Parallel, delayed
from collections import defaultdict, Counter, OrderedDict

# function to simulate spread with temporal BFS
def bfs_temp(dict adj, int seed, int date, float p, int recovery):
    # define variables
    cdef list active
    cdef list queue
    cdef list temp
    cdef (int, int) v
    # add seed-date pair to active list and to queue
    active, queue = [(seed, date)], [(seed, date)]
    # continue while queue contains elements
    while queue:
        # empty list for intermediate results
        temp = []
        # take first element in queue
        v = queue.pop(0)
        # add neighbors of v to temp if connection is within active period of v
        temp.extend([i for i in adj[v[0]] if i[1] > v[1] if (i[1] - v[1]) <= recovery if i not in active])
        # random draw for all links in temp
        ind = np.random.uniform(0, 1, len(temp)) < p
        # find newly activated nodes based on random draw
        new_active = list(compress(temp, ind))
        # add newly activated nodes to active and queue
        active.extend(new_active)
        queue.extend(new_active) 
    # return output
    return active

# function to simulate for one date and all nodes
def simulate(dict adj, list nodes, int date, float p, int recovery, int cutoff, int nsim):
    # define variables
    cdef int n
    cdef int i
    cdef list sim_temp
    # empty dict for results
    out = defaultdict(list)
    # loop over all nodes
    for n in nodes:
        # empty list for temporary results
        sim_temp = []
        # simulation nsim times
        for i in range(nsim):
            sim_temp.append(bfs_temp(adj, n, date, p, recovery))
        # keep only nodes that are still active at date of monitoring
        sim_temp = [[j[0] for j in u if j[1] >= cutoff] for u in sim_temp]
        # remove empty sublists
        sim_temp = [l for l in sim_temp if l]
        # add simulation results to dict
        out[(n, date)] = [list(set(l)) for l in sim_temp]
    return out

# simulate spreading
def parallel_simulation(dict adj, list nodes, int date_monitoring, int length_monitoring, float p, int recovery, int nsim):
    # cut-off date: only nodes that were activated later will still be active
    cdef int cutoff = date_monitoring - recovery
    # empty dict for results
    sim_list = defaultdict(list)
    # determine number of (virtual) cores
    cdef int num_cores = multiprocessing.cpu_count()
    # create node-time pairs
    inputs = [[t, nodes] for t in range(date_monitoring - length_monitoring, date_monitoring)]
    # parallel simulations
    processed_list = Parallel(n_jobs=num_cores)(delayed(simulate)(adj, i[1], i[0], p, recovery, cutoff, nsim) for i in inputs)
    # assign to attribute
    for d in processed_list:
        sim_list.update(d)
    # return output
    return sim_list
