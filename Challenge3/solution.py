import itertools


def count_inversions(arr):
    count = 0
    for i in range(len(arr)):
        for n in arr[i + 1:]:
            if n < arr[i] and n != 0:
                count = count + 1
    return count


def check_zero(arr):
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == 0:
                if i % 2 == 0:
                    return True
                else:
                    return False


def to_table(arr, size):
    table = tuple(arr[n:n + size] for n in range(0, len(arr), size))
    return table


def solvable_tiles(size=3):
    tiles_perm = itertools.permutations(range(size**2))
    if size % 2 == 1:
        for elem in tiles_perm:
            if count_inversions(elem) % 2 == 0:
                yield to_table(elem, size)
    elif size % 2 == 0:
        for elem in tiles_perm:
            if check_zero(to_table(elem, size)) and \
                    count_inversions(elem) % 2 == 1:
                yield to_table(elem, size)
            if not check_zero(to_table(elem, size)) and \
                    count_inversions(elem) % 2 == 0:
                yield to_table(elem, size)


sol = solvable_tiles(2)
print(next(sol))
