from itertools import permutations
from pysat.formula import CNF, IDPool
from pysat.solvers import Glucose42, Solver
from time import time
from datetime import datetime
from check import store, symmetry
from sympy import nextprime
import pandas as pd
import sys
import argparse


def solutions(n: int, power: int = 2):
    # Generates all solutions up to commutativity
    for x in range(n - 2):
        for y in range(x + 1, n - 1):
            for z in range(y + 1 ,n):
                if (x + y - z ** power) % n == 0 or (x + z - y ** power) % n == 0 or (y + z - x ** power) % n == 0:
                    yield x,y,z


def _id(pool: IDPool, i: int, color: int):
        # Generate/get ids for all int,color pairs
        return pool.id((i, color))


def pool_to_colors(n: int, c: int, pool: IDPool, solver: Solver):
    # If solution found, reconstruct color sets
    model = set(solver.get_model())
    colors = list([set() for i in range(c)])
    for i in range(n):
        for color in range(min(i + 1,c)):
            if _id(pool, i, color) in model:
                colors[color].add(i)
    return colors


def setup(n: int, c: int, zero_non_unique: bool = False, power: int = 2):
    cnf, pool = CNF(), IDPool()
    id = lambda i, color: _id(pool, i, color)

    def monochromatic():
        # Sets integer coloring constraint (exactly one color per int)
        for i in range(n):
            ids = [id(i, color) for color in range(min(i+1,c))]
            cnf.append(ids)     # At least one of (i,color) must be used
            for j in range(min(i+1,c)):
                for k in range(j + 1,min(i+1,c)):
                    cnf.append([-ids[j], -ids[k]])  # At most one color is used for i
    
    def exact():
        # Exact solution (all colors used)
        for color in range(c):
            # At least one i must be colored this color
            cnf.append([id(i, color) for i in range(color,n)])
        
    def encode_solutions():
        # Exclude each solution
        # This feels really inefficient
        def encode_solution(x: int, y: int, z: int):
            for c1, c2, c3 in permutations(range(c), 3):    # Every color combo can give rb solution
                if x < c1 or y < c2 or z < c3:
                    continue    # Skip any cases where we would assign an int to a greater color index (avoiding for ?efficiency?)
                cnf.append([    # Not all three in the triple can be in distinct colors
                    -id(x, c1),
                    -id(y, c2),
                    -id(z, c3)
                ])
        for triple in solutions(n, power):     # For EVERY triple (including x+y=z^2 and y+x=z^2) 
            encode_solution(*triple)    # we add clauses for EVERY color triple as well :(

    def zero_not_unique():
        # Exclude any solution where 0 is alone in its color class
        # Force at least one of 1...n to be in color 0, which we force 0 into
        cnf.append([id(i, 0) for i in range(1,n)])

    monochromatic()
    exact()
    encode_solutions()
    if zero_non_unique: zero_not_unique()
    return cnf, pool


def solve(cnf: CNF, pool: IDPool, solver: Solver):
    for clause in cnf.clauses:
        solver.add_clause(clause)
    result = solver.solve()
    return result, solver, pool

def newsolve(solver: Solver):
    solver.add_clause([-i for i in solver.get_model()])
    return solver.solve()


def get_from_csv(i: int, filepath: str = "rb.csv", delim: str = ";"):
    # Get the coloring sets for any number that's been calculated
    df: pd.DataFrame = pd.read_csv(filepath, delimeter=delim)
    set_str = df[df.iloc[:,2] == i].iloc[0, 2][1:-1]    # Grab row/col we are looking for
    set_list = set_str[1:-2].replace(" ","").replace("{","").split("},")  # Split each set in list into csv
    for i in range(len(set_list)):
        s = set_list[i].split(",")
        set_list[i] = set([int(i) for i in s])  # Map csv to list of ints, convert to set
    return set_list


def all_solutions(n: int, r: int):
    prelim = setup(n, r)
    solution, solver, pool = solve(*prelim, Glucose42(use_timer=True))
    while solution:
        coloring = pool_to_colors(n, r, pool, solver)
        coloring.sort(key=min)
        coloring.sort(key=len)
        yield coloring
        solution = newsolve(solver)


