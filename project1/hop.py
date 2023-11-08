from copy import copy
from collections import deque

class Matching:
    def __init__(self, left, right, allowedMatches):
        self.left = left
        self.right = right
        self.residualGraph = allowedMatches
        self.residualGraph['s'] = left
        self.notMatchedRight = set(right)
        self.nrMatches = 0

    def bfs(self):
        visited = set()
        visited.add('s')
        queue = deque()
        queue.append(('s',0))
        depth = 0
        found = False
        fronts = []
        final = set()
        while queue:
            n,d = queue.popleft()
            if d > depth:
                if found:
                    return True, fronts
                else:
                    depth = d
                    fronts.append([])
            if n not in self.residualGraph:
                continue
            
            for q in filter(lambda x : x not in visited, self.residualGraph[n]):
                visited.add(q)
                fronts[-1].append(q)
                if q in self.notMatchedRight:
                    final.add(q)
                    found = True
                    break
                else:
                    queue.append((q,depth+1))
                
        return found, fronts
    
    def dfs(self, fronts, final):
        stack = deque()
        stack.append('s')

        while stack:
            n = stack.pop()
            for q in filter(lambda)

        


    def augmentPaths(self, parent, qs):
            usedVertices = set()
            for q in qs:
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
                    # We should mark used nodes as used:
                    usedVertices.add(p)
                    self.residualGraph[parent[p]].remove(p)
                    if p not in self.residualGraph:
                        self.residualGraph[p] = [parent[p]]
                    else:
                        self.residualGraph[p].append(parent[p])
                    p = parent[p]
        

    def solveMatching(self):
        while True:
            found, parent, qs = self.bfs()
            if found:
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

