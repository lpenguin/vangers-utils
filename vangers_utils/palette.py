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
