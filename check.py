from itertools import combinations, product
from typing import Callable, Iterable
from rbcsv import Colorings, ColoringsK


def check(n: int, sets: list[set], func: Callable = None, all: bool = False, power: int = 2):
    # Returns False if no coloring is found, otherwise returns valid triple (or whatever the callback returns)
    if func: # Only works with triples
        return _check(sets, func)
    
    # Get all solutions, only supported by default eq. x+y=z^2
    if all:
        arr = []

    # Ridiculously inefficient brute force approach
    # Much room for optimization wrt combining coloring and checking in order to do exhaustive search better
    # Mainly useful for getting many examples of colorings instead of one, only feasible on small n
    colors = len(sets)

    # Compute all squares for each color
    squares = list([set() for i in sets])
    for i in range(colors):
        for j in sets[i]:
            squares[i].add((j ** power) % n)

    # Plug in every triple to check for rainbow solution
    for i in range(colors):     # This is our z color
        _sets = sets.copy()
        _sets.pop(i)            # Get set of remaining colors
        for s1, s2 in combinations(_sets, 2):   # Grab every pair of sets
            for x,y in product(s1, s2):
                if (x + y) % n in squares[i]:   # If any produce a square we've computed, it's a solution
                    z = _recover(n, sets[i], (x + y) % n, power)
                    if all:
                        arr.append((x, y, z))
                    else:
                        return (x, y, z)
    
    return arr if all else False


def _recover(n: int, s: set[int], v: int, power: int):
    # Gets a valid root of the quadratic residue, not necessarily unique
    for i in s:
        if (i ** power) % n == v:
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


def symmetry(n: int, sets: list[set]):
    result = list([True for i in range(len(sets))])
    for i in range(len(sets)):
        for j in sets[i]:
            if (-j) % n not in sets[i]:
                result[i] = False
                break
    return result


def store(sets: list[set]):
    return frozenset([frozenset(s) for s in sets])
        

if __name__=="__main__":
    # colors = coloring({2, 3, 4, 5, 6, 9, 10, 13, 14, 15, 16, 17}, {8, 11, 12, 7}, {1, 18})
    # print(check(19, colors))
    # c = ColoringsK()
    # color = c.coloring(103,51)
    # color.pop(-3)
    # print(color)
    # color.append({24,78})
    # color.append({22,80})
    # print(check(103,color,power=51))

    # color = [{0, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 50, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 69, 70, 71, 72, 73, 75, 77, 78, 79, 80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 94, 95, 96, 97, 98, 102, 103, 104, 105, 106, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 119, 120, 121, 122, 123, 125, 127, 128, 129, 130, 131, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 144, 145, 146, 147, 148, 152, 153, 154, 155, 156, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 169, 170, 171, 172, 173, 175, 177, 178, 179, 180, 181, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 194, 195, 196, 197, 198, 200, 202, 203, 204, 205, 206, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 219, 220, 221, 222, 223, 227, 228, 229, 230, 231, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 244, 245, 246, 247, 248, 250, 252, 253, 254, 255, 256, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 269, 270, 271, 272, 273, 277, 278, 279, 280, 281, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 294, 295, 296, 297, 298, 300, 302, 303, 304, 305, 306, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 319, 320, 321, 322, 323, 325, 327, 328, 329, 330, 331, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 344, 345, 346, 347, 348, 352, 353, 354, 355, 356, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 369, 370, 371, 372, 373, 375, 377, 378, 379, 380, 381, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 394, 395, 396, 397, 398, 402, 403, 404, 405, 406, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 419, 420, 421, 422, 423, 425, 427, 428, 429, 430, 431, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 444, 445, 446, 447, 448, 450, 452, 453, 454, 455, 456, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 469, 470, 471, 472, 473, 477, 478, 479, 480, 481, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 494, 495, 496, 497, 498, 500, 502, 503, 504, 505, 506, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 519, 520, 521, 522, 523, 527, 528, 529, 530, 531, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 544, 545, 546, 547, 548, 550, 552, 553, 554, 555, 556, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 569, 570, 571, 572, 573, 575, 577, 578, 579, 580, 581, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 594, 595, 596, 597, 598, 602, 603, 604, 605, 606, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 619, 620, 621, 622, 623},
    # {1, 518, 7, 524, 526, 18, 532, 24, 26, 543, 32, 549, 551, 43, 557, 49, 51, 568, 57, 574, 576, 68, 582, 74, 76, 593, 82, 599, 601, 93, 607, 99, 101, 618, 107, 624, 118, 124, 126, 132, 143, 149, 151, 157, 168, 174, 176, 182, 193, 199, 201, 207, 218, 224, 226, 232, 243, 249, 251, 257, 268, 274, 276, 282, 293, 299, 301, 307, 318, 324, 326, 332, 343, 349, 351, 357, 368, 374, 376, 382, 393, 399, 401, 407, 418, 424, 426, 432, 443, 449, 451, 457, 468, 474, 476, 482, 493, 499, 501, 507},
    # {100, 525},
    # {600, 25},
    # {275, 350},
    # {400, 225},
    # {475, 150}]

    # print(check(625,color))

    c = Colorings()
    color = c.coloring(27)
    print(color)

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