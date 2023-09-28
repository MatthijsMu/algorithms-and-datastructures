#include <list>
#include <map>
#include <algorithm>
#include <set>

using namespace std;

enum color {
    grey, white, black
};

class Graph {
public:
    // access functions
    virtual list<int> &vertices () = 0;

    virtual set<int> &adjacent_vertices (int) = 0;

    virtual bool adjacent (int, int) const = 0;
};

class Adj_List_Graph : Graph {
private:
    list<int> v;
    map<int, set<int>> adj_v;

public:
    //constructor:
    Adj_List_Graph(list<int> &vv, map<int, set<int>> &al) : v{vv}, adj_v{al} {}

    list<int> &vertices () override {
      return v;
    }

    set<int> &adjacent_vertices (int vertex) override {
      return adj_v.at(vertex);
    }


    bool adjacent (int u, int v) const override {
      return adj_v.at(u).find (v) != adj_v.at (u).end();
    }
};

void dfs_visit(Graph &G, int vertex, size_t &time, map<int, size_t> &d,
               map<int, size_t> &f, map<int, color> &coloring);

void dfs (Graph &G, map<int, size_t> &d,
          map<int, size_t> &f);

int main(void) {
  list<int> vs {1,2,3,4,5,6,7};
  map<int,set<int>> adjs {pair<int, set<int>>{1, {3}}, pair<int, set<int>>{2, {3}}, pair<int, set<int>>{3, {4,5}}, pair<int, set<int>>{4, {6}}, pair<int, set<int>>{5, {6}}, pair<int, set<int>>{6, {7,8}}};
  Adj_List_Graph myGraph (vs, adjs);

  
}






void dfs (Graph &G, map<int, size_t> &d,
                   map<int, size_t> &f) {
  map<int, color> coloring{};

  for (int vertex: G.vertices ()) {
    coloring.emplace (pair<int, color>{vertex, white});
  }

  size_t time = 0;

  for (int vertex: G.vertices()) {
    if (coloring.at (vertex) == white)
      dfs_visit (G, vertex, time, d, f, coloring);
  }
}

void dfs_visit (Graph &G, int vertex, size_t &time, map<int, size_t> &d,
                map<int, size_t> &f, map<int, color> &coloring) {
  d.emplace (pair<int, size_t>{vertex, ++time});
  coloring.at (vertex) = grey;
  for (int neighbour : G.adjacent_vertices (vertex)) {
    dfs_visit (G, neighbour, time, d, f, coloring);
  }
  coloring.at (vertex) = black;
  f.emplace (pair<int, size_t>{vertex, ++time});
}



