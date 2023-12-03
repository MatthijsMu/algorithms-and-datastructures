import numpy as np

def LCS(s, z):
    '''
    computes the longest common subsequence 
    of two sequences s and z (assumed to be lists)
    where n <= m:

    A common subsequence of two sequences s[0..n-1], z[0..m-1]
    where m,n are natural numbers, is defined as
    a list of natural numbers N[0..k-1] such that
    N is strictly increasing, i.e. N[l] < N[l+1],
    such that N[k-1] < n, 
    and such that s[N[l]] == z[N[l]] for all l.

    a longest common subsequence, or LCS, is a subsequence that has 
    maximum length over all subsequences. It may not be unique, but its
    length is since the natural numbers are a well-order and s and z are finite.

    (As an example, consider 1,2,3 and 2,1,3: there are two LCS)
    
    The method:
    - Let m be a n by m array, where m[i,j] is the length of a LCS of s[0..i] and z[0..j]
    - We can recognize a recursion in this definition:
      A[i,j] = 
        - if s[i] != z[j], then it is the length of the LCS of 
        (s[1..i],z[i..j-1]) or (s[1..i-1],z[i..j]), so the maximum of
        LCS(s[1..i],z[1..j-1]), LCS(s[1..i-1],z[1..j]), or A[i,j-1], A[i-1,j]

        - if s[i] = s[j], we can take the LCS of s[1..i-1] and z[1..j-1] and append
        s[i],z[j] to this. Hence it is LCS(s[1..i-1],z[1..j-1]) + 1, or A[i-1,j-1] + 1

        if i = 0 or j = 0, A[i,j] = 0 ("base case")

    Performing this recursion explicitly is unnecessary and computationally expensive.
    The key ingredient is memoization. This we do using the array m, and the
    correct bottom-up way of computing each m[i,j]:

    First write 0 to A[i,0] and [0.j] for all i = 0..n-1, j = 0..m-1
    Then compute m[i,j] only when m[i-1,j-1], m[i-1,j], m[i,j-1] are already available.
    This we can do simply by row-wise computation, as long as we start each row in the "(1,row) corner", where
    all recursion neighbours have already been computed:

    1   1   1   1
    1   2   3   4
    1   5   6   7
    1   8   9  10
    1   11 ...
    1
    
    '''
    n = len(s)
    m = len(z)

    A = np.empty(shape=(m+1,n+1), dtype=np.int64)

    for row in range(m+1):
        print(f'A[{row,0}] = 0\n')
        A[row,0] = 0

    for col in range(n+1):
        print(f'A[{0,col}] = 0\n')
        A[0,col] = 0

    for j in range(1,n+1):
        for i in range(1,m+1):
            print(f's[{j}] = ', s[j-1], f', z[{i}] = ', z[i-1])
            if s[j-1] == z[i-1]:
                print(f' are equal, so A[{i,j}] = A[{i-1,j-1}] + 1 = ', A[i-1,j-1]+1, '\n')
                A[i,j]=A[i-1,j-1]+1
            else:
                print(f'are unequal, so A[{i,j}] = max ( A[{i-1,j}], A[{i,j-1}] ) = max ({A[i-1,j],A[i,j-1]}) = ',max(A[i-1,j],A[i,j-1]),'\n')
                A[i,j]=max(A[i-1,j],A[i,j-1])

    return A, A[m,n]

    
def retrieve_subseq(A, s, z):
    '''
    To retrieve afterwards what an LCS is corresponding to the found max length of any LCS, 
    we can keep track of how A[i,j] changes as we decrease i and j:

    starting at (i,j) = (n,m),

    EACH STEP CONSISTS OF TWO CHECKS:

    - if A[i,j] = A[i-1,j-1] + 1, we can construct a LCS by including s[i],z[j]. So mark both s[i] and z[j] as included, and append this
        recursively to the subsequence of s[0..i-1], z[0..j-1] by moving to A[i-1,j-1] and investigating that number.
    
    - if A[i,j] = A[i-1,j-1] + 1 does not hold, either:
        - A[i,j] = A[i,j-1]: this means that the LCS of s[0..i], z[0..j] does not include z[j]. so decrement j by 1 and don't mark anything
        - A[i,j] = A[i-1,j]: this means that the LCS of s[0..i], z[0..j] does not include s[i]. so decrement i by 1 and don't mark anything
    
    do this until either i = 0 or j = 0. In that case, we have considered all elements of s, or z, respectively.
    So we can stop, because one of the considered sequences is empty, so there were no other elements from the nonempty sublist included in the LCS

    The indices (i,j) in marked then give all the matching elements s[i], z[j] in the LCS. This retrieval algorithm decreases at least i or j
    in each STEP, and one STEP is O(1) since it entails only O(1) conditional checks and O(1) assignments.

    so the retrieval algorithm runs in O(n+m). This is dominated by the O(nm) for the computation of A.
    '''

    lcs = []

    i,j = A.shape 
    i-=1
    j-=1
    while i > 0 and j > 0:
        if A[i,j] == A[i-1,j-1] + 1:
            print(f'A[{i,j}] = A[{i-1,j-1}] + 1, so prepend s[{j}] = {s[j-1]}')
            i-= 1
            j-= 1
            lcs.append(s[j-1])
        elif A[i,j] == A[i-1,j]:
            print(f'A[{i,j}] != A[{i-1,j-1}] + 1, but A[{i,j}] = A[{i-1,j}], so i--')
            i-=1
        else:
            print(f'A[{i,j}] != A[{i-1,j-1}] + 1, but A[{i,j}] = A[{i-1,j}], so i--')
            j-=1
        print(f'(i,j) = {i,j}')

    return lcs

s = [1,0,0,1,0,1,0,1]
z = [0,1,0,1,1,0,1,1,0]

lcs_arr, len_lcs = LCS(s,z)

print(lcs_arr)

print(len_lcs)

print(retrieve_subseq(lcs_arr, s, z))