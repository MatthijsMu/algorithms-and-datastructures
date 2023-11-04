def volume(box):
    return box[0]*box[1]*box[2]

def fitsIn(boxA, boxB):
    return boxA[0] < boxB[0] and boxA[1] < boxB[1] and boxA[2] < boxB[2]

def boxNest():
    n = int(input())
    boxes = []
    for _ in range(n):
        [x,y,z] = input().split()
        x = float(x)
        y = float(y)
        z = float(z)
        boxes.append(tuple(sorted([x,y,z])))

    boxes = sorted(boxes)
    
    chains = []
    for box in boxes:
        added_to_chain = False
        for chain in reversed(chains):
            if fitsIn(chain[-1], box):
                chain.append(box)
                added_to_chain = True
                break
        if not added_to_chain:
            chains.append([box])

    return len(chains)

# Main code:
print(boxNest()) 