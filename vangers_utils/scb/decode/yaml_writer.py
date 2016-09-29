import sys
from typing import Tuple, List, Any

import yaml

from vangers_utils.scb.options import Section, Mode


class YamlWriter:
    iSCRIPT_EOF = 8383

    def __init__(self, out_file_io):
        self._mode = Mode.AS_NONE  # type: Mode

        self._out_f = out_file_io
        self._level = 0

        self._add_mapping_end_on_end_block = True

        self._events = []  # type: List[yaml.Event]
        self._events.append(yaml.StreamStartEvent(encoding='utf-8'))
        self._events.append(yaml.DocumentStartEvent(explicit=True))
        self._add_mapping_start()

    def next_section(self, section: Section):
        self._add_mapping_end_on_end_block = True

        if section in (Section.I_END_BLOCK, Section.I_SCRIPT_EOF):
            self._add_scalar(str(section), implicit=True)
            self._add_scalar('', implicit=True)
            self._add_mapping_end_on_end_block = False
            return section

        self._add_scalar(str(section), implicit=True)
        self._add_mapping_start()

    def _add_scalar(self, value: Any, implicit: bool = False):
        if implicit or isinstance(value, str) and value.startswith('$'):
            tag = None
            implicit = (True, False)
        else:
            tag = u'tag:yaml.org,2002:{}'.format(type(value).__name__)
            implicit = (False, False)
        value = str(value)

        self._events.append(
            yaml.ScalarEvent(anchor=None,
                             tag=tag,
                             implicit=implicit,
                             value=str(value)),
        )

    def _add_mapping_start(self):
        self._level += 1
        self._events.append(
            yaml.MappingStartEvent(anchor=None, tag=None, implicit=True, flow_style=False)
        )

    def _add_mapping_end(self):
        if self._level == 0:
            sys.stderr.write("Attempt to decrease mapping level\n")
            return
        self._level -= 1
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

    def composite(self, param_specs: List[Tuple[str, str]]):
        for spec_name, value in param_specs:
            self._add_scalar('$' + spec_name)
            self._add_scalar(value)

    def composite_array(self, param_specs_array: List[List[Tuple[str, Any]]], size: int, write_size: bool):
        self._add_scalar('$values[]')
        self._add_sequence_start()

        if write_size:
            self._add_mapping_start()
            self._add_scalar('$size')
            self._add_scalar(size)
            self._add_mapping_end()

        for param_specs in param_specs_array:
            self._add_mapping_start()
            for n, (spec_name, value) in enumerate(param_specs):
                self._add_scalar('$' + spec_name)
                self._add_scalar(value)
            self._add_mapping_end()
        self._add_sequence_end()

    def set_mode(self, mode: Mode):
        self._mode = mode
        self._add_mapping_end_on_end_block = False

    def value(self, value, comment, name=None):
        pname = '$' + name if name else '$v'

        self._add_scalar(pname)
        self._add_scalar(value)

    def flush(self):
        self._add_mapping_end()
        self._events.append(
            yaml.DocumentEndEvent(explicit=True),
        )
        self._events.append(
            yaml.StreamEndEvent(),
        )

        yaml.emit(self._events, stream=self._out_f, allow_unicode=True)

    def end_section(self):
        if self._add_mapping_end_on_end_block:
            self._add_mapping_end()
