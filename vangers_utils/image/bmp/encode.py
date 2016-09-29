from io import BytesIO
from typing import Dict, List

import numpy as np
from PIL import Image

from vangers_utils import binary_writer
from vangers_utils.image import palette


def encode_image(file_name: str, meta: Dict[str, int], pal: List[int])-> bytes:
    is_bmp, is_background, is_no_offsets = (
        meta['is_bmp'], meta['is_background'], meta['is_no_offsets']
    )

    bytes_io = BytesIO()
    writer = binary_writer.BinaryWriter(bytes_io)

    if not is_bmp and not is_background:
        if not is_no_offsets:
            writer.write('uint16', meta['sizex'])
            writer.write('uint16', meta['sizey'])
            writer.write('uint16', meta['size'])
            writer.write('uint16', meta['offsetx'])
            writer.write('uint16', meta['offsety'])
        else:
            writer.write('uint16', meta['sizex'])
            writer.write('uint16', meta['sizey'])
            writer.write('uint16', meta['size'])
    else:
        if is_bmp:
            writer.write('uint16', meta['sizex'])
            writer.write('uint16', meta['sizey'])

    image = Image.open(file_name)  # type: Image
    b = _data_to_256(np.array(image), pal).tobytes()
    bytes_io.write(b)

    return bytes_io.getvalue()


def _data_to_256(data: np.ndarray, pal: List[int])->np.ndarray:
    pal_mapping = palette.create_palette_mapping(pal)

    def _to_256(x):
        color_index = palette.color_index(x[:3])
        return pal_mapping[color_index]

    return np.apply_along_axis(_to_256, 2, data)