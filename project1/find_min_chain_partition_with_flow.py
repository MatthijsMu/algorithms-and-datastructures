import networkx as nx
import matplotlib.pyplot as plt
import copy
import queue

def posetToMatching(strictPartialOrder, poset):
    verticesA = copy(poset)
    verticesB = copy(poset)
    adjacencyDict = dict()

    for p in poset:
        for s in poset:
            if strictPartialOrder(p,s):
                adjacencyDict[p].append(("B",s))

    return verticesA, verticesB, adjacencyDict

def matchingToFlow(verticesA, verticesB, adjacencyDict):
    adjCapDict = dict([(nA,[(nB, 1) for nB in adjacencyDict[nA]]) for nA in verticesA])
    adjCapDict["S"] = [(nA, 1) for nA in verticesA]
    for nB in verticesB:
        adjCapDict[nB] = [("T",1)]

    return adjCapDict

def findPathDFS(graphDict, explored, path, src, dst):

    if path and path[-1] == dst:
        return True, path
    
    if not path:
        n = src
    else:
        n = path[-1]
   
    for m in graphDict[n]:
        if not m in explored:
            path.append(m)
            explored.append(m)
            found, p = findPathDFS(graphDict, explored, path, src, dst)
            if found:
                return True, p
            else:
                path.pop(-1)
        
    return False, []
        



def solveBinaryFlow(adjCapDict):
    # a simplified implementation specifically tailored for 
    # flow graphs with all edge capacities equal to 1.
    # Since flow(edge) is always a multiple 
    # of the unit quantity in a problem, which is 1 for such 
    # graphs, flows can only either be 0 or 1.
    # Meaning that: we don't have to store the flow values or
    # capacities with the edges, but only need to 
    # list the edges that currently have flow = 1.
    residual = adjCapDict
    active = [] # list of all active flow edges

    found, path = findPathDFS(residual, [], [], "S", "T")
    while found:
        for prev, next in zip(path, path[1:]):
            # reverse each edge from path, in the residual graph
            residual[prev].remove(next)
            residual[next].add(prev)
            active.add((prev, next))
        found, path = findPathDFS(residual, [], [], "S", "T")

    return active

def fromFlowToMatching(activeEdges):
    # Restores the matching in the bipartite matching graph based on the flow
    # on the flow graph:
    matchingEdges = list(filter(lambda x,y: not x == "S" and not y == "T", activeEdges))
    return matchingEdges

def fromMatchingToPartition(matchingEdges, poset):
    partition = []
    matchingEdges += [(p,p) for p in poset]
    while


 

    



def fitsIn(boxA, boxB):
    return boxA[0] < boxB[0] and boxA[1] < boxB[1] and boxA[2] < boxB[2]

def inputBoxes():
    n = int(input())
    boxes = []
    for _ in range(n):
        [x,y,z] = input().split()
        x = float(x)
        y = float(y)
        z = float(z)
        boxes.append(tuple(sorted([x,y,z])))

    return boxes


def main():
    boxes = inputBoxes()
    flow_dict = toFlowProblem(fitsIn, boxes)


main()