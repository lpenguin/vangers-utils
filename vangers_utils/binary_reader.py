import struct
import yaml


class BinaryReaderEOFException(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'Not enough bytes in file to satisfy read request'


class BinaryReader:
    # Map well-known type names into struct format characters.
    typeNames = {
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

    def __init__(self, fileName):
        if isinstance(fileName, str):
            self.file = open(fileName, 'rb')
        else:
            self.file = fileName

    def read(self, typeName):
        if typeName == 'str':
            return self._read_str()

        if typeName == 'str0':
            return self._read_zero_ended_str()

        typeFormat = BinaryReader.typeNames[typeName.lower()]
        typeSize = struct.calcsize(typeFormat)
        value = self.file.read(typeSize)
        if typeSize != len(value):
            raise BinaryReaderEOFException
        return struct.unpack(typeFormat, value)[0]

    def _read_str(self):
        size = self.read('int32')
        data = self.file.read(size+1)
        unpacked = struct.unpack('{}s'.format(size), data[:-1])[0]

        try:
            return unpacked.decode('CP866')
        except UnicodeDecodeError:
            return repr(yaml.dump(unpacked))

    def rest(self)->bytes:
        return self.file.read()

    def __del__(self):
        self.file.close()

    def _read_zero_ended_str(self):
        data = ''
        while True:
            c = self.read('char')
            if c == b'\x00':
                break
            data += c.decode()
        return data

