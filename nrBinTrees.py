def nrBinTrees(n):
    array = [0] * (n+1)
    array[0] = 1
    for i in range(1,n+1):
        array[i] = sum([array[k-1]*array[i-k] for k in range(1,i+1)])
    return array[n]

print(nrBinTrees(4))

# O(w * (t * 2^w + e + v log v))