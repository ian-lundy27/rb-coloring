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

    '''
    n=343,c=6
    coloring = [
        {0, 98, 196, 294, 49, 147, 245},
        {1, 6, 8, 13, 15, 20, 22, 27, 29, 34, 36, 41, 43, 48, 50, 55, 57, 62, 64, 69, 71, 76, 78, 83, 85, 90, 92, 97, 99, 104, 106, 111, 113, 118, 120, 125, 127, 132, 134, 139, 141, 146, 148, 153, 155, 160, 162, 167, 169, 174, 176, 181, 183, 188, 190, 195, 197, 202, 204, 209, 211, 216, 218, 223, 225, 230, 232, 237, 239, 244, 246, 251, 253, 258, 260, 265, 267, 272, 274, 279, 281, 286, 288, 293, 295, 300, 302, 307, 309, 314, 316, 321, 323, 328, 330, 335, 337, 342},
        {2, 3, 4, 5, 9, 10, 11, 12, 16, 17, 18, 19, 23, 24, 25, 26, 30, 31, 32, 33, 37, 38, 39, 40, 44, 45, 46, 47, 51, 52, 53, 54, 58, 59, 60, 61, 65, 66, 67, 68, 72, 73, 74, 75, 79, 80, 81, 82, 86, 87, 88, 89, 93, 94, 95, 96, 100, 101, 102, 103, 107, 108, 109, 110, 114, 115, 116, 117, 121, 122, 123, 124, 128, 129, 130, 131, 135, 136, 137, 138, 142, 143, 144, 145, 149, 150, 151, 152, 156, 157, 158, 159, 163, 164, 165, 166, 170, 171, 172, 173, 177, 178, 179, 180, 184, 185, 186, 187, 191, 192, 193, 194, 198, 199, 200, 201, 205, 206, 207, 208, 212, 213, 214, 215, 219, 220, 221, 222, 226, 227, 228, 229, 233, 234, 235, 236, 240, 241, 242, 243, 247, 248, 249, 250, 254, 255, 256, 257, 261, 262, 263, 264, 268, 269, 270, 271, 275, 276, 277, 278, 282, 283, 284, 285, 289, 290, 291, 292, 296, 297, 298, 299, 303, 304, 305, 306, 310, 311, 312, 313, 317, 318, 319, 320, 324, 325, 326, 327, 331, 332, 333, 334, 338, 339, 340, 341},
        {161, 35, 259, 133, 231, 329, 14, 112, 210, 84, 308, 182, 280, 63},
        {7, 105, 42, 203, 140, 301, 238, 336, 56, 154, 91, 252, 189, 287},
        {224, 322, 70, 168, 266, 77, 175, 273, 21, 119, 217, 315, 28, 126},
    ]
    '''