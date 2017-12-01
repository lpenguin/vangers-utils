from typing import Any
from typing import List, Tuple

from vangers_utils.binary_reader import BinaryReader
from vangers_utils.scb.decode.yaml_writer import YamlWriter
from vangers_utils.scb.options import Section, Mode

FM_REDRAW = 0x01
FM_FLUSH = 0x02
FM_ACTIVE = 0x08
FM_ITEM_MENU = 0x10
FM_OFF = 0x20
FM_LOCATION_MENU = 0x40
FM_ISCREEN_MENU = 0x80
FM_NO_DEACTIVATE = 0x100
FM_SUBMENU = 0x200
FM_HIDDEN = 0x400
FM_LOCK = 0x800
FM_NO_ALIGN = 0x1000
FM_MAIN_MENU = 0x2000
FM_RANGE_FONT = 0x4000


class DecoderTrait:
    def __init__(self, in_file_io, out_file_io):
        self._reader = BinaryReader(in_file_io)
        self._writer = YamlWriter(out_file_io)
        self._section = None  # type: Section
        self._mode = Mode.AS_NONE

    def assert_mode(self, *modes: List[Mode]):
        if self._mode not in modes:
            raise ValueError("Misplaced section: {}. Mode must be: {}, actual mode: {}".format(
                self._section,
                ', '.join(map(str, modes)),
                self._mode,
            ))

    def has_mode(self, *mode: List[Mode]) -> bool:
        return self._mode in mode

    def set_mode(self, mode: Mode):
        self._mode = mode
        self._writer.new_object_level()

    def int(self, name: str = None, comment: str = None) -> int:
        data = self._reader.read('int32')
        self._writer.value(data, comment, name)
        return data

    def str(self, name: str = None, comment: str = None):
        data = self._reader.read('str').replace('\r', '\\r').replace('\n', '\\n')
        self._writer.value(data, comment, name)
        return data

    def flag(self, flag_name: str):
        pass

    def comment(self, comment: str):
        pass

    def composite(self, *param_specs: List[Tuple['str', 'str']]):
        param_values = []  # type: List[Tuple[str, Any]]
        for spec_name, spec_type in param_specs:
            value = self._reader.read(spec_type)
            param_values.append((spec_name, value))

        self._writer.composite(param_values)

    def composite_array(self, *param_specs: List[Tuple['str', 'str']], length: int = None):
        if not length:
            size = self._reader.read('int32')
        else:
            size = length

        param_values_array = []  # type: List[List[Tuple[str, Any]]]

        for i in range(size):
            param_values = []  # type: List[Tuple[str, Any]]
            for n, (spec_name, spec_type) in enumerate(param_specs):
                value = self._reader.read(spec_type)
                param_values.append((spec_name, value))
            param_values_array.append(param_values)

        self._writer.composite_array(param_values_array, size=size, write_size=not length)

    def next_section(self) -> Section:
        self._section = Section(self._reader.read('int32'))
        self._writer.next_section(self._section)
        return self._section


