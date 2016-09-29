from typing import List, Tuple
import numpy as np
from PIL import Image
import re

from vangers_utils.image import config


def from_bytes(b: bytes, width: int, height: int, palette: List[int]=None)->Image:
    im = Image.frombytes('L', (width, height), b)
    im.putpalette(palette or config.PALETTE_2)
    return im.convert('RGBA')


def replace_transparent(image: Image, transparent_color: Tuple[int, int, int, int])->Image:
    replacement_color = (0, 0, 0, 0)
    data = np.array(image)
    data[(data == transparent_color).all(axis=-1)] = replacement_color
    return Image.fromarray(data, mode='RGBA')


def get_meta_filename(filename: str)->str:
    return re.sub(r'^(.*)\.\w+$', r'\g<1>.meta.yaml', filename)
