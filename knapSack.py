import numpy as np

def knapSack(v, s, C):
    n = len(v)
    A = np.empty(shape=(n, C+1), dtype=np.uint64)

    '''
    A[i,c] is defined as "the maximum value at capacity c given an itemset 0..i, 
    where for i=0 this is the singleton set {0}, since s and v have zero-based index

    A is an n by C+1 matrix, since we use rows for i=0,..,n-1 and columns for c = 0,...C

    This gives the recursion:
    A[i,c] = A[i-1,c]                               if  s[i] > c, and for i=0 this is 0
    A[i,c] = max{A[i-1,c], A[i-1,c-s[i]] + v[i]}    if  s[i] <= c, and for i=0 this is v[i]
    '''
    for c in range(0,C+1):
        if c >= s[0]:
            A[0,c] = v[0]
        else:
            A[0,c] = 0

    for i in range(1,n):
        for c in range(C+1):
            if s[i] > c:
                A[i,c] = A[i-1,c]
            else:
                A[i,c] = max(A[i-1,c], A[i-1,c-s[i]] + v[i])

    return A, A[n-1,C]

def knapSackReconstruction(v, s, C, A):
    n = len(v)
    S = []
    c = C
    for i in range(n-1,-1, -1):
        if s[i] <= c and A[i-1,c-s[i]] + v[i] >= A[i-1,c]:
            S.append(i)
            c -= s[i]
    
    return S

def getValues():
    print("enter the values of the items on one line, separated by spaces:")
    return [int(s) for s in input().split()]

def getSizes():
    print("enter the sizes of the items on one line, separated by spaces:")
    return [int(s) for s in input().split()]

def getCapacity():
    print("enter the capacity of the knapsack:")
    return int(input())

v = getValues()
s = getSizes()
C = getCapacity()

assert len(s) == len(v), "number of values does not match number of given sizes."

A, V = knapSack(v, s, C)
S = knapSackReconstruction(v, s, C, A)

print(f"The total value is {V}.")
print(f"This is obtained by packing items {[i+1 for i in S]}.")

print(A)
