from enum import Enum
from typing import Union, Callable

DEBUG = True

def debug_print(msg):
    if DEBUG:
        print(msg)
    else:
        pass

class ProbingStragegy (Enum):
    LINEAR = 1,
    DOUBLE_HASHING = 2

class ChainedHashTable:
    def __init__(self, size : int, hash : Callable[[int], int]):
        self.SIZE = size
        self.table = [0] * size
        self.hash = hash

    def insert(self, key : int):
        h = self.hash(key)
        if self.table[h] == 0:
            self.table[h] = [key]

        

class OpenHashTable:
    def __init__(self, size : int, 
                 primary_hash : Callable[[int], int], 
                 probing_strategy : ProbingStragegy, 
                 secondary_hash : Union[Callable[[int], int], None] = None):
        self.SIZE = size
        self.table = [None] * size
        self.probing_strategy = probing_strategy
        self.primary_hash = primary_hash
        if probing_strategy == ProbingStragegy.LINEAR:
            self.hash = lambda k, i: (self.primary_hash(k) + i ) % self.SIZE
        if probing_strategy == ProbingStragegy.DOUBLE_HASHING:
            self.secondary_hash = secondary_hash
            self.hash = lambda k, i: (self.primary_hash(k) + i * self.secondary_hash(k)) % self.SIZE
    
    def insert(self, key : int):
        i = 0
        debug_print(f'h({key}, {i}) = {self.hash(key,i)}')
        while self.table[self.hash(key,i)] != None:
            debug_print(f'index is already taken, increase i to {i+1}')
            i += 1
            debug_print(f'h({key}, {i}) = {self.hash(key,i)}')
        debug_print('index not taken, insert:')
        self.table[self.hash(key,i)] = key
        debug_print(f'table[{self.hash(key,i)}] <- {key}')

m = 13
hashA = lambda x : (3*x + 1) % 13
hashTableA = OpenHashTable(size=m,primary_hash=hashA,probing_strategy=ProbingStragegy.LINEAR)

hashB_primary   = hashA
hashB_secondary = lambda x : x % 15
hashTableB = OpenHashTable(size=m, primary_hash=hashB_primary, probing_strategy=ProbingStragegy.DOUBLE_HASHING, secondary_hash=hashB_secondary)

debug_print("hash table A:")
for k in [8, 12, 40, 13, 88, 45, 29, 20, 23, 77]:
    hashTableA.insert(k)

for i in range(m):
    print(f'{i} \t | {hashTableA.table[i]} \t |')

debug_print("hash table B:")
for k in [8, 12, 40, 13, 88, 45, 29, 20, 23, 77]:
    hashTableB.insert(k)

for i in range(m):
    print(f'{i} \t | {hashTableB.table[i]} \t |')