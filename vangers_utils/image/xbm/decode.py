from typing import List

import numpy as np
from PIL import Image

import vangers_utils.image.palette
from vangers_utils import binary_reader
from vangers_utils.image import misc
from vangers_utils.image.xbm.image import XbmImage


def _read_meta_and_data(file_name: str) -> (XbmImage.Meta, bytes):
    r = binary_reader.BinaryReader(file_name)
    meta = XbmImage.Meta(
        posx=r.read('int32'),
        posy=r.read('int32'),
        b_size_x=r.read('int32'),
        b_size_y=r.read('int32'),
        size_x=r.read('int32'),
        size_y=r.read('int32'),
        image_size=r.read('int32'),
    )

    byte_data = r.file.read()
    r.file.close()
    return meta, byte_data


def _decode_image(image_data: bytes, screen_width: int, screen_height: int, palette: List[int]) -> Image:
    reader = ImageDataDecoder(
        bytes_data=image_data,
        width=screen_width,
        height=screen_height)

    screen = reader.decode()
    im = misc.from_bytes(screen.tobytes(), screen_width, screen_height, palette=palette)
    return im#image_misc.replace_transparent(im)


def decode_image(file_name: str, screen_width: int, screen_height: int, palette: List[int])-> XbmImage:
    meta, data = _read_meta_and_data(file_name)
    return XbmImage(
        meta=meta,
        image=_decode_image(image_data=data,
                            screen_width=screen_width,
                            screen_height=screen_height,
                            palette=palette,
                            )
    )


def encode_image(file_name: str, screen_width: int, screen_height: int)-> XbmImage:
    meta, data = _read_meta_and_data(file_name)
    return XbmImage(
        meta=meta,
        image=_decode_image(image_data=data,
                            screen_width=screen_width,
                            screen_height=screen_height)
    )


class ImageDataDecoder(object):
    def __init__(self, bytes_data: bytes, width: int, height: int):
        self.data = np.fromiter(bytes_data, dtype='b')
        self.screen = np.zeros(width * height, dtype=np.uint8) + 255
        self.width = width
        self.height = height
        self.pos = 0

    def read_int(self)->int:
        res = self.data[self.pos:self.pos + 4].view(np.uint32)
        self.pos += 4
        return res[0]

    def read_many(self, count: int)->bytes:
        res = self.data[self.pos:self.pos + count]
        self.pos += count
        return res

    def copy_into_screen(self, x, y, count, data):
        index = y * self.width + x
        self.screen[index:index + count] = data

    def has_next(self)->bool:
        return self.pos < len(self.data)

    def decode(self)->np.array:
        cnt = self.read_int()

        while cnt != 0 and self.has_next():
            x = self.read_int()
            y = self.read_int()
            _data = self.read_many(cnt)
            self.copy_into_screen(x, y, cnt, _data)
            cnt = self.read_int()
        return self.screen