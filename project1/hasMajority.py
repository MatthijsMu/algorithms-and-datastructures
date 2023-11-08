def hasMajority(eq, lst):
    n = len(lst)
    if n == 1:
        return True, 1, lst[0]
    
    hasMaj1, nrMaj1, valMaj1 = hasMajority(eq, lst[:n//2])
    hasMaj2, nrMaj2, valMaj2 = hasMajority(eq, lst[n//2:])

    if hasMaj1 and hasMaj2 and valMaj1 == valMaj2:
        return True, nrMaj1 + nrMaj2, valMaj1
    else:
        return False, None, None

# The algorithm has the following recurrence relation for the complexity:
# T(0) = O(1)
# T(n) = 2 T(n/2) + O(1)
# Hence by the tree method, we find that it must run in O(lg n) time