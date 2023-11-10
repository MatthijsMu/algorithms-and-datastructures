from copy import copy
from collections import deque

class Matching:
    def __init__(self, left, right, allowedMatches):
        # The set of left nodes in the matching.
        # These need to be named differently than
        # the set of right nodes, since the graph
        # search algorithms implemented here assume 
        # all nodes of the graph have a unique name
        self.left = left
        # The set of right nodes
        self.right = right
        # The residual graph is the directed graph
        # formed by vertices V = left Union right Union {'s'},
        # E = {(n,m): n in left, m in right and n may be matched with m} Union {('s', n): n in left}
        # It is represented as a dictionary mapping key n to its adjacency list.
        self.residualGraph = allowedMatches
        self.residualGraph['s'] = left
        # A set (has O(1) lookup/add/delete operations) of
        # all nodes in right that have not been matched yet.
        # this is needed to see whether bfs has already reached an end node.
        # Alternatively, we could have appended a node 't' to completely
        # transform this into a flow problem, but since the below implementation
        # works fine, I won't alter it.
        self.notMatchedRight = set(right)
        # Implicitly, there is a set notMatchedLeft consisting of all nodes
        # that can be reached from 's' in the residual graph (since edges ('s',n) are 
        # reversed once an augmenting path through n is foun, i.e. once n is matched)
        self.nrMatches = 0

    def bfs(self):
        # Keep a set of visited nodes: prevents cycling.
        visited = set()
        visited.add('s')
        # The queue to which newly visited nodes are added.
        # The queue also stores each nodes depth in the bfs tree,
        # for bookkeeping
        queue = deque()
        queue.append(('s',0))
        # A parent dictionary, giving the node's predecessor in the
        # bfs tree.
        parent = dict()
        # The current depth of the bfs tree (increments monotonically
        # every time we enter a deeper layer of the bfs tree)
        depth = 0
        found = False
        # qs is a list of all nodes in notMatchedRight 
        # that have a minimum augmenting path
        # to 's'
        qs = []


        while queue: 
            # pop a visited node and its depth from the queue
            n,d = queue.popleft()
            # if we go a layer deeper into the bfs tree:
            if d > depth:
                # if we already found a notMatchedRight node, 
                # return all found nodes and the bfs tree
                if found:
                    return True, parent, qs
                # else, set the depth to d.
                else:
                    
                    depth = d


            # The following step is needed because the adjacency dictionary may not 
            # have n as a key (we could have resolved this by giving n's with no
            # outgoing edges an entry (n, []) in the dictionary, but this also 
            # works and reduces space overhead). If there are no outgoing edges,
            # n is a leaf and we skip.
            if n not in self.residualGraph:
                continue
            
            # Else, expand n: filter on descendants that have not been visited yet.
            # since visited is a set, filtering is a linear scan O(n)
            for q in filter(lambda x : x not in visited, self.residualGraph[n]):
                visited.add(q)
                parent[q] = n
                # If q is in right and notMatched (O(1) lookup into the set self.notMatchedRight),
                # append to qs (the set F of final nodes of augmenting paths), and set
                # found to True
                if q in self.notMatchedRight:
                    qs.append(q)
                    found = True
                    break
                # Else, enqueue q, with its appropriate depth.
                else:
                    queue.append((q,depth+1))
                
        return found, parent, qs


    def augmentPaths(self, parent, qs):
            usedVertices = set()
            for q in qs:
                # DFS check:
                # First check whether there is still a path of unused vertices through parent
                # It could happen that a BFS branch forked somewhere, in which case only one
                # of the two paths to a node in qs should be inverted.
                checkPath = True
                p = q
                while p in parent:
                    if p in usedVertices:
                        checkPath = False
                        break
                    else:
                        p = parent[p]
                if not checkPath:
                    break

                # If the DFS check above did not fail, we can continue and
                # reverse all edges along this path in the residual graph, 
                # increment nrMatches and remove q from the notMatchedRight 
                # set:
                self.notMatchedRight.remove(q)
                self.nrMatches += 1
                p = q
                while p in parent:
                    # We should mark used nodes as used, otherwise
                    # the above DFS check does not work
                    usedVertices.add(p)
                    self.residualGraph[parent[p]].remove(p)
                    # This if-statement is needed to (again) avoid keyErrors 
                    # in the adjacency dictionary.
                    if p not in self.residualGraph:
                        self.residualGraph[p] = [parent[p]]
                    else:
                        self.residualGraph[p].append(parent[p])
                    # Go to next p in path
                    p = parent[p]
        

    def solveMatching(self):
        while True:
            # BFS for minimum augmenting paths
            found, parent, qs = self.bfs()
            if found:
                # DFS for a "maximal" set of augmenting paths (this is not entirely true: 
                # because not all possible paths may have been considered; it could be that 
                # a node n that can be reached from m and k, was already marked as visited 
                # when explored from m, so that parent[n] = m, but m gets used in another path. 
                # In that case, there could have been another path through (k,n) but this path
                # is never considered because k is not collected as a potential parent of n.
                # Now, this issue has been resolved in an alternative implementation where parent
                # maps nodes to lists of predecessors and visited nodes are allowed to be explored
                # a second time from)
                self.augmentPaths(parent,qs)
            else:
                break

    def getMatching(self):
        return [(self.residualGraph[p][0],p) for p in filter(lambda q: q in self.right and self.residualGraph[q], self.residualGraph.keys())]
    
    def getNrMatches(self):
        return self.nrMatches
    
class MinChainPartition:
    def __init__(self, poset, relation, topologicalKey):
        self.poset = sorted(poset, key=topologicalKey)
        self.matching = Matching([(p,0) for p in self.poset], \
                                 [(p,1) for p in self.poset], \
                                 dict([((p,0),[(q,1) for q in filter(lambda x: relation(p,x), self.poset[i:])]) for i,p in enumerate(self.poset) ]))
        self.relation = relation
        self.topologicalKey = topologicalKey
        self.chained = set()
        self.matches = dict()

    def buildChain(self, ch):
        while ch[-1] in self.matches:
            self.chained.add(ch[-1])
            ch.append(self.matches[ch[-1]])
        self.chained.add(ch[-1])
        return ch


    def solvePartition(self):
        self.matching.solveMatching()

    def getPartition(self):
        self.matches = dict([(p,q) for ((p,_),(q,_)) in self.matching.getMatching()])
        chains = []
        for p in sorted(self.poset, key=self.topologicalKey):
            if not p in self.chained:
                chains.append(self.buildChain([p]))

        return chains
    
    def getNrOfChains(self):
        return len(self.poset) - self.matching.getNrMatches()


def fitsIn(boxA, boxB):
    return boxA[0] < boxB[0] and boxA[1] < boxB[1] and boxA[2] < boxB[2]

def volume(box):
    return box[0] * box[1] * box[2]

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

'''
matching = Matching([1,2,3], ["A","B","C"], dict([(1,["B","A"]),(2,["B","C"]),(3,["C"])]))
matching.solveMatching()
print(matching.getNrMatches())

'''
boxes = inputBoxes()
#print("done with input")
minChainPartition = MinChainPartition(boxes, fitsIn, volume)
#print("done creating partition problem")
minChainPartition.solvePartition()
#print("done solving partition problem")
# partition = minChainPartition.solvePartition()
# print(partition)
print(minChainPartition.getNrOfChains())

