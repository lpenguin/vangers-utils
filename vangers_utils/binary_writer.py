import struct
from typing import Any
import yaml
from typing import IO


class BinaryWriter:
    # Map well-known type names into struct format characters.
    TYPE_NAMES = {
        'int8': 'b',
        'uint8': 'B',
        'int16': 'h',
        'uint16': 'H',
        'int32': 'i',
        'uint32': 'I',
        'int64': 'q',
        'uint64': 'Q',
        'float': 'f',
        'double': 'd',
        'char': 's'}

    def __init__(self, filename: str):
        self.file = open(filename, 'wb')  # type: IO[bytes]

    def write(self, type_name: str, value: Any):
        if type_name == 'str':
            self._write_str(value)
            return

        if type_name == 'str0':
            self._write_zero_ended_str(value)
            return

        type_format = BinaryWriter.TYPE_NAMES[type_name.lower()]
        type_size = struct.calcsize(type_format)
        self.file.write(struct.pack(type_format, value))
        value = self.file.read(type_size)
        if type_size != len(value):
            raise ValueError("Binary write: invalid size")

    def _write_str(self, value: str):
        value_bytes = value.encode('CP866')
        value_len = len(value_bytes)

        self.write('int32', value_len)
        value_bytes += b'\x00'
        packed = struct.pack('{}s'.format(value_len), value_bytes + b'\x00')
        self.file.write(packed)

    def rest(self)->bytes:
        return self.file.read()

    def __del__(self):
        self.file.close()

    def _write_zero_ended_str(self, value: str):
        value_bytes = value.encode('CP866')
        packed = struct.pack('{}s'.format(len(value_bytes)), value_bytes + b'\x00')
        self.file.write(packed)

