from typing import List, Dict

from PIL import Image

from vangers_utils import binary_reader
from vangers_utils.image import image_misc


class BmpImage:
    def __init__(self, image: Image, meta: Dict[str, int]):
        self.image = image
        self.meta = meta


def read_image(file_name: str, palette: List[int],
               is_bmp: bool=True, is_background: bool=False, is_no_offsets: bool=False)->BmpImage:

    reader = binary_reader.BinaryReader(file_name)

    meta = {
        'sizex': None,
        'sizey': None,
        'size': None,
        'offsetx': None,
        'offsety': None,
        'is_bmp': int(is_bmp),
        'is_background': int(is_background),
        'is_no_offsets': int(is_no_offsets),
    }  # type: Dict[str, int]

    if not is_bmp and not is_background:
        if not is_no_offsets:
            meta['sizex'] = reader.read('uint16')
            meta['sizey'] = reader.read('uint16')
            meta['size'] = reader.read('uint16')
            meta['offsetx'] = reader.read('uint16')
            meta['offsety'] = reader.read('uint16')
        else:
            meta['sizex'] = reader.read('uint16')
            meta['sizey'] = reader.read('uint16')
            meta['size'] = reader.read('uint16')
    else:
        if is_bmp:
            meta['sizex'] = reader.read('uint16')
            meta['sizey'] = reader.read('uint16')
            meta['size'] = 1
        else:
            meta['size'] = 1

    b = reader.rest()

    im = image_misc.from_bytes(b, meta['sizex'], meta['sizey'], palette=palette)
    # transparent_color = (240, 160, 0, 255)
    r, g, b = palette[-3:]
    transparent_color = (r, g, b, 255)
    image = image_misc.replace_transparent(im, transparent_color)
    return BmpImage(
        image=image,
        meta=meta,
    )

