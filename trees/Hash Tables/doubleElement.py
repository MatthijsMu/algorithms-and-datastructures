from typing import Hashable

def doubleElement(A : list[Hashable]):
    T = set() 

    for a in A:
        if a not in T:
            T.add(a)
        else:
            return True

    return False