class ScbToYamlDecoder(DecoderTrait):
    def __init__(self, in_file_io, out_file_io):
        super().__init__(in_file_io, out_file_io)

        self.mlEvSeqSize = None
        self.fnMenuFlags = 0
        self.iScreenFlag = None
        self.invMatSizeY = None
        self.invMatSizeX = None
        self.invItmShapeLen = None

    def get_prev_mode(self) -> Mode:
        if self.has_mode(Mode.AS_NONE):
            if not self.iScreenFlag:
                raise ValueError("Invalid END_BLOCK (iScreenFlag)")
            else:
                self.iScreenFlag = 0
                return Mode.AS_NONE
        elif self.has_mode(Mode.AS_INIT_SHAPE_OFFS):
            return Mode.AS_INIT_ITEM
        elif self.has_mode(Mode.AS_INIT_ITEM):
            return Mode.AS_NONE
        elif self.has_mode(Mode.AS_INIT_MATRIX):
            return Mode.AS_NONE
        elif self.has_mode(Mode.AS_INIT_MATRIX_EL):
            return Mode.AS_INIT_MATRIX
        elif self.has_mode(Mode.AS_INIT_MENU):
            if not self.iScreenFlag:
                if self.fnMenuFlags & FM_ITEM_MENU:
                    return Mode.AS_INIT_ITEM
                else:
                    return Mode.AS_NONE
            else:
                if self.fnMenuFlags & FM_ITEM_MENU:
                    return Mode.AS_INIT_ITEM
                else:
                    self.fnMenuFlags |= FM_ISCREEN_MENU
                    return Mode.AS_NONE
        elif self.has_mode(Mode.AS_INIT_MENU_ITEM):
            return Mode.AS_INIT_MENU
        elif self.has_mode(Mode.AS_INIT_BUTTON):
            return Mode.AS_NONE
        elif self.has_mode(Mode.AS_INIT_COUNTER):
            return Mode.AS_NONE
        elif self.has_mode(Mode.AS_INIT_IBS):
            return Mode.AS_NONE
        elif self.has_mode(Mode.AS_INIT_BML):
            return Mode.AS_NONE
        elif self.has_mode(Mode.AS_INIT_IND):
            return Mode.AS_NONE
        elif self.has_mode(Mode.AS_INIT_INFO_PANEL):
            return Mode.AS_NONE
        elif self.has_mode(Mode.AS_INIT_COLOR_SCHEME):
            return Mode.AS_NONE
        elif self.has_mode(Mode.AS_INIT_LOC_DATA):
            return Mode.AS_NONE
        elif self.has_mode(Mode.AS_INIT_WORLD_MAP):
            return Mode.AS_NONE
        elif self.has_mode(Mode.AS_INIT_WORLD_DATA):
            return Mode.AS_INIT_WORLD_MAP
        elif self.has_mode(Mode.AML_INIT_DATA):
            return Mode.AML_INIT_DATA_SET
        elif self.has_mode(Mode.AML_INIT_DATA_SET):
            return Mode.AS_NONE
        elif self.has_mode(Mode.AML_INIT_EVENT):
            return Mode.AML_INIT_DATA
        elif self.has_mode(Mode.AML_INIT_EVENT_COMMAND):
            return Mode.AML_INIT_EVENT
        elif self.has_mode(Mode.BM_INIT_MENU_ITEM):
            return Mode.BM_INIT_MENU
        elif self.has_mode(Mode.BM_INIT_MENU):
            return Mode.AS_NONE
        elif self.has_mode(Mode.AS_INIT_SHUTTER):
            return Mode.AS_INIT_LOC_DATA
        elif self.has_mode(Mode.AML_INIT_EVENT_SEQ):
            return Mode.AML_INIT_DATA_SET
        else:
            raise ValueError("ENDBLOCK: Unknown mode: {}".format(self._mode))

    def convert(self):
        self._reader.read('str0')
        self._reader.read('int32')
        while True:
            section = self.next_section()
            print(section)
            if section == Section.I_SCRIPT_EOF:
                break

            if section == Section.INIT_MECHOS_PRM:
                self.composite(
                    ('unused', 'int32'),
                    ('matrixId', 'int32'),
                    ('shift', 'int32'),
                    ('data', 'str')
                )
            elif section == Section.INIT_ITEM_PRM:
                self.composite(('iitem', 'int32'),
                               ('shift', 'int32'),
                               ('data', 'str'))
            elif section == Section.SET_PROMPT_TEXT:
                self.assert_mode(
                    Mode.AS_INIT_BUTTON,
                    Mode.AS_INIT_IND,
                    Mode.AS_INIT_ITEM,
                )
                if self.has_mode(Mode.AS_INIT_BUTTON):
                    self.str('aBt_promptData')
                elif self.has_mode(Mode.AS_INIT_IND):
                    self.str('aInd_promptData')
                elif self.has_mode(Mode.AS_INIT_ITEM):
                    self.str('invItm_promptData')
                else:
                    raise ValueError("Misplaced option" + str(section))
            elif section == Section.INIT_NUM_GATE_SHUTTERS:
                self.assert_mode(Mode.AS_INIT_LOC_DATA)
                self.int(comment="alloc_gate_shutters(t_id)")
            elif section == Section.ADD_MAP_INFO_FILE:
                self.assert_mode(Mode.AS_INIT_LOC_DATA)
                self.str(comment="elemPtr -> init_id(script -> get_conv_ptr());")
            elif section == Section.SET_SOUND_PATH:
                self.assert_mode(Mode.AS_INIT_LOC_DATA)
                self.str(comment="&locData -> soundResPath")
            elif section == Section.INIT_NUM_MATRIX_SHUTTERS:
                self.assert_mode(Mode.AS_INIT_LOC_DATA)
                self.composite(('i_id', 'int32'), ('sz', 'int32'))
            elif section == Section.INIT_SHUTTER_POS:
                self.assert_mode(Mode.AS_INIT_SHUTTER)
                self.composite(
                    ('id', 'int32'),
                    ('Pos[$id].X', 'int32'),
                    ('Pos[$id].Y', 'int32'),
                )
            elif section == Section.INIT_SHUTTER_DELTA:
                self.assert_mode(Mode.AS_INIT_SHUTTER)
                self.composite(
                    ('Delta.X', 'int32'),
                    ('Delta.Y', 'int32'),
                )
            elif section == Section.NEW_GATE_SHUTTER:
                self.assert_mode(Mode.AS_INIT_LOC_DATA)

                self.int(name='id')
                self.set_mode(Mode.AS_INIT_SHUTTER)
            elif section == Section.NEW_MATRIX_SHUTTER:
                self.assert_mode(Mode.AS_INIT_LOC_DATA)

                self.composite(
                    ('shutterNum', 'int32'),
                    ('id', 'int32'),
                )
                self.set_mode(Mode.AS_INIT_SHUTTER)
            elif section == Section.INIT_STARTUP_TIME:
                self.int()
            elif section == Section.SET_UPMENU_FLAG:
                self.flag('upMenuFlag')
            elif section == Section.INIT_SHUTDOWN_TIME:
                self.int()
            elif section == Section.NEW_ML_EVENT_COMMAND:
                self.assert_mode(Mode.AML_INIT_EVENT)
                self.set_mode(Mode.AML_INIT_EVENT_COMMAND)
            elif section == Section.NEW_ML_EVENT:
                self.assert_mode(Mode.AML_INIT_DATA)
                self.set_mode(Mode.AML_INIT_EVENT)
            elif section == Section.NEW_ML_DATA:
                self.assert_mode(Mode.AML_INIT_DATA_SET)
                self.set_mode(Mode.AML_INIT_DATA)
            elif section == Section.NEW_ML_EVENT_SEQ:
                self.assert_mode(Mode.AML_INIT_DATA_SET)

                self.int(name='id')
                self.mlEvSeqSize = self.int(name='size')
                self.set_mode(Mode.AML_INIT_EVENT_SEQ)
            elif section == Section.NEW_BITMAP_MENU:
                self.assert_mode(Mode.AS_NONE)
                self.set_mode(Mode.BM_INIT_MENU)
            elif section == Section.NEW_BITMAP_MENU_ITEM:
                self.assert_mode(Mode.BM_INIT_MENU)
                self.set_mode(Mode.BM_INIT_MENU_ITEM)
            elif section == Section.NEW_ML_DATA_SET:
                self.assert_mode(Mode.AS_NONE)
                self.set_mode(Mode.AML_INIT_DATA_SET)
            elif section == Section.NEW_ML_ITEM_DATA:
                self.assert_mode(Mode.AML_INIT_DATA_SET)
                self.composite(
                    ('ItemID', 'int32'),
                    ('NullLevel', 'int32'),
                    ('frameName', 'str'),
                )
            elif section == Section.INIT_ML_EVENT_KEY_CODE:
                self.assert_mode(Mode.AML_INIT_EVENT)
                self.int(name="mvEv.keys.addKey")
            elif section == Section.SET_RND_VALUE:
                self.assert_mode(Mode.AML_INIT_EVENT)
                self.int(name="mvEv.rndValue")
            elif section == Section.SET_SPEECH_CHANNEL:
                self.assert_mode(Mode.AML_INIT_DATA_SET)
                self.int()
            elif section == Section.SET_FRAME_CHECK_FLAG:
                self.assert_mode(Mode.AML_INIT_DATA)
                self.flag('AML_FRAME_CHECK')
            elif section == Section.SET_SPEECH_LEVEL:
                self.assert_mode(Mode.AML_INIT_DATA_SET)
                self.comment("mlDataSet -> SpeechPriority[t_id] = script -> read_idata()")
                self.composite(
                    ('t_id', 'int32'),
                    ('speech_level', 'int32'),
                )
            elif section == Section.SET_ML_EVENT_SEQUENCE:
                self.assert_mode(Mode.AML_INIT_EVENT, Mode.AML_INIT_EVENT_SEQ)
                if self.has_mode(Mode.AML_INIT_EVENT):
                    self.flag("AML_SEQUENCE_EVENT")
                elif self.has_mode(Mode.AML_INIT_EVENT_SEQ):
                    self.composite_array(
                        ('seq_id', 'int32'),
                        ('seq_mode', 'int32'),
                        length=self.mlEvSeqSize
                    )
            elif section == Section.INIT_ML_EVENT_CODE:
                self.assert_mode(Mode.AML_INIT_EVENT_COMMAND)
                self.composite(
                    ('code', 'int32'),
                    ('data1', 'int32'),
                    ('data2', 'int32'),
                )
            elif section == Section.INIT_ML_EVENT_STARTUP:
                self.assert_mode(Mode.AML_INIT_EVENT)
                self.int()
            elif section == Section.SET_PRIORITY:
                self.assert_mode(Mode.AML_INIT_EVENT, Mode.AML_INIT_EVENT_SEQ)
                self.int()
            elif section == Section.SET_NOT_LOCKED_FLAG:
                self.assert_mode(Mode.AML_INIT_EVENT)
                self.flag('AML_IF_NOT_LOCKED')
            elif section == Section.SET_LOCKED_FLAG:
                self.assert_mode(Mode.AML_INIT_EVENT)
                self.flag('AML_IF_LOCKED')
            elif section == Section.INIT_START_TIMER:
                self.assert_mode(Mode.AML_INIT_EVENT_COMMAND)
                self.int()
            elif section == Section.INIT_CHANNEL_ID:
                self.assert_mode(
                    Mode.AML_INIT_EVENT,
                    Mode.AML_INIT_DATA,
                    Mode.AML_INIT_EVENT_SEQ,
                )
                self.int()
            elif section == Section.INIT_ML_EVENT_SDATA:
                self.assert_mode(Mode.AML_INIT_EVENT)
                self.int()
            elif section == Section.INIT_OFFS_X:
                self.assert_mode(
                    Mode.AS_INIT_WORLD_MAP,
                    Mode.AS_INIT_IBS,
                )
                self.composite(
                    ('id', 'int32'),
                    ('OffsX', 'int32'),
                )
            elif section == Section.SET_WORLD_NAME:
                self.assert_mode(
                    Mode.AS_INIT_WORLD_DATA,
                    Mode.AML_INIT_DATA,
                    Mode.AS_INIT_LOC_DATA,
                    Mode.AS_INIT_SHUTTER,
                )
                if self.has_mode(Mode.AS_INIT_WORLD_DATA):
                    self.str()
                elif self.has_mode(Mode.AML_INIT_DATA):
                    self.str()
                elif self.has_mode(Mode.AS_INIT_LOC_DATA):
                    self.composite(
                        ('nameId', 'str'),
                        ('nameId2', 'str'),
                    )
                elif self.has_mode(Mode.AS_INIT_SHUTTER):
                    self.str()
            elif section == Section.ADD_FLAG:
                self.assert_mode(Mode.AS_INIT_WORLD_DATA)
                self.int(comment="wData -> flags |= t_id;")
            elif section == Section.ADD_LINK:
                self.assert_mode(Mode.AS_INIT_WORLD_DATA)
                self.int()
            elif section == Section.SET_MAX_STR:
                self.assert_mode(Mode.AS_INIT_INFO_PANEL)
                self.int()
            elif section == Section.INIT_INFO_OFFS_X:
                self.assert_mode(Mode.AS_INIT_INFO_PANEL)
                self.int()
            elif section == Section.INIT_BACK_COL:
                self.assert_mode(
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_MENU,
                )
                self.int()
            elif section == Section.SET_RANGE_FLAG:
                self.assert_mode(
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_COUNTER,
                )
                if self.has_mode(Mode.AS_INIT_INFO_PANEL):
                    self.flag("IP_RANGE_FONT")
                elif self.has_mode(Mode.AS_INIT_MENU):
                    self.flag("FM_RANGE_FONT")
                    self.fnMenuFlags |= FM_RANGE_FONT
                elif self.has_mode(Mode.AS_INIT_COUNTER):
                    self.flag("CP_RANGE_FONT")
            elif section == Section.SET_SUBMENU_FLAG:
                self.assert_mode(Mode.AS_INIT_MENU)
                self.flag("FM_SUBMENU")
                self.fnMenuFlags |= FM_SUBMENU
            elif section == Section.SET_MAINMENU_FLAG:
                self.assert_mode(Mode.AS_INIT_MENU)
                self.flag("FM_MAIN_MENU")
                self.fnMenuFlags |= FM_MAIN_MENU
            elif section == Section.INIT_INFO_OFFS_Y:
                self.assert_mode(Mode.AS_INIT_INFO_PANEL)
                self.int()
            elif section == Section.SET_NO_ALIGN:
                self.assert_mode(Mode.AS_INIT_INFO_PANEL)
                self.flag("IP_NO_ALIGN")
            elif section == Section.INIT_OFFS_Y:
                self.assert_mode(
                    Mode.AS_INIT_WORLD_MAP,
                    Mode.AS_INIT_IBS,
                )
                if self.has_mode(Mode.AS_INIT_WORLD_MAP):
                    self.int(name='id')
                    self.int(name='ShapeOffsY')
                elif self.has_mode(Mode.AS_INIT_IBS):
                    self.int(name='id')
                    self.int(name='PosY')
            elif section == Section.NEW_WORLD_MAP:
                self.assert_mode(
                    Mode.AS_NONE,
                )
                self.set_mode(Mode.AS_INIT_WORLD_MAP)
            elif section == Section.NEW_WORLD_DATA:
                self.assert_mode(
                    Mode.AS_INIT_WORLD_MAP,
                )

                self.int(name='id')
                self.int(name='letter')
                self.int(name='shape_id')
                self.set_mode(Mode.AS_INIT_WORLD_DATA)
            elif section == Section.TOGGLE_ISCREEN_MODE:
                self.flag("iScreenFlag")
                self.iScreenFlag = 1
            elif section == Section.I_END_BLOCK:
                self.set_mode(self.get_prev_mode())
            elif section == Section.INIT_CELL_SIZE:
                if self.iScreenFlag:
                    self.int(name='iCellSize')
                else:
                    self.int(name='aCellSize')
            elif section == Section.NEW_INV_MATRIX:
                self.assert_mode(
                    Mode.AS_NONE,
                )

                self.int(name='internalId')
                self.int(name='type')
                self.set_mode(Mode.AS_INIT_MATRIX)
            elif section == Section.NEW_INFO_PANEL:
                self.assert_mode(
                    Mode.AS_NONE,
                )
                self.set_mode(Mode.AS_INIT_INFO_PANEL)
            elif section == Section.NEW_IBS:
                self.assert_mode(
                    Mode.AS_NONE,
                )

                self.int(name='id')
                self.set_mode(Mode.AS_INIT_IBS)
            elif section == Section.NEW_IND:
                self.assert_mode(
                    Mode.AS_NONE,
                )

                self.int(name='id')
                self.set_mode(Mode.AS_INIT_IND)
            elif section == Section.NEW_BML:
                self.assert_mode(
                    Mode.AS_NONE,
                )

                self.flag("BMP_FLAG")
                self.int(name='id')
                self.set_mode(Mode.AS_INIT_BML)
            elif section == Section.NEW_INV_ITEM:
                self.assert_mode(
                    Mode.AS_NONE,
                )

                self.str(name="name")
                self.set_mode(Mode.AS_INIT_ITEM)
            elif section == Section.NEW_COUNTER:
                self.assert_mode(
                    Mode.AS_NONE,
                )

                self.int(name="type")
                self.set_mode(Mode.AS_INIT_COUNTER)
            elif section == Section.NEW_BUTTON:
                self.assert_mode(
                    Mode.AS_NONE,
                )

                self.int(name="type")
                self.set_mode(Mode.AS_INIT_BUTTON)
            elif section == Section.NEW_MENU:
                self.assert_mode(
                    Mode.AS_NONE,
                    Mode.AS_INIT_ITEM,
                )
                self.fnMenuFlags = 0
                if self.has_mode(Mode.AS_INIT_ITEM):
                    self.fnMenuFlags = FM_ITEM_MENU
                self.set_mode(Mode.AS_INIT_MENU)
            elif section == Section.NEW_MENU_ITEM:
                self.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.set_mode(Mode.AS_INIT_MENU_ITEM)
            elif section == Section.INIT_NUMVALS:
                self.assert_mode(
                    Mode.AS_INIT_IND,
                )
                self.int()
            elif section == Section.INIT_X:
                self.assert_mode(
                    Mode.AS_INIT_MATRIX,
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_BUTTON,
                    Mode.AS_INIT_IND,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_COUNTER,
                    Mode.AS_INIT_WORLD_DATA,
                    Mode.BM_INIT_MENU_ITEM,
                )
                self.int()
            elif section == Section.INIT_Y:
                self.assert_mode(
                    Mode.AS_INIT_MATRIX,
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_BUTTON,
                    Mode.AS_INIT_IND,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_COUNTER,
                    Mode.AS_INIT_WORLD_DATA,
                    Mode.BM_INIT_MENU_ITEM,
                )
                self.int()
            elif section == Section.INIT_MSX:
                self.assert_mode(
                    Mode.AS_INIT_MATRIX,
                )
                self.invMatSizeX = self.int()
            elif section == Section.SET_RAFFA_FLAG:
                self.assert_mode(
                    Mode.AS_INIT_MATRIX,
                )
                self.flag('IM_RAFFA')
            elif section == Section.SET_NUM_AVI_ID:
                self.assert_mode(
                    Mode.AS_INIT_MATRIX,
                    Mode.AS_INIT_ITEM,
                )
                self.int()
            elif section == Section.SET_ESCAVE_FLAG:
                self.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.flag('INV_ITEM_SHOW_ESCAVE')
            elif section == Section.SET_SHOW_LOAD:
                self.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.flag('INV_ITEM_SHOW_ESCAVE')
            elif section == Section.SET_TEMPLATE:
                self.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.str(name="template")
            elif section == Section.SET_ACTIVATE_FLAG:
                self.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.flag("INV_ITEM_NO_ACTIVATE")
            elif section == Section.INIT_PART_DATA:
                self.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.int(name="baseID[0]")
                self.int(name="targetID[0]")
                self.int(name="baseID[1]")
                self.int(name="targetID[1]")
            elif section == Section.SET_NO_SHOW_LOAD:
                self.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.flag("&= ~INV_ITEM_SHOW_LOAD")
            elif section == Section.SET_NOT_COMPLETED_FLAG:
                self.assert_mode(
                    Mode.AS_INIT_MATRIX,
                )
                self.flag("IM_NOT_COMPLETE")
            elif section == Section.INIT_MSY:
                self.assert_mode(
                    Mode.AS_INIT_MATRIX,
                )
                self.invMatSizeY = self.int(name="SizeY")
            elif section == Section.INIT_RADIUS:
                self.assert_mode(
                    Mode.AS_INIT_IND,
                )
                self.int(name="__no_key__")
            elif section == Section.INIT_CORNER:
                self.assert_mode(
                    Mode.AS_INIT_IND,
                )
                self.int(name="CornerNum")
            elif section == Section.INIT_IND_TYPE:
                self.assert_mode(
                    Mode.AS_INIT_IND,
                )
                self.int(name="type")
            elif section == Section.INIT_SX:
                self.assert_mode(
                    Mode.AS_INIT_ITEM,
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_BML,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_WORLD_MAP,
                    Mode.AS_INIT_COUNTER,
                    Mode.BM_INIT_MENU
                )
                self.int(name="SizeX")
            elif section == Section.INIT_SY:
                self.assert_mode(
                    Mode.AS_INIT_ITEM,
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_BML,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_WORLD_MAP,
                    Mode.AS_INIT_COUNTER,
                    Mode.BM_INIT_MENU
                )
                self.int(name="SizeY")
            elif section == Section.INIT_SLOT_TYPE:
                self.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.int(name="slotType")
            elif section == Section.INIT_AVI_ID:
                self.assert_mode(
                    Mode.AS_INIT_ITEM,
                    Mode.AS_INIT_MATRIX,
                )
                self.int(name="t_id")
                self.str(name="str_id")
            elif section == Section.INIT_COMMENTS:
                self.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.composite_array(
                    ('comment', 'str')
                )
            elif section == Section.INIT_NUM_INDEX:
                self.assert_mode(
                    Mode.AS_INIT_ITEM,
                    Mode.AS_INIT_LOC_DATA,
                )
                if self.has_mode(Mode.AS_INIT_ITEM):
                    self.int('NumIndex')
                elif self.has_mode(Mode.AS_INIT_LOC_DATA):
                    self.int('i')
                    self.int('numIndex')
            elif section == Section.INIT_SHAPE_LEN:
                self.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.invItmShapeLen = self.int('ShapeLen')
            elif section == Section.INIT_SHAPE:
                self.assert_mode(
                    Mode.AS_INIT_ITEM,
                    Mode.AS_INIT_WORLD_MAP,
                )
                if self.has_mode(Mode.AS_INIT_ITEM):

                    self.composite_array(
                        ('ShapeX', 'int32'),
                        ('ShapeY', 'int32'),
                        length=self.invItmShapeLen
                    )
                    self.set_mode(Mode.AS_INIT_SHAPE_OFFS)

                elif self.has_mode(Mode.AS_INIT_WORLD_MAP):
                    self.int('t_id')
                    self.str('shape_files[t_id]')
            elif section == Section.INIT_MATRIX_EL:
                self.assert_mode(
                    Mode.AS_INIT_MATRIX
                )

                self.composite_array(
                    ('matrix[index].type', 'int32'),
                    length=self.invMatSizeX * self.invMatSizeY
                )
                self.set_mode(Mode.AS_INIT_MATRIX_EL)
            elif section == Section.INIT_SLOT_NUMS:
                self.assert_mode(
                    Mode.AS_INIT_MATRIX
                )

                self.composite_array(
                    ('matrix[index].slotNumber', 'int32'),
                    length=self.invMatSizeX * self.invMatSizeY
                )
                self.set_mode(Mode.AS_INIT_MATRIX_EL)
            elif section == Section.INIT_SLOT_TYPES:
                self.assert_mode(
                    Mode.AS_INIT_MATRIX
                )

                self.composite_array(
                    ('matrix[index].slotType', 'int32'),
                    length=self.invMatSizeX * self.invMatSizeY
                )
                self.set_mode(Mode.AS_INIT_MATRIX_EL)
            elif section == Section.INIT_CLASS:
                self.assert_mode(
                    Mode.AS_INIT_ITEM
                )
                self.int(name="classId")
            elif section == Section.INIT_FNAME:
                self.assert_mode(
                    Mode.AS_INIT_ITEM
                )
                self.str(name="fname")
            elif section == Section.INIT_FILE:
                self.assert_mode(
                    Mode.AS_INIT_IBS,
                    Mode.AS_INIT_BML,
                )
                self.str(name="name")
            elif section == Section.INIT_BGROUND:
                self.assert_mode(
                    Mode.AS_INIT_IBS,
                )
                self.int(name="backObjID")
            elif section == Section.INIT_SEQ_NAME:
                self.assert_mode(
                    Mode.AS_INIT_BUTTON,
                )
                self.str(name="fname")
            elif section == Section.SET_CONTROL_ID:
                self.assert_mode(
                    Mode.AS_INIT_BUTTON,
                )
                self.int(name="ControlID")
            elif section == Section.INIT_EVENT_CODE:
                self.assert_mode(
                    Mode.AS_INIT_BUTTON,
                    Mode.AS_INIT_ITEM,
                    Mode.AS_INIT_MENU_ITEM,
                )
                if self.has_mode(Mode.AS_INIT_BUTTON):
                    self.int(name="code")
                    self.int(name="data")
                elif self.has_mode(Mode.AS_INIT_ITEM):
                    self.int(name='code')
                elif self.has_mode(Mode.AS_INIT_MENU_ITEM):
                    self.int(name='code')
                    self.int(name="data")
            elif section == Section.SET_UNPRESS:
                self.assert_mode(
                    Mode.AS_INIT_BUTTON,
                )
                self.flag("B_UNPRESS")
            elif section == Section.INIT_ACTIVE_TIME:
                self.assert_mode(
                    Mode.AS_INIT_BUTTON,
                    Mode.AS_INIT_MENU,
                    Mode.AML_INIT_EVENT,
                    Mode.BM_INIT_MENU,
                )
                self.int(name="activeCount")
            elif section == Section.INIT_FNC_CODE:
                self.assert_mode(
                    Mode.AS_INIT_MENU_ITEM,
                )
                self.int(name="fnc_code")
            elif section == Section.SET_NO_DELETE_FLAG:
                self.assert_mode(
                    Mode.AS_INIT_MENU_ITEM,
                )
                self.flag('FM_NO_DELETE')
            elif section == Section.SET_SUBMENU_ID:
                self.assert_mode(
                    Mode.AS_INIT_MENU_ITEM,
                )
                self.int(name='submenuID')
                self.flag('FM_SUBMENU_ITEM')
            elif section == Section.SET_BSUBMENU_ID:
                self.assert_mode(
                    Mode.AS_INIT_MENU_ITEM,
                )
                self.int(name='submenuID')
                self.flag('FM_BSUBMENU_ITEM')
            elif section == Section.SET_NUM_V_ITEMS:
                self.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.int(name='VItems')
            elif section == Section.INIT_SPACE:
                self.assert_mode(
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_MENU_ITEM,
                )
                self.int(name='vSpace')
            elif section == Section.SET_NO_DEACTIVATE_FLAG:
                self.assert_mode(
                    Mode.AS_INIT_MENU,
                    Mode.AML_INIT_EVENT,
                )
                self.flag('FM_NO_DEACTIVATE')
            elif section == Section.SET_LOCATION_MENU_FLAG:
                self.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.flag('FM_LOCATION_MENU')
            elif section == Section.SET_BML_NAME:
                self.assert_mode(
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_IND,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.BM_INIT_MENU_ITEM,
                )
                if self.has_mode(Mode.AS_INIT_MENU):
                    self.str('bml_name')
                elif self.has_mode(Mode.AS_INIT_IND):
                    self.str('bml.name')
                elif self.has_mode(Mode.AS_INIT_INFO_PANEL):
                    self.str('bml_name')
                elif self.has_mode(Mode.BM_INIT_MENU_ITEM):
                    self.str('fname')
            elif section == Section.INIT_BACK_BML:
                self.assert_mode(
                    Mode.AS_INIT_MATRIX,
                )
                self.str()
            elif section == Section.SET_IBS_NAME:
                self.assert_mode(
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_COUNTER,
                )
                self.str()
            elif section == Section.SET_MAP_NAME:
                if self.has_mode(Mode.AS_INIT_LOC_DATA):
                    self.str()
                else:
                    self.int('t_id')
                    self.str()
            elif section == Section.SET_SAVE_SCREEN_ID:
                self.assert_mode(
                    Mode.AS_INIT_LOC_DATA,
                )
                self.int('SaveScreenID')
            elif section == Section.SET_WORLD_ID:
                self.assert_mode(
                    Mode.AS_INIT_LOC_DATA,
                )
                self.int('WorldID')
            elif section == Section.SET_EXCLUDE:
                self.assert_mode(
                    Mode.AS_INIT_LOC_DATA,
                )
                self.int('t_id')
            elif section == Section.INIT_SCREEN_ID:
                self.assert_mode(
                    Mode.AS_INIT_LOC_DATA,
                )
                self.str('screenID')
            elif section == Section.INIT_PAL_NAME:
                self.assert_mode(
                    Mode.AS_INIT_LOC_DATA,
                )
                self.str('palName')
            elif section == Section.INIT_CUR_FNC:
                self.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.int('curFunction')
            elif section == Section.INIT_FONT:
                self.assert_mode(
                    Mode.AS_INIT_MENU_ITEM,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_WORLD_DATA,
                    Mode.AS_INIT_COUNTER,
                    Mode.AS_INIT_IBS,
                )
                self.int('font')
            elif section == Section.INIT_VSPACE:
                self.assert_mode(
                    Mode.AS_INIT_INFO_PANEL,
                )
                self.int('vSpace')
            elif section == Section.INIT_HSPACE:
                self.assert_mode(
                    Mode.AS_INIT_INFO_PANEL,
                )
                self.int('hSpace')
            elif section == Section.INIT_STRING:
                self.assert_mode(
                    Mode.AS_INIT_MENU_ITEM,
                )
                self.str('name')
            elif section == Section.INIT_SCANCODE:
                self.assert_mode(
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_MENU_ITEM,
                    Mode.AS_INIT_BUTTON,
                    Mode.AML_INIT_EVENT,
                )
                self.int('key')
            elif section == Section.INIT_MENU_TYPE:
                self.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.int('type')
            elif section == Section.INIT_UP_KEY:
                self.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.int('up_key')
            elif section == Section.INIT_DOWN_KEY:
                self.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.int('down_key')
            elif section == Section.INIT_TRIGGER:
                self.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.int('trigger_code')
            elif section == Section.INIT_ID:
                self.assert_mode(
                    Mode.AS_INIT_BUTTON,
                    Mode.AS_INIT_ITEM,
                    Mode.AS_INIT_LOC_DATA,
                    Mode.AS_INIT_MATRIX,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_COUNTER,
                    Mode.AML_INIT_DATA_SET,
                    Mode.AML_INIT_DATA,
                    Mode.BM_INIT_MENU_ITEM,
                    Mode.BM_INIT_MENU,
                    Mode.AML_INIT_EVENT_SEQ,
                )
                if self.has_mode(Mode.AS_INIT_LOC_DATA):
                    self.int('t_id')
                    self.str('id')
                elif self.has_mode(Mode.AS_INIT_MATRIX):
                    self.str('id')
                else:
                    self.int('id')
            elif section == Section.INIT_S_ID:
                self.assert_mode(
                    Mode.AS_INIT_LOC_DATA,
                )
                self.int('t_id')
                self.str('s_objIDs[$t_id]')
            elif section == Section.INIT_MODE_KEY:
                self.int('key')
            elif section == Section.INIT_INV_KEY:
                self.int('key')
            elif section == Section.INIT_INFO_KEY:
                self.int('key')
            elif section == Section.SET_CURMATRIX:
                self.int('curMatrix')
            elif section == Section.INIT_CUR_IBS:
                self.int('curIbsID')
            elif section == Section.NEW_LOC_DATA:
                self.assert_mode(Mode.AS_NONE)

                self.int(name='id')
                self.set_mode(Mode.AS_INIT_LOC_DATA)
            elif section == Section.NEW_COL_SCHEME:
                if self.has_mode(Mode.AS_INIT_LOC_DATA):
                    self.int(name='numColorScheme')
                self.int('curScheme')
                self.set_mode(Mode.AS_INIT_COLOR_SCHEME)
            elif section == Section.INIT_NUM_SCHEMES:
                self.int('aciNumColSchemes')
            elif section == Section.INIT_SCHEME_LEN:
                self.int('aciColSchemeLen')
            elif section == Section.INIT_COLOR:
                self.assert_mode(Mode.AS_INIT_COLOR_SCHEME)
                self.int('t_id')
                self.int('scheme')
            else:
                raise ValueError("Invalid section: {}".format(section))
            self._writer.end_section()
        self._writer.flush()
