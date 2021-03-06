from enum import Enum


class Section(Enum):
    I_END_BLOCK = 0
    I_END_STRING = 1
    INIT_MODE_KEY = 2
    INIT_INV_KEY = 3
    INIT_INFO_KEY = 4
    INIT_CELL_SIZE = 5
    NEW_INV_MATRIX = 6
    NEW_INV_ITEM = 7
    NEW_MENU = 8
    NEW_MENU_ITEM = 9
    NEW_BUTTON = 10
    INT_BUTTON_TYPE = 11
    INV_BUTTON_TYPE = 12
    INF_BUTTON_TYPE = 13
    INIT_X = 14
    INIT_Y = 15
    INIT_SX = 16
    INIT_SY = 17
    INIT_MSX = 18
    INIT_MSY = 19
    INIT_SCANCODE = 20
    INIT_CLASS = 21
    ITEM_BASE = 22
    ITEM_WEAPON = 23
    INIT_FNC_CODE = 24
    INIT_SPACE = 25
    INIT_FONT = 26
    INIT_STRING = 27
    INIT_CUR_FNC = 28
    INIT_FNAME = 29
    INIT_SEQ_NAME = 30
    INIT_EVENT_CODE = 31
    INIT_ACTIVE_TIME = 32
    INIT_MATRIX_EL = 33
    INIT_MENU_TYPE = 34
    INIT_UP_KEY = 35
    INIT_DOWN_KEY = 36
    INIT_TRIGGER = 37
    INIT_ID = 38
    SET_UNPRESS = 39
    SET_BML_NAME = 40
    SET_IBS_NAME = 41
    SET_MAP_NAME = 42
    SET_BCELL_NAME = 43
    SET_WCELL_NAME = 44
    SET_CURMATRIX = 45
    NEW_IBS = 46
    NEW_BML = 47
    INIT_FILE = 48
    INIT_BGROUND = 49
    INIT_CUR_IBS = 50
    INIT_SLOT_NUMS = 51
    INIT_SLOT_TYPES = 52
    INIT_SLOT_NUM = 53
    INIT_SLOT_TYPE = 54
    NEW_IND = 55
    INIT_RADIUS = 56
    INIT_MAX_VAL = 57
    INIT_CORNER = 58
    INIT_IND_TYPE = 59
    INIT_SHAPE_LEN = 60
    INIT_SHAPE = 61
    INIT_NUM_INDEX = 62
    INIT_BACK_BML = 63
    NEW_INFO_PANEL = 64
    INIT_VSPACE = 65
    INIT_HSPACE = 66
    NEW_COUNTER = 67
    INT_COUNTER = 68
    INF_COUNTER = 69
    INV_COUNTER = 70
    INIT_NUMVALS = 71
    INIT_NUM_SCHEMES = 72
    INIT_SCHEME_LEN = 73
    NEW_COL_SCHEME = 74
    INIT_COLOR = 75
    TOGGLE_ISCREEN_MODE = 76
    NEW_LOC_DATA = 77
    INIT_SCREEN_ID = 78
    INIT_PAL_NAME = 79
    INIT_S_ID = 80
    NEW_WORLD_MAP = 81
    NEW_WORLD_DATA = 82
    INIT_OFFS_X = 83
    INIT_OFFS_Y = 84
    ADD_FLAG = 85
    ADD_LINK = 86
    INIT_INFO_OFFS_X = 87
    INIT_INFO_OFFS_Y = 88
    SET_NO_ALIGN = 89
    SET_WORLD_NAME = 90
    INIT_COMMENTS = 91
    INIT_AVI_ID = 92
    INIT_BACK_COL = 93
    SET_MAX_STR = 94
    SET_NO_DEACTIVATE_FLAG = 95
    SET_LOCATION_MENU_FLAG = 96
    SET_NUM_V_ITEMS = 97
    NEW_ML_EVENT_COMMAND = 98
    NEW_ML_EVENT = 99
    NEW_ML_DATA = 100
    INIT_ML_EVENT_CODE = 101
    INIT_ML_EVENT_STARTUP = 102
    INIT_ML_EVENT_SDATA = 103
    INIT_STARTUP_TIME = 104
    INIT_SHUTDOWN_TIME = 105
    INIT_START_TIMER = 106
    INIT_CHANNEL_ID = 107
    NEW_ML_DATA_SET = 108
    INIT_ML_EVENT_KEY_CODE = 109
    SET_ML_EVENT_SEQUENCE = 110
    SET_SUBMENU_FLAG = 111
    SET_NUM_AVI_ID = 112
    SET_SHOW_LOAD = 113
    SET_NO_SHOW_LOAD = 114
    NEW_BITMAP_MENU = 115
    NEW_BITMAP_MENU_ITEM = 116
    SET_EXCLUDE = 117
    NEW_ML_ITEM_DATA = 118
    SET_UPMENU_FLAG = 119
    SET_SUBMENU_ID = 120
    SET_BSUBMENU_ID = 121
    SET_MAINMENU_FLAG = 122
    SET_NO_DELETE_FLAG = 123
    SET_DOOR_ID = 124
    SET_SHAPE_ID = 125
    INIT_PART_DATA = 126
    NEW_GATE_SHUTTER = 127
    NEW_MATRIX_SHUTTER = 128
    INIT_SHUTTER_POS = 129
    INIT_SHUTTER_DELTA = 130
    INIT_NUM_GATE_SHUTTERS = 131
    INIT_NUM_MATRIX_SHUTTERS = 132
    SET_NOT_COMPLETED_FLAG = 133
    SET_PROMPT_TEXT = 134
    SET_SAVE_SCREEN_ID = 135
    SET_WORLD_ID = 136
    SET_RAFFA_FLAG = 137
    SET_PRIORITY = 138
    SET_NOT_LOCKED_FLAG = 139
    SET_LOCKED_FLAG = 140
    SET_SOUND_PATH = 141
    NEW_ML_EVENT_SEQ = 142
    SET_SPEECH_CHANNEL = 143
    SET_SPEECH_LEVEL = 144
    SET_RND_VALUE = 145
    SET_CONTROL_ID = 146
    SET_FRAME_CHECK_FLAG = 147
    INIT_MECHOS_PRM = 148
    INIT_ITEM_PRM = 149
    SET_RANGE_FLAG = 150
    SET_ACTIVATE_FLAG = 151
    SET_TEMPLATE = 152
    SET_ESCAVE_FLAG = 153
    ADD_MAP_INFO_FILE = 154
    I_SCRIPT_EOF = 8383


class Mode(Enum):
    AS_NONE = 0
    AS_INIT_MATRIX = 1
    AS_INIT_BUTTON = 2
    AS_INIT_ITEM = 3
    AS_INIT_MATRIX_EL = 4
    AS_INIT_MENU = 5
    AS_INIT_MENU_ITEM = 6
    AS_INIT_IBS = 7
    AS_INIT_BML = 8
    AS_INIT_IND = 9
    AS_INIT_SHAPE_OFFS = 10
    AS_INIT_INFO_PANEL = 11
    AS_INIT_COUNTER = 12
    AS_INIT_COLOR_SCHEME = 13
    AS_INIT_LOC_DATA = 14
    AS_INIT_WORLD_MAP = 15
    AS_INIT_WORLD_DATA = 16
    AML_INIT_EVENT_COMMAND = 17
    AML_INIT_EVENT = 18
    AML_INIT_DATA_SET = 19
    AML_INIT_DATA = 20
    AML_INIT_EVENT_SEQ = 21
    BM_INIT_MENU_ITEM = 22
    BM_INIT_MENU = 23
    AS_INIT_SHUTTER = 24
