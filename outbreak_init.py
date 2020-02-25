# prepare edgelist
def prepare_edgelist(edgelist, date_monitoring, length_monitoring):
    return [e for e in edgelist if e[2] >= (date_monitoring - length_monitoring) if e[2] <= date_monitoring]

# find all unique ids in monitoring period
def find_nodes(edgelist): 
    # get only nodes
    out = [[e[0], e[1]] for e in edgelist]
    # flatten list
    out = sorted(list(set([item for sublist in out for item in sublist])))
    # return output
    return out
    
# create adjacency dict
def build_adjacency_dict(edgelist, is_directed=False):
    # empty dict
    adj = {}
	# find all nodes
    nodes = find_nodes(edgelist)
    # procedure for undirected
    if(is_directed==False):
        # loop over nodes and add adjacent nodes to dict
        for n in nodes:
            edg1 = [(e[1], e[2]) for e in edgelist if e[0] == n]
            edg2 = [(e[0], e[2]) for e in edgelist if e[1] == n]
            adj[n] = edg1 + edg2
    else:
        for n in nodes:
            edg = [(e[1], e[2]) for e in edgelist if e[0] == n]
            adj[n] = edg
    # return output
    return adj