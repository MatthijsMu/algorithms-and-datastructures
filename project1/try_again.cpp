#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>

using namespace std;

class Matching {
    vector<int> l;
    vector<int> r;
    unordered_map<int,vector<int>> rG;
    unordered_set<int> notMatchedRight {};
    size_t nrMatches = 0;

    Matching(vector<int> left, 
            vector<int> right, 
            unordered_map<int,vector<int>> residualGraph) 
            : l{left}, r{right}, rG{residualGraph} {}

    bool bfs(int p, unordered_map<int, int>& parent, int& q){
        unordered_set<int> visited {};
        queue<int> Q {};
        Q.emplace(p);
        while(!Q.empty()){
            int n = Q.front();
            Q.pop();
            if (!rG.n not in self.residualGraph:
                continue
            
            for q in filter(lambda x : x not in visited, self.residualGraph[n]):
                visited.add(q)
                parent[q] = n
                if q in self.notMatchedRight:
                    return True, parent, q
                else:
                    queue.append(q)
        }
        return False, None, None
    }


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
        self.notMatchedRight.remove(q)
        while q in parent:
            self.residualGraph[parent[q]].remove(q)
            if q not in self.residualGraph:
                self.residualGraph[q] = [parent[q]]
            else:
                self.residualGraph[q].append(parent[q])
            q = parent[q]
        

    def solveMatching(self):
        for l in self.left:
            found, parent, q = self.bfs(l)
            if found:
                self.augmentPath(parent,q)
                self.nrMatches += 1

    def getMatching(self):
        return [(self.residualGraph[p][0],p) for p in filter(lambda q: q in self.right and self.residualGraph[q], self.residualGraph.keys())]
    
    def getNrMatches(self):
        return self.nrMatches
    
}