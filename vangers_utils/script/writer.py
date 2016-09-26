from typing import Tuple, List

import sys

from vangers_utils.binary_reader import BinaryReader
from vangers_utils.script.options import Section, Mode


class Writer:
    class Out:
        def __init__(self, file):
            self._f = open(file, 'wt')

        def write(self, data):
            #sys.stdout.write(data)
            self._f.write(data)

        def close(self):
            self._f.close()

    INDENT_SYMBOL = '  '
    ARR_INDENT_SYMBOL = '- '
    iSCRIPT_EOF = 8383


    def __init__(self, in_f: str, out_f: str):
        self._reader = BinaryReader(in_f)
        self._section = None  # type: Section
        self._mode = Mode.AS_NONE  # type: Mode

        self._indent = ''
        self._n_file = 0
        self._out_f = out_f
        # self._out = Writer.Out(self._out_f.replace('yml', '{}.yml'.format(self._n_file)))
        self._out = Writer.Out(self._out_f)
        self._n_section = 0
        self._level = 0

    def end_section(self):
        pass

    def new_section(self)->Section:
        sid = self._reader.read('int32')
        if sid == self.iSCRIPT_EOF:
            return None
        self._section = Section(sid)
        if self._section == Section.I_END_BLOCK:
            indent = self._indent[:-len(self.INDENT_SYMBOL)]
        else:
            indent = self._indent
        self._n_section += 1
        
        self._out.write("{}{}:\n".format(indent, self._section))
        return self._section

    def _write_indent(self):
        self._out.write(self._indent)

    def composite(self, *param_specs: List[Tuple[str, str]]):
        for spec_name, spec_type in param_specs:
            self._write_indent()
            value = self._reader.read(spec_type)
            self._out.write("{}${}: !!{} {}\n".format(self.INDENT_SYMBOL, spec_name, type(value).__name__, value))
        

    def composite_array(self, *param_specs: List[Tuple[str, str]], length: int=None):
        if not length:
            size = self._reader.read('int32')
        else:
            size = length
        if length is None:
            self._write_indent()
            self._out.write("{indent}{arr_indent}$size: {value}\n".format(
                    indent=self.INDENT_SYMBOL,
                    arr_indent=self.ARR_INDENT_SYMBOL,
                    value=size,
                    ))
        for i in range(size):
            for n, (spec_name, spec_type) in enumerate(param_specs):
                value = self._reader.read(spec_type)
                self._write_indent()

                arr_indent = self.ARR_INDENT_SYMBOL if n == 0 else self.INDENT_SYMBOL
                self._out.write("{indent}{arr_indent}${name}: !!{type} {value}\n".format(
                    indent=self.INDENT_SYMBOL,
                    type=type(value).__name__,
                    arr_indent=arr_indent,
                    name=spec_name, 
                    value=value,
                    ))

    def has_mode(self, *mode: List[Mode])->bool:
        return self._mode in mode

    def set_mode(self, mode: Mode):
        self._mode = mode
        self._indent += self.INDENT_SYMBOL
        self._level += 1
        self._write_indent()
        self._out.write("# mode = {}\n".format(self._mode))

    def _value(self, value, comment, name=None):
        pname = '$'+name if name else '$v'

        self._write_indent()
        self._out.write("{indent}{name}: !!{type} {value}".format(
            indent=self.INDENT_SYMBOL,
            type=type(value).__name__,
            name=pname,
            value=value))
        if comment:
            self._out.write(" # "+comment)
        self._out.write('\n')

    def str(self, name: str=None, comment: str=None):
        data = self._reader.read('str')
        self._value(data, comment, name)

    def int(self, name: str=None, comment: str=None)->int:
        data = self._reader.read('int32')
        self._value(data, comment, name)
        return int(data)

    def assert_mode(self, *modes):
        if self._mode not in modes:
            raise ValueError("Misplaced section: {}. Mode must be: {}, actual mode: {}".format(
                self._section,
                ', '.join(map(str, modes)),
                self._mode,
            ))

    # def assert_mode_not(self, *modes):
    #     if self._mode in modes:
    #         raise ValueError("Misplaced section: {}. Mode must NOT be: {}, actual mode: {}".format(
    #             self._section,
    #             ', '.join(modes),
    #             self._mode,
    #         ))

    def comment(self, comment: str):
        self._write_indent()
        self._out.write("# "+comment+"\n")

    def flag(self, flag_name):
        self.comment("FLAG: "+flag_name)

    def flush(self):
        pass

    def end_block(self, new_mode):
        self._indent = self._indent[:-len(self.INDENT_SYMBOL)]
        self._mode = new_mode
        self._write_indent()
        self._out.write("# mode = {} (end block)\n".format(self._mode))
        self._level -= 1

        #if self._level == 0 and self._n_section > 1000:
        #    self._out.close()
        #    self._n_section = 0
        #    self._n_file += 1
        #    self._out = Writer.Out(self._out_f.replace('yml', '{}.yml'.format(self._n_file)))

    #def buf(self, name:str=None, comment: str=None):
    #    return self.str(name, comment)


