def minChains(relP, poset, relQ=id):
    return pickChains(relP,sorted(poset, key=relQ))

def pickChains(relP, topologically_sorted_poset):
    if not topologically_sorted_poset:
        return []
    else:
        chain, remainder = pickChain(relP, [topologically_sorted_poset[0]], topologically_sorted_poset[1:])
        return [chain] + pickChains(relP, remainder)
    
def pickChain(relP, ch, slc):
    if not slc:
        return ch, []
    else:
        if relP(ch[-1], slc[0]):
            return pickChain(relP, ch + [slc[0]], slc[1:])
        else:
            chain, remainder = pickChain(relP, ch, slc[1:])
            return chain, [slc[0]] + remainder

def fitsIn(boxA, boxB):
    return boxA[0] < boxB[0] and boxA[1] < boxB[1] and boxA[2] < boxB[2]

def inputBoxes():
    n = int(input())
    boxes = []
    for _ in range(n):
        [x,y,z] = input().split()
        x = float(x)
        y = float(y)
        z = float(z)
        boxes.append(tuple(sorted([x,y,z])))

    return boxes


def main():
    boxes = inputBoxes()
    boxes = sorted(boxes)
    partition = minChains(fitsIn, boxes)

    print(len(partition))

main()