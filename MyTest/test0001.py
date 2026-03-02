import itertools

a = [[1, 2, 3], [5, 2, 8], [7, 8, 9]]
print(list(itertools.chain.from_iterable(a)))

