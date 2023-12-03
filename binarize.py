from itertools import product

def __binary_tuples(nr_digits):
        return [tuple((j % (2**(i+1))) // (2**i) for i in range(nr_digits)) for j in range(2**nr_digits)]

print(__binary_tuples(6))
