import math
from typing import Dict

from bitarray import bitarray


def convert_tree(decomp_tree) -> Dict[int, bitarray]:
    def _traverse_tree(index: int, parent_prefix: str):
        value = decomp_tree[index]
        if value <= 0:
            decode_dictionary[parent_prefix] = - value
        else:
            left_index = (value << 1) + 0
            right_index = (value << 1) + 1
            _traverse_tree(left_index, parent_prefix + '0')
            _traverse_tree(right_index, parent_prefix + '1')

    decode_dictionary = {}
    _traverse_tree(1, '')
    return {
        value: bitarray(prefix)
        for prefix, value in decode_dictionary.items()
    }


def decode_buf(buffer: bytes, decode_dict1: Dict[int, bitarray], decode_dict3: Dict[int, bitarray]):
    charcount = (1 << 11)

    a = bitarray()
    a.frombytes(buffer)

    vals1 = a.decode(decode_dict1)

    outs1 = []
    last_char = 0
    for v in vals1:
        last_char = (last_char + v) % 256
        outs1.append(last_char)

    a1 = bitarray()
    a1.encode(decode_dict1, vals1[:charcount])

    a3_offset = (math.ceil(len(a1) / 8)) * 8

    a3 = a[a3_offset:]
    vals3 = a3.decode(decode_dict3)
    if len(vals3) == charcount + 1:
        # print('Wrong len: len(vals3): {len}, '
        #       'len(a1): {a1_len}, '
        #       'len(a1)/8: {len_a1_8}, '
        #       'a3_offset: {a3_offset}'.format(
        #     len=len(vals3),
        #     a1_len=len(a1),
        #     len_a1_8=len(a1)/8,
        #     a3_offset=a3_offset
        # ))
        vals3 = vals3[:-1]
    outs3 = []
    last_char = 0
    for v in vals3:
        last_char = (last_char ^ v) % 256
        outs3.append(last_char)
    return outs1[:charcount], outs3
