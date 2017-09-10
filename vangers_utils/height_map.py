from typing import Tuple

import numpy as np
from tqdm import tqdm

from vangers_utils.binary_reader import BinaryReader
from vangers_utils.decompress import convert_tree, decode_buf


def read_map(filename: str, y_size: int) -> Tuple[np.array, np.array]:
    with open(filename, 'rb') as f:
        reader = BinaryReader(f)
        offset_table = []
        size_table = []
        for _ in range(y_size):
            offset_table.append(reader.read('int32'))
            size_table.append(reader.read('int16'))

        decomp_dict1 = convert_tree(reader.read_array('int32', 512))
        decomp_dict3 = convert_tree(reader.read_array('int32', 512))

        x_size = 1 << 11

        arr1 = np.zeros((y_size, x_size), np.uint8)
        arr3 = np.zeros((y_size, x_size), np.uint8)
        for i, (offset, size) in tqdm(enumerate(zip(offset_table, size_table)), total=y_size):
            reader.seek(offset)
            buf = reader.read_bytes(size)
            vals1, vals3 = decode_buf(buf, decomp_dict1, decomp_dict3)
            arr1[i, :] = vals1
            arr3[i, :] = vals3

    return arr1, arr3
