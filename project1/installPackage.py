def findMaxPackage(P):
    Q1 = P[:(len(P) - 1)//2]
    Q2 = P[(len(P) - 1)//2:]

    if install(Q1) == fail:
        Q1' = findMaxPackage(Q1)
    else:
        Q1' = Q2

    if install(Q2) == fail:
        Q2' = findMaxPackage(Q2)
    else:
        Q2' = Q2
    
    return Union(Q1', Q2')