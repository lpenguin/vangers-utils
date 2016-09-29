from typing import Optional

import yaml

from vangers_utils.binary_writer import BinaryWriter
from vangers_utils.scb.options import Section


class YamlToScbConverter:
    KNOWN_TYPES = {
        'int': int,
        'str': str,
    }

    def __init__(self, in_file, out_file):
        self._in_file = in_file
        self._out_file = out_file

    def _write_section(self, section_name: str, writer: BinaryWriter):
        section_name = section_name.replace('Section.', '')
        section = Section[section_name]
        writer.write('int32', section.value)

    def _write_value(self, value: str, tag: str, writer: BinaryWriter):
        _, _1, type_name = tag.split(":")
        value_type = self.KNOWN_TYPES[type_name]
        value = value.replace('\\r', '\r').replace('\\n', '\n')
        value = value_type(value)

        writer.write(type_name, value)

    def convert(self, verbose: bool=False):
        with open(self._in_file, 'rt') as in_f:
            with open(self._out_file, 'wb') as out_f:
                writer = BinaryWriter(out_f, verbose=verbose)
                writer.write('str0', 'BIN_SCR_1_00')
                writer.write('int', 0)

                for event in yaml.parse(in_f):
                    if isinstance(event, yaml.ScalarEvent):
                        tag = event.tag  # type: Optional[str]
                        value = event.value  # type: str
                        if not tag and not value:
                            continue

                        if value.startswith('$'):
                            continue
                        if value.startswith('Section.'):
                            if verbose:
                                print(value)
                            self._write_section(value, writer)
                        else:
                            self._write_value(value, event.tag, writer)

