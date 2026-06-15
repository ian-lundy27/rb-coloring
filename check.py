from itertools import combinations, product
from typing import Callable, Iterable


def check(n: int, sets: list[set], func: Callable = None):
    # Returns False if no coloring is found, otherwise returns valid triple (or whatever the callback returns)
    if func: # Only works with triples
        return _check(sets, func)

    # Ridiculously inefficient brute force approach
    # Much room for optimization wrt combining coloring and checking in order to do exhaustive search better
    # Mainly useful for getting many examples of colorings instead of one, only feasible on small n
    colors = len(sets)

    # Compute all squares for each color
    squares = list([set() for i in sets])
    for i in range(colors):
        for j in sets[i]:
            squares[i].add((j ** 2) % n)

    # Plug in every triple to check for rainbow solution
    for i in range(colors):     # This is our z color
        _sets = sets.copy()
        _sets.pop(i)            # Get set of remaining colors
        for s1, s2 in combinations(_sets, 2):   # Grab every pair of sets
            for x,y in product(s1, s2):
                if (x + y) % n in squares[i]:   # If any produce a square we've computed, it's a solution
                    z = _recover(n, sets[i], (x + y) % n)
                    return (x, y, z)
    
    return False

def _recover(n: int, s: set[int], v: int):
    # Gets a valid root of the quadratic residue, not necessarily unique
    for i in s:
        if (i ** 2) % n == v:
            return i
                    
def _check(sets: list[set], func: Callable):
    # Less efficient, but custom. Doesn't consider commutativity
    for i in range(len(sets)):
        _sets = sets.copy()
        _sets.pop(i)
        for s1, s2, s3 in combinations(_sets, 3):
            for x, y, z in product(s1, s2, s3):
                if (func(x,y,z)):
                    return True, x, y, z
        return False
    
def coloring(*colors: Iterable, n: int = 0):
    # Converts groups of numbers into a list of sets used by other functions
    # Optional arg n will add all unused numbers <n into their own distinct color
    sets = list([set(color) for color in colors])
    if n:
        union = set()
        for s in sets:
            union.update(s)
        sets.append({i for i in range(n) if i not in union})
    return sets


if __name__=="__main__":
    colors = coloring({2, 3, 4, 5, 6, 9, 10, 13, 14, 15, 16, 17}, {8, 11, 12, 7}, {1, 18})
    print(check(19, colors))