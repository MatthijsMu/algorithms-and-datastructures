import numpy as np

def matMul(p):
    '''
    Given matrices of dimension
    A_0:    p[0] by p[1]
    A_1:    p[1] by p[2]
    ...
    A_n-2:  p[n-2] by p[n-1]

    where n = len(p)

    define the n-1 by n-1 matrices m and s as follows:
    m[i,j] = minimum number of operations needed to multiply A_i ... A_j optimally.
    s[i,j] = the k in [i, j-1] such that the top-level bracketing (A_i ... A_k)(A_k ... A_j) gives the optimal order of operations.

    Note that these numbers only make sense for j >= i. For j < i, we leave these matrices undefined and don't care about their contents

    They also satisfy the recursion:
    m[i,i] = 0 for all i

    m[i,j] = min {m[i, k] + m[k + 1, j] +  + nrows[i] * ncols[k] * ncols[j] | i <= k < j}
    s[i,j] = argmin {m[i, k] + m[k + 1, j] +  + nrows[i] * ncols[k] * ncols[j] | i <= k < j}

    
    Where, for **clarity** (there was so much trouble with indexing due to 1 based/ 0 based differenced XD), 
    ncols and nrows are just views of p[1:], p[:-1], respectively.

    The order of computation is important: we need to iterate over i,j correctly to make sure that all memoized values are already present.
    This actually means, quite simply, that we can only compute m[i,j] for longer subsequences A_i ... A_j once we know m[i,j] for all shorter
    subsequences. I.e., we know at first only how many multiplications it takes to compute A_0, A_1, ... A_n-2 (all take 0 multiplications!). 
    Next, we can calculate the number for A_1 A_2, A_2 A_3, ... A_n-3 A_n-2. 
    Next, for A_1 A_2 A_3, A_2, A_3, A_4, .. etc.

    In other words, in the outer loop, iterate over d, the length of subsequences, that is d:= j - i = 0, 1, ..., n-2 - 0 = n-2:
        Inside, iterate over i = 0, ... until j:= i+d > n-2, then break and go to the next d.
            Inside, iterate over k. Keep track of the current argmax and max, and once done iterating over k, write these to 
            m[i,j], s[i,j] respectively.
    '''
    n = len(p)

    nrows = p[:-1]
    ncols = p[1:]

    m = np.empty(shape=(n-1,n-1), dtype=np.int64)
    s = np.empty(shape=(n-1,n-1), dtype=np.int64)

    for i in range(0,n-1):
        m[i,i] = 0

    for d in range (1,n-1):
        for i in range(0,n-1):
            j = i+d
            if j > n-2:
                break
            min = m[i,i] + m[i+1, j] + nrows[i] * ncols[i] * ncols[j]
            argmin = i
            for k in range(i+1, j):
                if m[i, k] + m[k + 1, j] + nrows[i] * ncols[k] * ncols[j] < min:
                    min = m[i, k] + m[k + 1, j] + nrows[i] * ncols[k] * ncols[j]
                    argmin = k
            m[i,j] = min
            s[i,j] = argmin
    
    return m, s

def obtainParenthesization(s, i, j):
    '''
    Obtaining the minimum number of operations is simple: this is stored in m[0,n-2].

    How do we obtain the corresponding parenthesizing?
    Well, if s[i,j] = k, then this is equal to:
    "( the optimal parenthesizing of A_i...A_k, which can be found recursively using s[i,k])( the optimal parenthesizing of A_k+1...A_j, which can be found recursively using s[k,j])

    The base case is encountered when k = i or k = j, in which case one of the clauses is just A_i or A_j, respectively.

    In other words, we can find this parenthesizing recursively from array s. 

    What is the complexity of this lookup? Well, it is sort of a tree search, but there are only n-2 A_i, and every time we recurse, one split is created, and there
    are only n-3 places between A_i's where splits can be created, so the search will branch n-3 times in total before it can only encounter leaves. So obtaining
    the parenthization is O(n).
    '''
    if i == j:
        return f"A_{i}"
    else:
        return f"({obtainParenthesization(s,i, s[i,j])})({obtainParenthesization(s,s[i,j]+1,j)})"

def getMatrixDims():
    return [int(s) for s in input("give the dimensions p0, .. , pn-1, where Ai = pi x pi+1 for i = 0, .. n-2:\n").split()]

dims = getMatrixDims()
n = len(dims)
m, s = matMul(dims)
print(m)
print(f"Least number of operations needed: {m[0, n-2]}")
print("optimal parenthesization:")
print(obtainParenthesization(s, 0, n-2))