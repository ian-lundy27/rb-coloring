import numpy as np
import math
from PIL import Image
from check import coloring
from rbcsv import Colorings


def get_colors(r: int):
    colors = [
        (100,0,0),
        (0,100,0),
        (0,0,100),
        (160,160,0),
        (160,0,160),
        (0,160,160)
    ]
    used = set(colors)
    if r <= len(colors):
        return colors[:r]
    while len(colors) < r:
        new = tuple(np.random.randint(0,256,3))
        if new not in used:
            used.add(new)
            colors.append(new)
    return colors


def to_arr(p: int, q: int, coloring: list[set]):
    colors = get_colors(len(coloring))
    _colors = colors.copy()

    arr = np.zeros((p, q, 3), dtype=np.uint8)
    for s in coloring:
        color = colors.pop()
        for v in s:
            arr[v % p, math.floor(v/p)] = color

    _arr = np.zeros((q, p, 3), dtype=np.uint8)
    for s in coloring:
        color = _colors.pop()
        for v in s:
            _arr[v % q, math.floor(v/q)] = color
    
    return arr, _arr


if __name__=="__main__":
    # c = Colorings()
    p, q, scalar = 9, 25, 20
    # coloring = c.coloring(p * q)

    coloring = [
        {0},
        {1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24, 26, 27, 28, 29, 31, 32, 33, 34, 36, 37, 38, 39, 41, 42, 43, 44, 46, 47, 48, 49, 51, 52, 53, 54, 56, 57, 58, 59, 61, 62, 63, 64, 66, 67, 68, 69, 71, 72, 73, 74, 76, 77, 78, 79, 81, 82, 83, 84, 86, 87, 88, 89, 91, 92, 93, 94, 96, 97, 98, 99, 101, 102, 103, 104, 106, 107, 108, 109, 111, 112, 113, 114, 116, 117, 118, 119, 121, 122, 123, 124, 126, 127, 128, 129, 131, 132, 133, 134, 136, 137, 138, 139, 141, 142, 143, 144, 146, 147, 148, 149, 151, 152, 153, 154, 156, 157, 158, 159, 161, 162, 163, 164, 166, 167, 168, 169, 171, 172, 173, 174, 176, 177, 178, 179, 181, 182, 183, 184, 186, 187, 188, 189, 191, 192, 193, 194, 196, 197, 198, 199, 201, 202, 203, 204, 206, 207, 208, 209, 211, 212, 213, 214, 216, 217, 218, 219, 221, 222, 223, 224},
        {75, 150},
        {130, 5, 10, 140, 145, 20, 25, 155, 160, 35, 40, 170, 175, 50, 55, 185, 190, 65, 70, 200, 205, 80, 85, 215, 220, 95, 100, 110, 115, 125},
        {90, 135},
        {210, 15},
        {195, 30},
        {120, 105},
        {180, 45},
        {60, 165},
    ]

    # p,q = 3,5
    # n=p**2*q**2
    
    # colors = [
    #     {0},
    # ]
    # for i in range(p*q,round((n+1)/2),p*q):
    #     colors.append({i,n-i})
    # # print(colors)
    # colors.append(set())
    # for i in range(q,n,q):
    #     if i % p == 0: continue
    #     colors[-1].add(i)
    # # print(colors)
    # # print(check(n, coloring(*colors, n=n)))
    # colors = coloring(*colors, n=n)
    # print(len(colors))

    # coloring = colors
    # p,q = p**2,q**2
    arr = to_arr(p,q,coloring)
    img1, img2 = Image.fromarray(arr[0]).resize((q * scalar, p * scalar), resample=Image.Resampling.NEAREST), Image.fromarray(arr[1]).resize((p * scalar, q * scalar), resample=Image.Resampling.NEAREST)
    # img1.save(f"./images/{p*q}_{p}x{q}.jpg")
    img2.save(f"./images/{p*q}_{q}x{p}.jpg")