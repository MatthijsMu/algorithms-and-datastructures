def findMinChainPartition(rel, topologically_sorted_poset):
    if not topologically_sorted_poset:
        return []
    else:
        minimal_element = topologically_sorted_poset[0]
        inductive_partition = findMinChainPartition(rel, topologically_sorted_poset[1:])

        minimal_element_fits_somewhere = False

        for chain in inductive_partition:
            if rel(minimal_element, chain[0]):
                chain.insert(0,minimal_element)
                minimal_element_fits_somewhere = True
                break

        if not minimal_element_fits_somewhere:
            inductive_partition.append([minimal_element])

        return inductive_partition

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
    partition = findMinChainPartition(fitsIn, boxes)

    print(len(partition), partition)

main()