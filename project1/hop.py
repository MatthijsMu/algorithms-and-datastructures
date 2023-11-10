from collections import deque

class Matching:
    def __init__(self, left, right, allowedMatches):
        self.residualGraph = allowedMatches
        self.residualGraph['s'] = left
        self.notMatchedRight = set(right)
        self.notMatchedLeft = set(left)
        self.nrMatches = 0

    def bfs(self):
        visited = set()
        visited.add('s')

        queue = deque(self.notMatchedLeft)
        queue.appendleft('s')

        depth = dict()
        depth['s'] = 0
        for l in self.notMatchedLeft:
            depth[l] = 1
        
        current_d = 1

        found = False

        parents = dict()
        final = []
        while queue:
            n = queue.popleft()
            d = depth[n]
            if d > current_d:
                if found:
                    return True, parents, final
                else:
                    current_d = d
            if n not in self.residualGraph:
                continue
            
            for q in filter(lambda x : x not in visited or depth[q] == d+1, self.residualGraph[n]):
                if q in self.notMatchedRight and q not in visited:
                    final.append(q)
                    found = True
                elif q not in visited:
                    queue.append(q)
                depth[q] = d+1
                visited.add(q)
                if q in parents:
                    parents[q].append(n)
                else:
                    parents[q] = [n]
                
        return found, parents, final
    
    def dfs(self, parents, final):
        
        used = set()
        parent = dict()
        for qf in final:
            n = qf
            while n != 's':
                
                if list(filter(lambda x: x not in used, parents[n])):
                    # the first q in parents[n] will become its parent.
                    # this approach will give a maximal set of augmenting paths.
                    q = list(filter(lambda x: x not in used, parents[n]))[0]
                    parent[n] = q
                    if q != 's':
                        # we can mark any node we explore while searching, since if we cannot
                        # find a path through n from one node in final, then we cannot find 
                        # any path from final to 's' through n, so we don't need to explore
                        # n ever again.
                        used.add(q)
                    else:
                        self.notMatchedLeft.remove(n)
                # dfs into n's parent
                else:
                    break
                n = parent[n]
            # if successful, i.e. if 's' is indeed reached, add qf to used
            if n == 's':
                used.add(qf)

        return parent, list(filter(lambda q: q in used, final))
        


    def augmentPaths(self, parent, qs):
        for q in qs:
            self.notMatchedRight.remove(q)
            self.nrMatches += 1
            p = q
            while p in parent:
                self.residualGraph[parent[p]].remove(p)
                if p not in self.residualGraph:
                    self.residualGraph[p] = [parent[p]]
                else:
                    self.residualGraph[p].append(parent[p])                    
                p = parent[p]
        

    def solveMatching(self):
        while True:
            found, parents, qs = self.bfs()
            if found:
                parent, qs = self.dfs(parents, qs)
                self.augmentPaths(parent,qs)
            else:
                break

    def getMatching(self):
        return [(self.residualGraph[p][0],p) for p in filter(lambda q: q in self.right and self.residualGraph[q], self.residualGraph.keys())]
    
    def getNrMatches(self):
        return self.nrMatches
    
class MinChainPartition:
    def __init__(self, poset, relation, topologicalKey):
        self.poset = poset
        self.matching = Matching(list(range(len(poset))), \
                                 list(range(5000, 5000+len(poset))), \
                                 dict([(i,[j+5000 for j,q in filter(lambda x: relation(p,x[1]), enumerate(self.poset))]) for i,p in enumerate(self.poset) ]))
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
