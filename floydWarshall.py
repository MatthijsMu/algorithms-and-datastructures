import numpy as np

class FloydWarshall:
    def __init__(self, graph_dict, dist_dict):
        '''
        Assumes that all the nodes in the graph are
        present as keys in graph_dict, and that these
        are integers 0, ... , n-1, where n is the number 
        of nodes.

        This simplifies array indexing in numpy by a lot.
        '''
        self.n = len(graph_dict)
        self.D = np.full(shape = (self.n,self.n), fill_value = np.inf, dtype=float)
        self.parent = np.full(shape = (self.n,self.n), fill_value = np.NaN)
        for i in graph_dict:
            self.D[i][i] = 0
            for j in graph_dict[i]:
                self.D[i][j] = dist_dict[(i,j)]
                self.parent[i][j] = i

    def __iterate(self, k):
        print(self.D)
        D_out = np.empty(shape = (self.n, self.n))
        parent_out = np.empty(shape = (self.n, self.n))

        for i in range(self.n):
            for j in range(self.n):
                if self.D[i][j] > self.D[i][k] + self.D[k][j]:
                    parent_out[i][j] = self.parent[k][j]
                    D_out[i][j] = self.D[i][k] + self.D[k][j]
                else:
                    parent_out[i][j] = self.parent[i][j]
                    D_out[i][j] = self.D[i][j]

        self.D = D_out
        self.parent = parent_out


    def solve(self):
        for k in range(self.n):
            self.__iterate(k)
        print(self.D)


graph_dict = dict()

graph_dict[0] = [4]
graph_dict[1] = [0,3]
graph_dict[2] = [1,5]
graph_dict[3] = [0,4]
graph_dict[4] = [1]
graph_dict[5] = [1,2]

distance_dict = dict()
distance_dict[0,4] = -1
distance_dict[1,0] = 1
distance_dict[1,3] = 2
distance_dict[2,1] = 2
distance_dict[2,5] = -8
distance_dict[3,0] = -4
distance_dict[3,4] = 3
distance_dict[4,1] = 7
distance_dict[5,1] = 5
distance_dict[5,2] = 10


problem3 = FloydWarshall(graph_dict, distance_dict)
problem3.solve()