from heapq import heappush, heappop

def heapsort(L : list[int]):
    H = []
    for elt in L:               # len(L) times
        heappush(H, elt)        # O(log(len(L)))
    res = []
    for elt in L:               # len(L) times
        res.append(heappop(H))  # O(log(len(L)))
    return res
    
print(heapsort([1,2,3,3,2,1,23,2,1,2,30]))
