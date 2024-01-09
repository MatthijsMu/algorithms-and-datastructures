def mostFrequent4(document : list[str]) -> int :
    count : dict[str] = dict()           # n times
    for word in document:
        if word in count:    # this is, in pseudo-code, a LOOKUP, O(1)
            count[word] += 1 # this is INSERT, O(1)
        else:
            count[word] = 1
    # topFour is the list of top 4 most frequent words,
    # sorted on frequency where topFour[0] is most frequent.
    topFour : list[str] = []
    for word in document:
        if word not in topFour: # O(4) checks for equality, so constant time!
            topFour.append(word)
            i = len(topFour) - 1 # this is 4 once topFour is saturated, but it starts out empty
            while i > 0: # O(4) = O(1) iterations
                if count[topFour[i]] > count[topFour[i-1]]: # two O(1) lookups, O(1) comparisons and O(1) swaps.
                    topFour[i], topFour[i-1] = topFour[i-1], topFour[i]
                    i -= 1
                else: break
            if len(topFour) > 4:
                topFour.pop()
    return topFour

document = ["Hello", "World", "cheese", "cheese", "cheese", "eggs", "ham", "ham", "onion", "youtube", "onion", "World", "World"]
print (mostFrequent4(document))