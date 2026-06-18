from itertools import permutations
from pysat.formula import CNF, IDPool
from pysat.solvers import Glucose42, Solver
from time import time
from check import symmetry
import pandas as pd
import sys


def solutions(n: int):
    # Generates all solutions up to commutativity
    for x in range(n - 2):
        for y in range(x + 1, n - 1):
            for z in range(y + 1 ,n):
                if (x + y - z ** 2) % n == 0 or (x + z - y ** 2) % n == 0 or (y + z - x ** 2) % n == 0:
                    yield x,y,z


def _id(pool: IDPool, i: int, color: int):
        # Generate/get ids for all int,color pairs
        return pool.id((i, color))


def pool_to_colors(pool: IDPool, solver: Solver):
    # If solution found, reconstruct color sets
    model = set(solver.get_model())
    colors = list([set() for i in range(c)])
    for i in range(n):
        for color in range(min(i + 1,c)):
            if _id(pool, i, color) in model:
                colors[color].add(i)
    return colors


def setup(n: int, c: int, zero_non_unique: bool = False):
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
        for triple in solutions(n):     # For EVERY triple (including x+y=z^2 and y+x=z^2) 
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


if __name__=="__main__":
    # Gets VERY slow as number of colors increases, since every 3-permutation of colors is used for each (x,y,z) soln.

    # Hardcoded state
    n, c, count = 289, 5, False

    # Take input from CLI if given
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    if len(sys.argv) > 2:
        c = int(sys.argv[2])
    if len(sys.argv) > 3:
        count = sys.argv[3] in ("-count","-c")
        _all = sys.argv[3] in ("-all","-a")

    t = time()

    print(f"Setting up {c}-coloring of {n}...", end=" ", flush=True)
    prelim = setup(n, c)

    print("Solving...", end=" ", flush=True)
    solution, solver, pool = solve(*prelim, Glucose42(use_timer=True))

    if count or _all:   # If we want to count all possible rainbow-free colorings
        i = 0
        colors = pool_to_colors(pool, solver) if solution else False
        colors.sort(key=len)
        if _all:
            print()
            for color in colors:
                print(color)
        while solution:
            i += 1
            solution = newsolve(solver)
            if solution and _all:
                colors = pool_to_colors(pool, solver)
                colors.sort(key=len)
                print()
                for color in colors:
                    print(color)
  
        print(f"Found {i} solutions in {round(solver.time(), 2)}s. Total time: {round(time() - t,2)}s. ",end="")
        if count and colors:
            print("Example coloring:")
            for color in colors:
                print(color)

    elif solution:  # Not counting all, just looking for a single rainbow-free coloring
        print(f"Found a solution in {round(solver.time(), 2)}s. Total time: {round(time() - t,2)}s. Coloring:")
        for color in pool_to_colors(pool, solver):
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
                        best = pool_to_colors(pool, solver)
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