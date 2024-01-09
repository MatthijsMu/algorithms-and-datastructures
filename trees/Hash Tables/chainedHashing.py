DEBUG = True

def debug_print(msg):
    if DEBUG:
        print(msg)
    else:
        pass

class ChainedHashTable:
    def __init__(self, size : int, hash_function : Callable[[int], int]):
        self.SIZE = size 
        self.table = [None] * self.SIZE
        self.hash = hash_function

    def insert(self, key : int):
        debug_print(f'h({key}) = {self.hash(key)}')
        h = self.hash(key)
        if self.table[h] == 0:
            debug_print('index not taken, insert:')
            self.table[h] = [key]
            debug_print(f'table[{self.hash(key,i)}] <- {key}')
        else:
          debug_print(f'index is already taken, chain:')
          self.table[h].append(key)
          debug_print(f'table[{h}] -> {self.table[h]}')
            

        
