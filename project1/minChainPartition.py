from collections import deque

class Matching:
    def __init__(self, left, right, allowedMatches):
        self.residualGraph = allowedMatches
        self.residualGraph['s'] = left
        self.notMatchedRight = set(right)
        self.notMatchedLeft = set(left)
        self.nrMatches = 0

    def bfs(self):
        '''
        Performs a breadth-first search for a (not necessarily) vertex-disjoint set 
        of augmenting paths. The result is not a bfs tree, but a bfs lattice, where
        the final nodes at depth d have a list of parent nodes at depth d+1, etc.

        The search is performed starting in an imaginary source node 's'. We immediately
        append all self.notMatchedLeft nodes to the queue. Although this is functionally
        not necessary, it removes some redundant checks and is thus faster, even though
        self.notMatchedLeft is an unordered set, so that iteration is O(N_buckets)
        '''
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
        '''
        Performs a dfs for a maximal set of paths in a lattice found by self.bfs().
        Maximal is not maximum: thus, we can safely mark a node as used immediately
        upon discovery, since if a node cannot be used in a path from a predecessor p,
        then for any other predecessor q, we cannot reach 's' through this node either.

        Returns the set of final nodes that have a path in the found maximal set of 
        augmenting paths, and a dictionary parent that gives the (edge-disjoint) parent
        relation in the dfs tree.
        '''
        
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
        '''
        Given a maximal set of shortest augmenting paths, ending in the final
        set of unmatched right nodes `qs`, where the paths are given by a 
        dictionary that maps children to predecessors, this function reverses
        the edges along these paths in the residual graph and removes 
        the nodes in qs from self.notMatchedRight. It also updates the attribute
        self.nrMatches appropriately to the increase in matches that these
        augmenting paths give.
        '''
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
        '''
        Solves the matching problem using the Hopcroft-Karp algorithm (O(n^(5/2))):

        While an augmenting path exists, find a maximal set of vertex-disjoint augmenting
        paths and augment the flow along these paths.
        '''
        while True:
            found, parents, qs = self.bfs()
            if found:
                parent, qs = self.dfs(parents, qs)
                self.augmentPaths(parent,qs)
            else:
                break

    def getMatching(self):
        '''
        This function returns the pairs of nodes that are matched. 
        '''
        return [(self.residualGraph[p][0],p) for p in filter(lambda q: q in self.right and self.residualGraph[q], self.residualGraph.keys())]
    
    def getNrMatches(self):
        return self.nrMatches
    
class MinChainPartition:
    def __init__(self, poset, relation, topologicalKey):
        self.poset = poset
        self.matching = Matching(list(range(len(poset))), \
                                 list(range(len(poset), 2*len(poset))), \
                                 dict([(i,[j+len(poset) for j,q in filter(lambda x: relation(p,x[1]), enumerate(self.poset))]) for i,p in enumerate(self.poset) ]))
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
        '''
        Returns the minimum partition into chains as a list of lists, where the inner lists
        are lists of poset elements, and these represent the chains.
        '''
        self.matches = dict([(self.poset[i],self.poset[j-len(self.poset)]) for (i,j) in self.matching.getMatching()])
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
