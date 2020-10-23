from io import BytesIO
from typing import List, Dict, Optional, Tuple

from PIL import Image

from vangers_utils import binary_reader
from vangers_utils.image import misc


class BmpImage:
    def __init__(self, images: List, meta: Dict[str, int]):
        self.images = images
        self.meta = meta


def _infer_format(data: bytes, file_size: int) -> Optional[List[Tuple[str, str]]]:
    if _is_format1(data, file_size):
        return [
            ('sizex', 'uint16'),
            ('sizey', 'uint16'),
            ('size', 'uint16'),
            ('offsetx', 'uint16'),
            ('offsetx', 'uint16')
        ]
    elif _is_format2(data, file_size):
        return [
            ('sizex', 'uint16'),
            ('sizey', 'uint16'),
            ('size', 'uint16'),
        ]
    elif _is_format3(data, file_size):
        return [
            ('sizex', 'uint16'),
            ('sizey', 'uint16'),
        ]
    elif _is_format4(data, file_size):
        return [
            ('size', 'uint32'),
            ('ctable', 'uint32'),
            ('sizex', 'uint32'),
            ('sizey', 'uint32'),
        ]

    return None

def _is_format1(data: bytes, file_size: int)->bool:
    reader = binary_reader.BinaryReader(BytesIO(data))
    sizex = reader.read('uint16')
    sizey = reader.read('uint16')
    size = reader.read('uint16')
    offsetx = reader.read('uint16')
    offsety = reader.read('uint16')

    return file_size == (10 + size * sizex * sizey)


def _is_format2(data: bytes, file_size: int)->bool:
    reader = binary_reader.BinaryReader(BytesIO(data))
    sizex = reader.read('uint16')
    sizey = reader.read('uint16')
    size = reader.read('uint16')

    return file_size == (6 + size * sizex * sizey)


def _is_format3(data: bytes, file_size: int)->bool:
    reader = binary_reader.BinaryReader(BytesIO(data))
    sizex = reader.read('uint16')
    sizey = reader.read('uint16')

    return file_size == (4 + sizex * sizey)


def _is_format4(data: bytes, file_size: int)->bool:
    reader = binary_reader.BinaryReader(BytesIO(data))
    num_frames = reader.read('uint32')
    ctable = reader.read('uint32')
    sizex = reader.read('uint32')
    sizey = reader.read('uint32')

    print(file_size, num_frames, sizex, sizey)
    return file_size == (16 + num_frames * sizex * sizey)


def decode_image(file_name: str, palette: List[int]) -> BmpImage:
    with open(file_name, 'rb') as f:
        data = f.read()
        file_size = len(data)
    # print(palette)

    # palette = palette[:384] + objects_palette[384:]
    # print(len(palette))
    format = _infer_format(data, file_size)
    bytes_io = BytesIO(data)
    reader = binary_reader.BinaryReader(bytes_io)

    print(f'Inferred format: {format}')
    meta = {
        'sizex': None,
        'sizey': None,
        'size': None,
        'offsetx': None,
        'offsety': None,
        'ctable': None
    }  # type: Dict[str, int]

    for (field, field_type) in format:
        meta[field] = reader.read(field_type)

    print('SizeX: {sizex}, SizeY: {sizey}, Offsex: {offsetx}, OffsetY: {offsety}, length: {length}'.format(
        sizex=meta['sizex'],
        sizey=meta['sizey'],
        length=len(data),
        offsetx=meta['offsetx'],
        offsety=meta['offsety'],
    ))

    images = []  # type: List[Image]
    b = bytes_io.read(meta['sizex'] * meta['sizey'] * (meta['size'] or 1))
    # for _ in range(meta['size'] or 1):


    im = misc.from_bytes(b, meta['sizex'], meta['sizey'] * (meta['size'] or 1), palette=palette)
        # transparent_color = (240, 160, 0, 255)
        # r, g, b = palette[-3:]
        # transparent_color = (r, g, b, 255)
        # image = misc.replace_transparent(im, transparent_color)
    images.append(im)
        # break

    return BmpImage(
        images=images,
        meta=meta,
    )
