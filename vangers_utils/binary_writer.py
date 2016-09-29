import struct
from typing import Any, BinaryIO


class BinaryWriter:
    # Map well-known type names into struct format characters.
    TYPE_NAMES = {
        'int8': 'b',
        'uint8': 'B',
        'int16': 'h',
        'uint16': 'H',
        'int32': 'i',
        'int': 'i',
        'uint32': 'I',
        'int64': 'q',
        'uint64': 'Q',
        'float': 'f',
        'double': 'd',
        'char': 's'
    }

    def __init__(self, file: BinaryIO, verbose: bool=False):
        self._file = file
        self.pos = 0
        self._verbose = verbose

    def set_verbose(self, verbose: bool):
        self._verbose = verbose

    def write(self, type_name: str, value: Any):
        if type_name == 'str':
            packed = self._pack_str(value)
        elif type_name == 'str0':
            packed = self._pack_zero_ended_str(value)
        elif type_name == 'bytes':
            packed = value
        else:
            type_format = BinaryWriter.TYPE_NAMES[type_name.lower()]
            packed = self._pack_value(type_format, value)
        if self._verbose:
            if type_name == 'bytes':
                print("0x{:x} {}... (bytes({}))".format(
                    self.pos,
                    ':'.join(format(b, '02x') for b in packed[:10]),
                    len(packed)
                ))
            else:
                print("0x{:x} {} ({}:{})".format(
                    self.pos,
                    ':'.join(format(b, '02x') for b in packed),
                    value,
                    type_name
                ))

        self.pos += self._file.write(packed)

    def _pack_str(self, value: str)->bytes:
        value_bytes = value.encode('CP866')
        value_len = len(value_bytes)

        self.write('int32', value_len)
        value_bytes += b'\x00'
        packed = struct.pack('{}s'.format(len(value_bytes)), value_bytes)
        return packed

    def _pack_zero_ended_str(self, value: str)->bytes:
        value_bytes = value.encode('CP866') + b'\x00'
        packed = struct.pack('{}s'.format(len(value_bytes)), value_bytes)
        return packed

    def _pack_value(self, type_format: str, value: Any)->bytes:
        packed = struct.pack(type_format, value)
        return packed

    def rest(self)->bytes:
        return self._file.read()

