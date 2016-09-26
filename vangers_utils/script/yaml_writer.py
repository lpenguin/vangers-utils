from typing import Tuple, List, Any
import yaml

from vangers_utils.binary_reader import BinaryReader
from vangers_utils.script.options import Section, Mode


class YamlWriter:
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
        self._out = YamlWriter.Out(self._out_f)
        self._n_section = 0
        self._level = 0

        self._events = []  # type: List[yaml.Event]
        self._events.append(yaml.StreamStartEvent(encoding='utf-8'))
        self._events.append(yaml.DocumentStartEvent(explicit=True))
        self._add_mapping_start()

    def new_section(self)->Section:
        sid = self._reader.read('int32')
        if sid == self.iSCRIPT_EOF:
            self._add_mapping_end()
            return None
        self._section = Section(sid)
        if self._section == Section.I_END_BLOCK:
            self._add_mapping_end()
            return self._section

        self._n_section += 1

        self._add_scalar(str(self._section), implicit=True)
        self._add_mapping_start()
        return self._section

    # def _write_indent(self):
    #     self._out.write(self._indent)

    def _add_scalar(self, value: Any, implicit: bool=False):
        tag = 'tag:yaml.org,2002:{}'.format(type(value).__name__)
        value = str(value)
        if value.startswith('$') or value.startswith('Section.'):
            tag = None
            implicit = (True, False)
        else:
            # tag = 'tag:yaml.org,2002:{}'.format(type(value).__name__)
            implicit = (False, False)
        self._events.append(
            yaml.ScalarEvent(anchor=None,
                             tag=tag,
                             # tag=tag,
                             implicit=implicit,
                             # implicit=(True, True) if implicit else (False, False),
                             value=str(value)),
        )

    def _add_mapping_start(self):
        self._events.append(
            # yaml.MappingStartEvent(anchor=None, tag=u'tag:yaml.org,2002:map', implicit=True, flow_style=False)
            yaml.MappingStartEvent(anchor=None, tag=None, implicit=True, flow_style=False)
        )

    def _add_mapping_end(self):
        self._events.append(
            yaml.MappingEndEvent()
        )

    def _add_sequence_start(self):
        self._events.append(
            yaml.SequenceStartEvent(anchor=None, tag=u'tag:yaml.org,2002:seq', implicit=True, flow_style=True),
        )

    def _add_sequence_end(self):
        self._events.append(
            yaml.SequenceEndEvent(),
        )

    def composite(self, *param_specs: List[Tuple[str, str]]):
        # self._add_mapping_start()
        for spec_name, spec_type in param_specs:
            value = self._reader.read(spec_type)
            self._add_scalar(spec_name)
            self._add_scalar(value)
        # self._add_mapping_end()

    def composite_array(self, *param_specs: List[Tuple[str, str]], length: int=None):
        if not length:
            size = self._reader.read('int32')
        else:
            size = length
        self._add_scalar('$values[]')
        self._add_sequence_start()

        if length is None:
            self._add_mapping_start()
            self._add_scalar('$size')
            self._add_scalar(size)
            self._add_mapping_end()

        for i in range(size):
            self._add_mapping_start()
            for n, (spec_name, spec_type) in enumerate(param_specs):
                value = self._reader.read(spec_type)
                self._add_scalar(spec_name)
                self._add_scalar(value)
            self._add_mapping_end()
        self._add_sequence_end()

    def has_mode(self, *mode: List[Mode])->bool:
        return self._mode in mode

    def set_mode(self, mode: Mode):
        self._mode = mode
        self._indent += self.INDENT_SYMBOL
        self._level += 1
        # self._write_indent()
        # self._out.write("# mode = {}\n".format(self._mode))

    def _value(self, value, comment, name=None):
        pname = '$'+name if name else '$v'

        # self._add_mapping_start()
        self._add_scalar(pname)
        self._add_scalar(value)
        # self._add_mapping_end()

        # self._write_indent()
        # self._out.write("{indent}{name}: !!{type} {value}".format(
        #     indent=self.INDENT_SYMBOL,
        #     type=type(value).__name__,
        #     name=pname,
        #     value=value))
        # if comment:
        #     self._out.write(" # "+comment)
        # self._out.write('\n')

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
        pass
        # self._write_indent()
        # self._out.write("# "+comment+"\n")

    def flag(self, flag_name: str):
        # self.comment("FLAG: "+flag_name)
        self._value('$FLAG', '$'+flag_name)

    def end_block(self, new_mode):
        # self._indent = self._indent[:-len(self.INDENT_SYMBOL)]
        self._mode = new_mode
        # self._write_indent()
        # self._out.write("# mode = {} (end block)\n".format(self._mode))
        # self._level -= 1

        #if self._level == 0 and self._n_section > 1000:
        #    self._out.close()
        #    self._n_section = 0
        #    self._n_file += 1
        #    self._out = Writer.Out(self._out_f.replace('yml', '{}.yml'.format(self._n_file)))

    def flush(self):
        # self._add_mapping_end()
        self._events.append(
            yaml.DocumentEndEvent(explicit=True),
        )
        self._events.append(
            yaml.StreamEndEvent(),
        )

        for e in self._events:
            print(e)
        # yaml.emit(self._events, stream=self._out._f)
        # yaml.emit(self._events)

    def end_section(self):
        self._add_mapping_end()


