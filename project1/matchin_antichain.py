from typing import List
import copy

def toMatching(leq, S : List):
    # Takes a partial ordering relation `leq`
    # on a set S and returns the bipartite
    # matching graph, transformed into a flow
    # graph, of the corresponding 
    # chain partitioning problem.
    graph = dict()

    for s in S:
        graph[(0,s)] = []
        for t in S:
            if leq(s, t) and s != t:
                graph[s].append((1,t))

    for s in S:
        graph[(1,s)] = ["T"]

    graph["T"] = []
    graph["S"] = [(0,s) for s in S]

    return graph


        
            
        