def rbk(filepath: str = "rbk.csv", log: bool = True, stop_at_half: bool = True):
    try:
        df = pd.read_csv(filepath, delimiter=";")
        p, k = int(df.iloc[-1, 0]), int(df.iloc[-1, 1]) + 1           # Grab last entry, inc. k value 
        if k >= p or (stop_at_half and k > (p - 1) / 2):    # If next k is too large, inc. p value
            p = nextprime(p)
            k = 2
    except FileNotFoundError: 
        with open(filepath, "w") as file:
            file.write("p;k;rb;coloring\n") # Write labels
        p, k = 5, 2                         # Initial values

    r = 4
    coloring = [{0}, {i for i in range(1,p)}]

    with open(filepath, "a") as file:       # Write each rb-# result as we get it
        try:
            while True:
                print(f"Trying {r}-coloring of {p}, power {k}... ", end="", flush=True)
                cnf, pool = setup(p, r, power=k)
                print(f"{len(cnf.clauses)} clauses... ", end="", flush=True)
                solution, solver, _ = solve(cnf, pool, Glucose42())

                if solution:    # Try again with +1 color
                    coloring = pool_to_colors(p, r, pool, solver)   # Save example of best coloring
                    print(f"Found {r}-coloring of {p}, power {k}", end="" if log else "\n")
                    r += 1
                    if log: print(f" at {datetime.now()}")
                    continue

                else:           # No rainbow-free colorings, save
                    print(f"Rainbow number {r} for {p}, power {k}", end="" if log else "\n")
                    if log: print(f" at {datetime.now()}")
                    file.write(f"{p};{k};{r};{coloring}\n")
                    file.flush()

                    r = 2               # Reset state
                    k += 1              # Update k
                    if k >= p or (stop_at_half and k > (p - 1) / 2):    # ^p-1 takes a long time, so skip to get more primes at ^p-1/2
                        p = nextprime(p)    # Update p/k, if applicable
                        k = 2
                    coloring = [{0},{i for i in range(1,p)}]

        except KeyboardInterrupt:
            print(f"Exited during {r}-coloring of {p}, power {k}")
            file.flush()

        '''rb(Z_127,x+y=z^63) >= 15'''


def parseargs():
    parser = argparse.ArgumentParser(description="Compute r-coloring mod n with equation x+y=z^k.")
    parser.add_argument("n", type=int, help="Modulus", nargs="?", default=13)
    parser.add_argument("r", type=int, help="Number of colors", nargs="?", default=3)
    parser.add_argument("-k","--power", type=int, action="store", default=2, help="Value of k in x+y=z^k")
    parser.add_argument("-c","--count", action="store_true", help="Print total number of rainbow-free r-colorings")
    parser.add_argument("-a","--all", action="store_true", help="Print each rainbow-free coloring, overrides count")
    parser.add_argument("-q","--quiet", action="store_true", help="Print std updates, skip color printouts")
    return parser.parse_args()

if __name__=="__main__":

    # Gets VERY slow as number of colors increases, since every 3-permutation of colors is used for each (x,y,z) soln.
    args = parseargs()

    # Hardcoded state
    n, c, count, _all, quiet = args.n, args.r, args.count, args.all, args.quiet

    t = time()

    print(f"Setting up {c}-coloring of {n}...", end=" ", flush=True)
    prelim = setup(n, c, power=args.power)

    print("Solving...", end=" ", flush=True)
    solution, solver, pool = solve(*prelim, Glucose42(use_timer=True))

    # This is a mess of logic :(
    if count or _all:   # If we want to count all possible rainbow-free colorings
        unique = set()
        i = 0
        colors = pool_to_colors(n, c, pool, solver) if solution else False
        if colors:
            i = 1
            unique.add(store(colors))
            colors.sort(key=len)
            if _all and not quiet:
                print()
                for color in colors:
                    print(color)
                print(symmetry(n,colors))
        while solution:
            solution = newsolve(solver)
            if solution:
                colors = pool_to_colors(n, c, pool, solver)
                s = store(colors)
                if s not in unique:
                    i += 1
                    unique.add(s)
                    colors.sort(key=len)
                    if _all and not quiet:
                        print()
                        for color in colors:
                            print(color)
                        print(symmetry(n,colors))

        print(f"Found {i} solutions in {round(solver.time(), 2)}s. Total time: {round(time() - t,2)}s. ",end="")
        if count and colors and not quiet:
            print("Example coloring:")
            for color in colors:
                print(color)

    elif solution:  # Not counting all, just looking for a single rainbow-free coloring
        print(f"Found a solution in {round(solver.time(), 2)}s. Total time: {round(time() - t,2)}s. {'Coloring:' if not quiet else ''}")
        if not quiet:
            for color in pool_to_colors(n, c, pool, solver):
                print(color)

    else:   # No rainbow-free colorings
        print(f"No valid coloring found in {round(solver.time(), 2)}s. Total time: {round(time() - t,2)}s.")

'''
    try:
        filepath = "rb.csv"
        df = pd.read_csv(filepath, delimiter=";")
        n = df.iloc[-1,0]
    except:
        n = 2


    with open(filepath, "a") as file:
        try:
            while True:
                n += 1
                print(n, datetime.now())
                c = 3
                best = []
                while True:
                    solution, solver, pool = solve(*setup(n,c), Glucose42(use_timer=True))
                    if solution:
                        best = pool_to_colors(n, c, pool, solver)
                        solver.delete()
                        c += 1
                        continue
                    else:
                        solver.delete() 
                        string = f"{n};{c};{best}\n"
                        file.write(string) # Number, rb(), rainbow-free
                        file.flush()
                        break
        except KeyboardInterrupt as e:
            file.flush()
            print(e)
            raise
'''