import array
from glob import glob
from os.path import join, dirname, basename
from typing import Tuple, List, Dict

import numpy as np


def bit(x, n):
    return (x & (1 << n)) >> n


def tobin(x):
    r = "{0:b}".format(x)
    #     return r
    return ('0' * (8 - len(r))) + r


def scale(x, mask, color_name):
    l = sum(c == color_name for c in mask)
    m = 2 ** l
    return int(255 * ((x) / (m - 1)))


def palette_color(value, mask):
    colori = {
        'r': 0,
        'g': 0,
        'b': 0
    }

    for i, m in enumerate(mask):
        if m not in {'r', 'g', 'b'}:
            continue

        v = bit(value, len(mask) - i - 1)
        #     color[m] = color[m] + str(v)
        colori[m] = colori[m] * 2 + v

    # print(colori)
    r = scale(colori['r'], mask, 'r')
    g = scale(colori['g'], mask, 'g')
    b = scale(colori['b'], mask, 'b')
    return (r, g, b)


def make_palette(mask):
    palette = []
    for x in range(256):
        xs = tobin(x)
        (rc, gc, bc) = palette_color(x, mask)
        c = int((rc + gc + bc) / 3)
        palette.append(c)
        palette.append(c)
        palette.append(c)
    return palette


def color_index(c: Tuple[int, int, int])->int:
    r, g, b = c
    return b + 256 * g + 256 * 256 * r


def create_palette_mapping(pal: List[int])->Dict[int, np.uint8]:
    res = {}  # type: Dict[int, np.uint8]
    for i in range(0, len(pal), 3):
        r, g, b = pal[i], pal[i + 1], pal[i + 2]
        index = color_index((r, g, b))
        if index in res:
            continue
        res[index] = np.uint8(i // 3)

    return res


def read_palette_from_file(filename: str) -> List[int]:
    with open(filename, 'rb') as f:
        a = array.array('B')
        a.fromfile(f, 768)
        pal = a.tolist()
        return [c * 2 for c in pal]


def read_palette(palette_name: str) -> List[int]:
    filename = join(dirname(__file__), 'data', 'pal', '{}.pal'.format(palette_name))
    return read_palette_from_file(filename)


def list_palette_names() -> List[str]:
    files = glob(join(dirname(__file__), 'data', 'pal', '*.pal'))
    return [
        basename(file)[:-4]
        for file in files
    ]

