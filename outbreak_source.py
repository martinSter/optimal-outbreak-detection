from collections import defaultdict, Counter, OrderedDict

# function to find source likelihoods
def detect_sources(sim_ind_source, evidence, nsim):
    # create empty dict
    out = {}
    # loop over index
    for key, value in sim_ind_source.items():
        # check if nodes in evidence are part of batch of simulations for source
        if set(evidence).issubset(set(value.keys())):
            # empty list of sets
            sets = []
            # find simulation numbers for nodes in evidence
            for s in evidence:
                sets.append(set(value[s]))
            # compute number of simulations in common
            out[key] = len(set.intersection(*sets)) / nsim
        else:
            # if source does not contain evidence nodes, the overlap is 0
            out[key] = 0
    # normalize by total
    out = {k: v / total for total in (sum(out.values()),) for k, v in out.items()}
    # get only key-value pairs where value > 0
    out = {k: v for k, v in out.items() if v > 0}
    # turn them into list and remove dates
    out = [(k[0],v) for k,v in out.items()]
    # empty dict
    out_final = defaultdict(int)
    # add probabilities up over source nodes
    for k, v in out:
        out_final[k] += v
    # return sorted dictionary
    return OrderedDict(sorted(out_final.items(), key=lambda kv: kv[1], reverse=True))