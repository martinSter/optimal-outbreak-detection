from collections import defaultdict, Counter, OrderedDict

# create inverted index
def create_index(sim_list):
    # create empty dict
    index = defaultdict(set)
    # get flat list of values
    sim_flat = [item for sublist in list(sim_list.values()) for item in sublist]
    # enumerate simulations and loop over them
    for i, nodes in enumerate(sim_flat):
        for n in nodes:
            index[n].add(i)
    # return output
    return index

# create inverted index by source (for source detection)
def create_index_by_source(sim_list):
    # create empty dict
    index = defaultdict(dict)
    # loop over sim_list
    for key, value in sim_list.items():
        # empty dict for temporary results
        temp = defaultdict(set)
        # enumerate simulations and loop over them
        for i, nodes in enumerate(value):
            for n in nodes:
                temp[n].add(i)
        # add to dict
        index[key] = temp
    # return output
    return index
