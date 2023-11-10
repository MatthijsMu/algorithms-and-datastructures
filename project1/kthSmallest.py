def kthSmallest(k, Sa, Sb):
    n = len(Sa)
    m = len(Sb)

    # establish invariant: n <= m:
    if n > m:
        return kthSmallest(k, Sb, Sa)

    # establish requirement: k <= m + n:
    if k > m + n:
        return None
    
    # Base case:
    # k == 0 is the only strictly necessary base case. Other situations can be reduced by truncating and shifting operations
    if k == 0:
        return min(Sa[0], Sb[0])
    
    # We have k < m + n, n <= m.
    idxa = (n-1)//2
    idxb = (m-1)//2

    # let C = merge(Sa, Sb)

    # if idxa + idxb > k:
        # if Sa[idxa] > Sb[idxb], we know C[k] < Sa[idxa], and since Sa[idxa] <= Sa[l] for any l >= idxa , we can immediately discard Sa[idxa:]
        # if Sa[idxa] < Sb[idxb], we know C[k] < Sb[idxb], and since Sb[idxb] <= Sb[l] for any l >= idxb , we can immediately discard Sb[idxb:]
        # if Sa[idxa] = Sb[idxb], we know C[idxa + idxb] = C[idxa + idxb + 1] = Sa[idxa] = Sb[idxb], since when merging the elements Sa[idxa], Sb[idxb] 
        # will appear directly after each other and hence will be the k th, k+1 th elements of C respectively. This also means that we
        # can discard Sa[:idxa] and Sb[:idxb], but this requires to 

    # if idxa + idxb <= k:
        # if Sa[idxa] > Sb[idxb], we know C[k] > Sb[idxb], and since Sb[idxb] >= Sb[l] for any l <= idxb , we can discard Sa[:idxb+1], but we will have to shift the index k to keep track of the slice offset
        # if Sa[idxa] < Sb[idxb], we know C[k] > Sa[idxa], and since Sa[idxa] <= Sa[l] for any l <= idxa , we can discard Sb[:idxa+1], but we will have to shift the index k to keep track of the slice offset
        # if Sa[idxa] = Sb[idxb], we know C[idxa + idxb] = C[idxa + idxb + 1] = Sa[idxa] = Sb[idxb], since when merging the elements Sa[idxa], Sb[idxb] 
        # will appear directly after each other and hence will be the k th, k+1 th elements of C respectively.

    # We will always be able to discard half one of the two arrays, leading to an O(log n + log m) complexity


    if idxa + idxb <= k:
        if Sa[idxa] > Sb[idxb]:
            return kthSmallest(k - idxb - 1, Sa, Sb[idxb+1:])
        elif Sa[idxa] < Sb[idxb]:
            return kthSmallest(k - idxa - 1, Sa[idxa+1:], Sb)
        else:
            return kthSmallest(k - idxa - idxb, Sa[idxa:], Sb[idxb:])

    else:
        if Sa[idxa] > Sb[idxb]:
            return kthSmallest(k, Sa[:idxa], Sb)
        elif Sa[idxa] < Sb[idxb]:
            return kthSmallest(k, Sa, Sb[:idxb])
        else:
            return kthSmallest(k, Sa[:idxa], Sb[:idxb])

print(kthSmallest(9, [2,2,2,2,4,5,6,10,10,10,10],[2,4,9,10,10,10,10,10,10]))