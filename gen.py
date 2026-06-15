from check import check
from time import time
import numpy as np
import sys


def class_sizes(n: int, colors: int, mod: bool = True):

    def narr(i: int, pos: int, arr: np.ndarray):
        if pos == colors:
            yield arr
        else:
            for i in range(i, n - colors + pos + 2):
                arr[pos] = i                            # Set value at this pos. to new value
                yield from narr(i + 1, pos + 1, arr)    # Move on to position and repeat

    if mod:
        n -= 1                                          # Change min and max value when working mod n
        return narr(1,1,np.zeros(colors, dtype=int))    # Start at pos. 1 (skipping 0 since always min)
    else:
        return narr(2,1,np.ones(colors, dtype=int))
    

def color_in(n: int, arr: np.ndarray, mod = True):  # Regular coloring
    colors = arr.shape[0]
    def _color(i: int, sets: list[set]):
        if i > n:       # All numbers have been placed
            yield sets
        elif i in arr:  # Value used as one of the minimums
            yield from _color(i + 1, sets)
        else:    
            for j in range(colors):
                if i < arr[j]:  # i < min, skip this color
                    continue
                _sets = sets.copy()                 # Shallow copy so sets on other branches aren't affected
                _sets[j] = sets[j].copy()           # Replace only this color's set with a copy to allow safe modification
                _sets[j].add(i)                     # Color value
                yield from _color(i + 1, _sets)     # Continue at next int

    if mod:
        n -= 1  # Shifting bounds from 1 thru n to 0 thru n-1
    yield from _color(1 if mod else 2, list([{int(s)} for s in arr]))


if __name__=="__main__":
    # Hardcoded state
    n, c = 12, 4

    # Take input from CLI if given
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    if len(sys.argv) > 2:
        c = int(sys.argv[2])

    i = 0
    t = time()

    print(f"Checking {n} in {c} colors")

    for s in class_sizes(n,c):
        for coloring in color_in(n, s):
            if not check(n, coloring):
                print(f"{coloring}")
                i += 1

    print(f"Found {i} such colorings for {n} in {round(time() - t,2)}s")