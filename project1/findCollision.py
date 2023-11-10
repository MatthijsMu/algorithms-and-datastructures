def findCollision(shift, arr):
    n = len(arr)
    if n == 0:
        return False, None
    
    else:
        h = n//2
        if arr[h] == shift + h:
            return True, shift + h
        if arr[h] < shift +  h:
            return findCollision(shift + h + 1, arr[h + 1:])
        else:
            return findCollision(shift, arr[:h])
        
found = findCollision(0, sorted([-2, -1,1,2,3,4,5,6,7,9]))
print(found)

# returns x if there is an integer x such that arr[x] == x. Assumes a sorted array of 
# distinct elements. Runs in O(log n) where n = len(arr)

# We can extract tail-recursion and transform into equivalent while-loop:
def findCollision_(shift, arr):
    n = len(arr)
    while not n == 0:
        h = n//2
        if arr[h] == shift + h:
            return True, shift + h
        if arr[h] < shift +  h:
            shift += h+1
            arr = arr[h+1:]
        else:
            arr = arr[:h]
            
    return False, None