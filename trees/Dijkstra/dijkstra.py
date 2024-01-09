from heapq import heappop, heappush
'''
  heapq adapts a sequential, random-access container such as
  a list that adapts a container so that it acts as a min
  heap. We use the functions:
  
  - heappop(H): Assumes that H satisfies the heap property.
                Returns the minimum element, pops this and
                restores the heap property (O(log n) where
                len(H) = n).
                
  - heappush(H, elt):
                Assumes that H satisfies the heap property.
                Inserts elt into the heap, maintaining the 
                heap property (O(log n) where len(H) = n).
'''

def dijkstra(graph_cost_dict : dict[int,int], source_vertex : int, final_vertices_set : set[int]):
    '''
    Computes the vertices in the set final_vertices_set
    '''
    travel_costs_to_final_vertices = []
    cost   = dict([(vertex, 10000) for vertex in graph_cost_dict])
    heap = [(0,source_vertex)]
    finished = set()
    while heap:
        total_cost, top = heappop(heap)
        cost[top] = total_cost
        
        if top in final_vertices_set and not top in finished:
            travel_costs_to_final_vertices.append((top, total_cost))

        finished.add(top)
        for neighbour, dist in graph_cost_dict[top]:
                if neighbour not in finished and cost[neighbour] > dist + total_cost:
                    heappush(heap, (dist + total_cost, neighbour))
                    cost  [neighbour] = dist + total_cost

    return travel_costs_to_final_vertices

def reduce (graph_cost_dict : dict[int,int], new_vertices_list : list[int]):
    '''
    Reduces a graph to a complete graph with as vertices new_vertices_list and edges representing
    the shortest paths between new_vertices, with as their distances the shortest path length.
    '''
    final_vertices_set = set(new_vertices_list)
    return dict([(fin_vtx, dijkstra(graph_cost_dict, fin_vtx, new_vertices_set)) for fin_vtx in new_vertices_list])


def testMe():
    graph_dict = dict([
        (0 , [(2,5),(3,2)]), 
        (1 , [(2,8),(5,2)]),
        (2 , [(0,5),(1,8),(3,3)]),
        (3 , [(0,2),(2,3),(4,7)]),
        (4 , [(3,7),(5,4)]),
        (5 , [(1,2),(4,4)])
    ])

    final_vertices_list = [1,3,4]

    reduced_graph = reduce(graph_dict, final_vertices_list)

    print(reduced_graph)
    
testMe()
