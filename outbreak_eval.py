from collections import defaultdict
from itertools import compress
import numpy as np
import random

# function to simulate spread with temporal BFS
def bfs_temp(adj, seed, date, p, recovery):
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

# function to compute degree of nodes
def create_eval_data(adj, nodes, eval_p, eval_recovery, eval_size, eval_date_monitoring, eval_length_monitoring, min_outbreak_size=0):
    # cut-off date: only nodes that were activated later will still be active
    cutoff = eval_date_monitoring - eval_recovery
    # empty dict for results
    out = defaultdict(list)    
    # loop as long as the length of the output is not nsim
    while len(out) < eval_size:
        # randomly pick a seed node
        seed = random.choice(nodes)
        # select starting date randomly
        seed_date = random.choice(list(range(eval_date_monitoring - eval_length_monitoring, eval_date_monitoring)))
        # simulate from seed configuration
        sim = bfs_temp(adj, seed, seed_date, eval_p, eval_recovery)
        # keep only nodes that are still active at monitoring date
        sim = list(set([i[0] for i in sim if i[1] >= cutoff]))
        # if we set a min_outbreak_size, make sure given run satisfies condition
        # IMPORTANT: if recovery time is very short, simulations can run for a long time with min_outbreak_size > 0
        if len(sim) >= min_outbreak_size:
            out[(seed, seed_date)] = sim
    return out

