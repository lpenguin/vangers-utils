import numpy as np
from PIL import Image

from vangers_utils import config


def from_bytes(b: bytes, width: int, height: int, palette: str=None)->Image:
    im = Image.frombytes('L', (width, height), b)
    im.putpalette(palette or config.PALETTE)
    return im.convert('RGBA')


def replace_transparent(image: Image)->Image:
    transparent_color = (32, 76, 32, 255)
    replacement_color = (0, 0, 0, 0)
    data = np.array(image)
    data[(data == transparent_color).all(axis=-1)] = replacement_color
    return Image.fromarray(data, mode='RGBA')