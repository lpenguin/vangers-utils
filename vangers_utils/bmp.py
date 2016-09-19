from PIL import Image

from vangers_utils import binary_reader
from vangers_utils import config, image_misc, palette


def read_image(file_name: str, pal: str=None)->Image:
    reader = binary_reader.BinaryReader(file_name)
    width = reader.read('uint16')
    height = reader.read('uint16')

    b = reader.rest()

    if pal:
        pal = palette.make_palette(pal)
    im = image_misc.from_bytes(b, width, height, palette=pal)
    return image_misc.replace_transparent(im)
