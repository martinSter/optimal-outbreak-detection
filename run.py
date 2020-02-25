#!/usr/bin/env python3

# import modules
import time
import pickle
import numpy as np
import pandas as pd

import outbreak_init
import outbreak_sim_cy
import outbreak_index
import outbreak_greedy_cy
import outbreak_source

import argparse
parser = argparse.ArgumentParser(description='Outbreak detection for escort data')
parser.add_argument('input', help='input CSV path')
parser.add_argument('output1', help='output path')
parser.add_argument('output2', help='output path')
args = parser.parse_args()

# Gather our code in a main() function
def main():
    # save starting time
    start = time.time()
    
    # 1. import and prepare data
    df = pd.read_csv(args.input, sep=';', header=None, skiprows=24)
    # set column names
    df.columns = ['idf','idm','date','grade','an','or','mo']
    # create a list with tuples
    subset = df[['idf', 'idm', 'date']]
    edgelist_full = [tuple(x) for x in subset.values]
    # sort the list of movements by date
    edgelist_full = sorted(edgelist_full, key = lambda x: x[2])
    
    # 2. set parameters
    # date of monitoring
    date_monitoring = 2232
    # length of monitoring window (days)
    length_monitoring = 90
    # number of simulations per seed configuration
    nsim = 1000
    # probability of infection in SIR process
    p = 0.6
    # length of recovery period (days)
    recovery = 100

    # 3. run outbreak detection
    # reduce edgelist
    edgelist = outbreak_init.prepare_edgelist(edgelist_full, date_monitoring, length_monitoring)
    # get all nodes as list
    nodes = outbreak_init.find_nodes(edgelist)
    # determine number of sensors
    nsensors = len(nodes)
    # build adjacency dict
    adj = outbreak_init.build_adjacency_dict(edgelist, is_directed=False)
    # simulate
    sim_list = outbreak_sim_cy.parallel_simulation(adj, nodes, date_monitoring, length_monitoring, p, recovery, nsim)
    # create inverted index of simulation results
    sim_ind = outbreak_index.create_index(sim_list)
    # greedy maximization
    optimal_observers = outbreak_greedy_cy.greedy_max(nodes, sim_ind, length_monitoring, nsensors, nsim)

    # 4. compute expected detection likelihood
    eval_expected_prob = [0]
    for ns in range(20, nsensors, 20):
        eval_expected_prob.append(outbreak_greedy_cy.cumulative_probability(sim_ind, optimal_observers[0:ns], length_monitoring, nsim))

    # 5. export
    pickle.dump(optimal_observers, open(args.output1, "wb"))
    pickle.dump(eval_expected_prob, open(args.output2, "wb"))

    # save end time and print total time of procedure
    end = time.time()
    print('Total running time is {}'.format(end - start))

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
