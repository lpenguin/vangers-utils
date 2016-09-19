from typing import Tuple, List

from vangers_utils.binary_reader import BinaryReader
from vangers_utils.script.options import Section, Mode


class Writer:
    INDENT_SYMBOL = '  '
    ARR_INDENT_SYMBOL = '- '

    def __init__(self, in_f: str, out_f: str):
        self._reader = BinaryReader(in_f)
        self._section = None  # type: Section
        self._mode = Mode.AS_NONE  # type: Mode

        self._indent = ''
        self._out = open(out_f, 'w')

    def new_section(self)->Section:
        self._section = Section(self._reader.read('int32'))
        return self._section

    def _write_indent(self):
        self._out.write(self._indent)

    def composite(self, *param_specs: List[Tuple[str, str]]):
        self._write_indent()
        self._out.write(self._section)
        for spec_name, spec_type in param_specs:
            self._write_indent()
            value = self._reader.read(spec_type)
            self._out.write(self.INDENT_SYMBOL+spec_name+": "+value)
        self._out.write("\n")

    def composite_array(self, *param_specs: List[Tuple[str, str]]):
        self._write_indent()
        self._out.write(self._section)

        size = self._reader.read('int32')
        for i in range(size):
            for spec_name, spec_type in param_specs:
                value = self._reader.read(spec_type)
                self._out.write(self.ARR_INDENT_SYMBOL if i == 0 else self.INDENT_SYMBOL)
                self._write_indent()
                self._out.write(spec_name + ": " + value)

    def has_mode(self, mode: Mode)->bool:
        return self._mode == mode

    def set_mode(self, mode: Mode):
        self._mode = mode
        self._write_indent()
        self._out.write(str(mode)+" { ")
        self._indent += self.INDENT_SYMBOL

    def _value(self, value, comment, name=None):
        pname = name if name else str(self._section)

        self._write_indent()
        self._out.write(pname+": "+value)
        if comment:
            self._out.write(" # "+comment)
        self._out.write('\n')

    def str(self, comment: str=None, name: str=None):
        data = self._reader.read('str')
        self._value(data, comment, name)

    def int(self, comment: str=None, name: str=None)->int:
        data = self._reader.read('int32')
        self._value(data, comment, name)
        return int(data)

    def assert_mode(self, *modes):
        if self._mode not in modes:
            raise ValueError("Misplaced option"+str(self._section))

    def comment(self, comment: str):
        self._write_indent()
        self._out.write("# "+comment+"\n")

    def flag(self, flag_name):
        self.comment("FLAG: "+flag_name)

    def end_block(self):
        raise NotImplementedError()


