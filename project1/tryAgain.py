from copy import copy

class Matching:
    def __init__(self, left, right, allowedMatches):
        self.left = left
        self.right = right
        self.residualGraph = allowedMatches
        self.matched = set()
        self.notMatched = set(left)

    def dfs(self, p):
        visited = set()
        stack = [(p,0,len(self.residualGraph[p]))]
        while stack:
            if stack[-1][1] < stack[-1][2]:
                # non-leaf call: there are still nbrs to explore. Take the next neighbour, `current`:
                current = self.residualGraph[stack[-1][0]][stack[-1][1]]
                # print(current)
                stack[-1] = (stack[-1][0], stack[-1][1] + 1, stack[-1][2])
                if current in visited:
                    continue
                else:
                    visited.add(current)
                    if current in self.right and not current in self.matched:
                        # found a path ending in an unmatched node (<=> flow augmenting path)
                        return True, [t[0] for t in stack] + [current] 
                    elif current in self.residualGraph:
                        # dfs:  if there are paths present, step into a new stack frame (push to stack)
                        stack.append((current,0,len(self.residualGraph[current])))
                        continue
            else: 
                # leaf call: tear down current stack frame
                stack.pop()
                continue
            
        return False, []
            

    def augmentPath(self, path):
        for p, s in zip(path, path[1:]):
            self.residualGraph[p].remove(s)
            if s in self.residualGraph:
                self.residualGraph[s].append(p)
            else: 
                self.residualGraph[s] = [p]
        self.matched.add(path[0])
        self.matched.add(path[-1])
        self.notMatched.remove(path[0])

    def solveMatching(self):
        for i, l in enumerate(self.left):
            # print(i)
            found, path = self.dfs(l)
            if found:
                self.augmentPath(path)

        return [(self.residualGraph[p][0],p) for p in filter(lambda q: q in self.right and self.residualGraph[q], self.residualGraph.keys())]
    
class MinChainPartition:
    def __init__(self, poset, relation, topologicalKey):
        self.poset = sorted(poset, key=topologicalKey)
        self.matching = Matching([(p,0) for p in self.poset], \
                                 [(p,1) for p in self.poset], \
                                 dict([((p,0),[(q,1) for q in filter(lambda x: relation(p,x), self.poset)]) for p in self.poset ]))
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
        self.matches = dict([(p,q) for ((p,_),(q,_)) in self.matching.solveMatching()])
        chains = []
        for p in sorted(self.poset, key=self.topologicalKey):
            if not p in self.chained:
                chains.append(self.buildChain([p]))

        return chains
    
    def solveNrChains(self):
        return len(self.poset) - len(self.matching.solveMatching())


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


# matching = Matching([1,2,3,4,5,6], ["A","B","C","D","E"], dict([(1,["A","C"]),(3,["B","E"]),(2,["C"]),(4,["D"]),(6,["D","C"]),(5,["E"])]))
# print(matching.solveMatching())

boxes = inputBoxes()
minChainPartition = MinChainPartition(boxes, fitsIn, volume)
# partition = minChainPartition.solvePartition()
# print(partition)
print(minChainPartition.solveNrChains())
