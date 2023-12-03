import numpy as np

jumps = dict()
jumps[0]=       [4,6]
jumps[1]    =  [6,8]
jumps[2]     =  [7,9]
jumps[3]   =   [4,8]
jumps[4]    =   [3,9,0]
jumps[5]     =  []
jumps[6]      = [1,7,0]
jumps[7]     =  [2,6]
jumps[8]     =  [1,3]
jumps[9]     = [2,4]


def knightDialing(N, start):
    D = np.empty(shape=(N+1,10), dtype = np.int64)
    for k in range(10):
        D[1,k] = 1
    for n in range(2,N+1):
        for k in range(10):
            num = 0
            for dest in jumps[k]:
                num += D[n-1, dest]
            D[n,k] = num
    return D[N,start]

print(knightDialing(3,1))