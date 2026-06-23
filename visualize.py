import numpy as np
import math
from PIL import Image

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
        print(new, type(new))
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
    c = Colorings()
    p, q, scalar = 11, 13, 100
    coloring = c.coloring(p * q)
    arr = to_arr(p,q,coloring)
    img1, img2 = Image.fromarray(arr[0]).resize((q * scalar, p * scalar), resample=Image.Resampling.NEAREST), Image.fromarray(arr[1]).resize((p * scalar, q * scalar), resample=Image.Resampling.NEAREST)
    img1.save(f"./images/{p*q}_{p}x{q}.jpg")
    img2.save(f"./images/{p*q}_{q}x{p}.jpg")