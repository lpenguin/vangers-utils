from io import BytesIO
from itertools import chain

import numpy as np
from PIL import Image

from vangers_utils.binary_writer import BinaryWriter
from vangers_utils.image.palette import color_index, create_palette_mapping, PALETTE
from vangers_utils.image.xbm.image import XbmImage


class XbmEncoder:
    def __init__(self):
        self._pal_mapping = create_palette_mapping(PALETTE)
        self._transparent_color = 255 #self._pal_mapping[_color_index((32, 76, 32))]

    def _rgb_to_256(self, data: np.ndarray)->np.ndarray:
        def _to_256(x):
            return self._pal_mapping[color_index(x[:3])]

        encoded = np.apply_along_axis(_to_256, 2, data)

        return encoded

    def _encode_data(self, data: np.ndarray)->bytes:
        bytes_io = BytesIO()
        out = BinaryWriter(bytes_io)
        out.pos = 0x1c
        for y, row in enumerate(data):
            is_prev_transparent = True
            first_opaque_x = None
            for x, color in enumerate(chain(row, [self._transparent_color])):
                is_transparent = color == self._transparent_color
                from_transparent_to_opaque = is_prev_transparent and not is_transparent
                from_opaque_to_transparent = not is_prev_transparent and is_transparent

                if from_transparent_to_opaque:
                    first_opaque_x = x
                elif from_opaque_to_transparent:
                    bs = row[first_opaque_x:x].tobytes()  # type: bytes
                    cnt = x - first_opaque_x
                    if len(bs) != cnt:
                        raise ValueError("Invalid bytes len: {}, expected: {}".format(
                            len(bs), cnt
                        ))
                    out.write('int32', cnt)
                    out.write('int32', first_opaque_x)
                    out.write('int32', y)
                    out.write('bytes', bs)

                is_prev_transparent = is_transparent
        out.write('int32', 0)
        return bytes_io.getvalue()

    def encode_data_to_file(self, data_rgb: np.ndarray, meta: XbmImage.Meta, out_file: str):
        data_256 = self._rgb_to_256(data_rgb)

        with open(out_file, 'wb') as f:
            encoded_data = self._encode_data(data_256)

            w = BinaryWriter(f)
            w.write('int32', meta.posx)
            w.write('int32', meta.posy)
            w.write('int32', meta.b_size_x)
            w.write('int32', meta.b_size_y)
            w.write('int32', meta.size_x)
            w.write('int32', meta.size_y)
            w.write('int32', len(encoded_data))
            w.write('bytes', encoded_data)


def encode_image(meta: XbmImage.Meta, in_filename: str, out_file_name: str):
    img = Image.open(in_filename)
    data_rgb = np.array(img)
    XbmEncoder().encode_data_to_file(data_rgb, meta, out_file_name)

    # data_256 = _rgb_to_256(pal_mapping, data_rgb)
    # _encode_data_to_file(data_256, img_meta, out_file_name)
