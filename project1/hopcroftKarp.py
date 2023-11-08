from queue import Queue

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


def fitsIn(boxA, boxB):
    return boxA[0] < boxB[0] and boxA[1] < boxB[1] and boxA[2] < boxB[2]

class BipartiteMatching:
    def __init__(self, left, right, adj) -> None:
        self.left = left
        self.right = right
        self.adj = adj
        self.pair_left = dict([(u,'nil') for u in left])
        self.pair_right = dict([(v,'nil') for v in right])
        self.dist = dict()
        self.Q = Queue(5000)
        self.inf = 1000000000000

    def bfs(self):
        for u in self.left:
            if self.pair_left[u] == 'nil':
                self.dist[u] = 0
                self.Q.put(u)
            else:
                self.dist[u] = self.inf
        self.dist['nil'] = self.inf
        while not self.Q.empty():
            u = self.Q.get()
            if self.dist[u] < self.dist['nil']:
                if u in self.adj:
                    for v in self.adj[u]:
                        if self.dist[self.pair_right[v]] == self.inf:
                            self.dist[self.pair_right[v]] = self.dist[u] + 1
                            self.Q.put(self.pair_right[v])
        return not self.dist['nil'] == self.inf

    def dfs(self, u):
        if not u == 'nil':
            if u in self.adj:
                for v in self.adj[u]:
                    if self.dist[self.pair_right[v]] == self.dist[u] + 1:
                        if self.dfs(self.pair_right[v]):
                            self.pair_right[v] = u
                            self.pair_left[u] = v
                            return True
            self.dist[u] = self.inf
            return False
        return True
    
    def hopcroftKarp(self):
        matching = 0
        while self.bfs():
            for u in self.left:
                if self.pair_left[u] == 'nil' and self.dfs(u):
                    matching += 1
        return matching
                    

def makeNbrList(boxes):
    lst = dict()
    lst['S'] = list(map(lambda box: (box,0), boxes))
    for box in boxes:
        lst[(box,1)] = ['T']
        lst[(box,0)] = list(map(lambda ob: (ob,1), filter(lambda x: fitsIn(box, x), boxes)))
    
    return lst

boxes = inputBoxes()
matching = BipartiteMatching(\
    list(map(lambda box: (box,0),boxes)),\
    list(map(lambda box: (box,1),boxes)),\
    makeNbrList(boxes))

#matching = BipartiteMatching([1,2,3], ["A","B","C"], dict([(1,["B","A"]),(2,["B","C"]),(3,["C"])]))
print(len(boxes) - matching.hopcroftKarp())