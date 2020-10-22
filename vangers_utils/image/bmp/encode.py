from io import BytesIO
from typing import Dict, List

import numpy as np
from PIL import Image

from vangers_utils import binary_writer
from vangers_utils.image import palette


def encode_image(image: Image, meta: Dict[str, int], pal: List[int])-> bytes:
    bytes_io = BytesIO()
    writer = binary_writer.BinaryWriter(bytes_io)

    if meta is None:
        meta = {
            'sizex': image.size[0],
            'sizey': image.size[1],
            'size': None,
            'offsetx': None,
            'offsety': None,
        }

    if meta['sizex'] is not None:
        writer.write('uint16', meta['sizex'])
        writer.write('uint16', meta['sizey'])

    if meta['size'] is not None:
        writer.write('uint16', meta['size'])

    if meta['offsetx'] is not None:
        writer.write('uint16', meta['offsetx'])
        writer.write('uint16', meta['offsety'])

    if image.mode == 'P':
        b = bytes(image.getdata())
    else:
        b = _data_to_256(np.array(image), pal).tobytes()

    bytes_io.write(b)

    return bytes_io.getvalue()


def _data_to_256(data: np.ndarray, pal: List[int])->np.ndarray:
    pal_mapping = palette.create_palette_mapping(pal)

    def _to_256(x):
        color_index = palette.color_index(x[:3])
        return pal_mapping[color_index]

    return np.apply_along_axis(_to_256, 2, data)