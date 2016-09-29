import re
from typing import List, Tuple

import numpy as np
from PIL import Image

import vangers_utils.image.palette


def from_bytes(b: bytes, width: int, height: int, palette: List[int]=None)->Image:
    im = Image.frombytes('L', (width, height), b)
    im.putpalette(palette or vangers_utils.image.palette.PALETTE)
    return im.convert('RGBA')


def replace_transparent(image: Image, transparent_color: Tuple[int, int, int, int])->Image:
    replacement_color = (0, 0, 0, 0)
    data = np.array(image)
    data[(data == transparent_color).all(axis=-1)] = replacement_color
    return Image.fromarray(data, mode='RGBA')


def get_meta_filename(filename: str)->str:
    return re.sub(r'^(.*)\.\w+$', r'\g<1>.meta.yaml', filename)

