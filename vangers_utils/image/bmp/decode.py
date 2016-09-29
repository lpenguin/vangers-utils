from io import BytesIO
from typing import List, Dict

from PIL import Image

from vangers_utils import binary_reader
from vangers_utils.image import misc


class BmpImage:
    def __init__(self, images: List, meta: Dict[str, int]):
        self.images = images
        self.meta = meta


def decode_image(file_name: str, palette: List[int],
                 is_bmp: bool=True, is_background: bool=False, is_no_offsets: bool=False)-> BmpImage:
    with open(file_name, 'rb') as f:
        bytes_io = BytesIO(f.read())

    reader = binary_reader.BinaryReader(bytes_io)

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

    images = []  # type: List[Image]
    for _ in range(meta['size']):
        b = bytes_io.read(meta['sizex'] * meta['sizey'])
        im = misc.from_bytes(b, meta['sizex'], meta['sizey'], palette=palette)
        # transparent_color = (240, 160, 0, 255)
        r, g, b = palette[-3:]
        transparent_color = (r, g, b, 255)
        image = misc.replace_transparent(im, transparent_color)
        images.append(image)

    return BmpImage(
        images=images,
        meta=meta,
    )


