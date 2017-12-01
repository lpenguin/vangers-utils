from io import BytesIO
from typing import List, Dict

from PIL import Image

from vangers_utils import binary_reader
from vangers_utils.image import misc


class BmpImage:
    def __init__(self, images: List, meta: Dict[str, int]):
        self.images = images
        self.meta = meta


def decode_image(file_name: str, palette: List[int]) -> BmpImage:
    with open(file_name, 'rb') as f:
        data = f.read()
        bytes_io = BytesIO(data)

    reader = binary_reader.BinaryReader(bytes_io)

    meta = {
        'sizex': None,
        'sizey': None,
        'size': None,
        'offsetx': None,
        'offsety': None,
    }  # type: Dict[str, int]

    sizex = reader.read('uint16')
    sizey = reader.read('uint16')
    meta['sizex'] = sizex
    meta['sizey'] = sizey

    approx_size = len(data) // (sizex * sizey)
    header_size = len(data) % (sizex * sizey)
    if header_size == 10:
        meta['size'] = reader.read('uint16')
        meta['offsetx'] = reader.read('uint16')
        meta['offsety'] = reader.read('uint16')
    elif header_size == 6:
        meta['size'] = reader.read('uint16')
    elif header_size == 4:
        pass
    else:
        raise Exception("Wrong header size: {}".format(header_size))

    print('SizeX: {sizex}, SizeY: {sizey}, Offsex: {offsetx}, OffsetY: {offsety}, length: {length}, '
          'approx size: {approx_size}, '
          'header_size: {header_size}'.format(
        sizex=sizex,
        sizey=sizey,
        approx_size=approx_size,
        header_size=header_size,
        length=len(data),
        offsetx=meta['offsetx'],
        offsety=meta['offsety'],
    ))

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
