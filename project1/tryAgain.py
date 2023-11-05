from copy import copy
from collections import deque

class Matching:
    def __init__(self, left, right, allowedMatches):
        self.left = left
        self.right = right
        self.residualGraph = allowedMatches
        self.notMatchedRight = set(right)
        self.notMatchedLeft = set(left)
        self.nrMatches = 0

    def bfs(self, p):
        visited = set()
        queue = deque()
        queue.append(p)
        parent = dict()
        while queue:
            n = queue.popleft()
            if n not in self.residualGraph:
                continue
            
            for q in filter(lambda x : x not in visited, self.residualGraph[n]):
                visited.add(q)
                parent[q] = n
                if q in self.notMatchedRight:
                    return True, parent, q
                else:
                    queue.append(q)
                
        return False, None, None


    def dfs(self, p):
        visited = set()
        parent = dict()
        stack = deque()
        stack.append(p)
        while stack:
            n = stack.pop()
            if n not in self.residualGraph:
                continue
            for q in filter(lambda x : x not in visited, self.residualGraph[n]):
                visited.add(q)
                parent[q] = n
                if q in self.notMatchedRight:
                    return True, parent, q
                else:
                    stack.append(q)
                    
        return False, None, None

        
            

    def augmentPath(self, parent, q):
        if len(parent) == 21:
            pass
        self.notMatchedRight.remove(q)
        while q in parent:
            self.residualGraph[parent[q]].remove(q)
            if q not in self.residualGraph:
                self.residualGraph[q] = [parent[q]]
            else:
                self.residualGraph[q].append(parent[q])
            q = parent[q]
        

    def solveMatching(self):
        for l in self.notMatchedLeft:
            found, parent, q = self.dfs(l)
            if found:
                self.augmentPath(parent,q)
                self.nrMatches += 1

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


#matching = Matching([1,2,3], ["A","B","C"], dict([(1,["B","A"]),(2,["B","C"]),(3,["C"])]))
#print(matching.solveMatching())

boxes = inputBoxes()
print("done with input")
minChainPartition = MinChainPartition(boxes, fitsIn, volume)
print("done creating partition problem")
minChainPartition.solvePartition()
print("done solving partition problem")
# partition = minChainPartition.solvePartition()
# print(partition)
print(minChainPartition.getNrOfChains())
