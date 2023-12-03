import numpy as np

def maxPathLineGraph(nbrs):
    n = len(nbrs)
    L = np.empty(shape=(n), dtype=np.int64)
    L[n-1] = 0
    for i in range(n-2, -1, -1):
        max = -1
        for j in nbrs[i]:
            if L[j] > max:
                max = L[j]
        L[i] = max + 1
    return L[0]

graph = dict()
graph[0] = [1,3]
graph[1] = [3,4]
graph[2] = [3]
graph[3] = [4]
graph[4] = []

print(maxPathLineGraph(graph))