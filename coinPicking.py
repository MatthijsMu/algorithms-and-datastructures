import numpy as np

def coinPick(c, n):
    '''
    Assuming upper-left means: at position (0,0), and lower-right means: at position (n-1,n-1)
    where grid will be an np.array of shape=(n,n).

    Define T as an (n,n) array where T[i,j] = maximum number of coins that can be collected from square (i,j)
    Since we can only increment indices (i.e. move up or right), there is an obvious base case:

    T[0,0] = c[i,j] since we can collect the coins on c[i,j] and then we are finished

    if (i,j) == (i, n-1), we can only move rightward along the edge of the grid, so T[i,n-1] = c[i,n-1] + t[i+1,n-1]
    if (i,j) == (n-1, j), we can only move upward, hence T[n-1,i] = c[i,j] + T[n-1,j+1]

    Otherwise, we can choose two directions: either up or right. Assuming that we have memoized T[i',j'] 
    for {(i',j'): i'>=i and j'>j}, {(i',j'): i'>i and j'>=j}, we can compute T[i,j] = c[i,j] + max {T[i+1,j],T[i,j+1]}
    
    The correct order of computation is in diagonal bands, i.e starting at

    (n-1,n-1)
    (n-2,n-1),(n-1,n-2)
    (n-3,n-1),(n-2,n-2),(n-1,n-3)

    ...
    (0,n-1), (1,n-2)...(n-2,1), (n-1,0)
    ...

    (0,0)

    In other words, 

    for manh_dist = n-1 down to including 0:
        for  i,j in {(i,j):i+j = manh_dist}
            compute T[i,j] as above

    The induction argument above shows that T[0,0] indeed contains the total maximum number
    of coins one can collect if one follows the optimal path.

    I have made the implementation use one big loop with case distinction.
    I think this is more clear (and with the same complexity of O(n^2)) than having separate loops
    for edge cases.

    Complexity: each square in the grid gets visited once. Inside the loop, there are only constant
    time operations. So the complexity is O(n*n) = O(n^2)
    '''
    T = np.empty(shape=(n,n), dtype=np.int64)

    T[n-1,n-1] = c[n-1,n-1]

    for i in range(n-2,-1,-1):
        T[i,n-1] = c[i,n-1] + T[i+1,n-1]
        T[n-1,i] = c[n-1,i] + T[n-1,i+1]

    for d_from_end in range(1,n):
        for i in range(1,d_from_end+1):
            j = d_from_end - i
            if j <= 0:
                break
            T[i,j] = c[i,j] + max(T[i+1,j],T[i,j+1])

    for d_from_begin in range(n-2,-1,-1):
        for i in range(d_from_begin+1):
            j = d_from_begin - i
            T[i,j] = c[i,j] + max(T[i+1,j],T[i,j+1])

    return T

N = 5
grid = np.random.random_integers(low=0, high=20, size=(N,N))

print(f"Grid:\n{grid}")
dp_grid = coinPick(grid,N)
print(f"Dynamic Programming grid:\n{dp_grid}")