from vangers_utils.script.options import Section, Mode
# from vangers_utils.script.writer import Writer
from vangers_utils.script.writer import Writer
from vangers_utils.script.yaml_writer import YamlWriter

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

class Converter:
    def __init__(self, in_file: str, out_file: str):
        self.writer = Writer(in_file, out_file)
        # self.writer = YamlWriter(in_file, out_file)
        self.mlEvSeqSize = None
        self.fnMenuFlags = 0
        self.iScreenFlag = None
        self.invMatSizeY = None
        self.invMatSizeX = None
        self.invItmShapeLen = None

    def get_prev_mode(self)->Mode:
        #switch(curMode){
        #        case AS_NONE:
        if self.writer.has_mode(Mode.AS_NONE):
            if not self.iScreenFlag:
                raise ValueError("Invalid END_BLOCK (iScreenFlag)")
            else:
                self.iScreenFlag = 0
                return Mode.AS_NONE
        #//            if(!self.iScreenFlag)
        #//                _handle_error("Misplaced \"}\"");
        #//            else
        #//                self.iScreenFlag = 0;
        #            break;
        #        case AS_INIT_SHAPE_OFFS:
        elif self.writer.has_mode(Mode.AS_INIT_SHAPE_OFFS):
            return Mode.AS_INIT_ITEM
        #            curMode = AS_INIT_ITEM;
        #            break;
        #        case AS_INIT_ITEM:
        elif self.writer.has_mode(Mode.AS_INIT_ITEM):
            return Mode.AS_NONE
        #            curMode = AS_NONE;
        #//            if(self.iScreenFlag)
        #//                aScrDisp -> add_iitem(invItm);
        #//            else
        #//                aScrDisp -> add_item(invItm);
        #            break;
        #        case AS_INIT_MATRIX:
        elif self.writer.has_mode(Mode.AS_INIT_MATRIX):
            return Mode.AS_NONE
        #            curMode = AS_NONE;
        #//            if(self.iScreenFlag)
        #//                aScrDisp -> add_imatrix(invMat);
        #//            else
        #//                aScrDisp -> add_matrix(invMat);
        #            break;
        #        case AS_INIT_MATRIX_EL:
        elif self.writer.has_mode(Mode.AS_INIT_MATRIX_EL):
            return Mode.AS_INIT_MATRIX
        #            curMode = AS_INIT_MATRIX;
        #            break;
        #        case AS_INIT_MENU:
        elif self.writer.has_mode(Mode.AS_INIT_MENU):
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
        #            if(!self.iScreenFlag){
        #                if(self.fnMenuFlags & FM_ITEM_MENU){
        #                    curMode = AS_INIT_ITEM;
        #//                    aScrDisp -> add_menu(fnMnu);
        #//                    invItm -> menu = (iListElement*)fnMnu;
        #                }
        #                else {
        #                    curMode = AS_NONE;
        #//                    aScrDisp -> add_menu(fnMnu);
        #                }
        #            }
        #            else {
        #                if(self.fnMenuFlags & FM_ITEM_MENU){
        #                    curMode = AS_INIT_ITEM;
        #//                    invItm -> menu = (iListElement*)fnMnu;
        #                }
        #                else {
        #                    curMode = AS_NONE;
        #                    self.fnMenuFlags |= FM_ISCREEN_MENU;
        #//                    aScrDisp -> add_imenu(fnMnu);
        #                }
        #            }
        #            break;
        #        case AS_INIT_MENU_ITEM:
        elif self.writer.has_mode(Mode.AS_INIT_MENU_ITEM):
            return Mode.AS_INIT_MENU
        #            curMode = AS_INIT_MENU;
        #//            if(upMenuFlag){
        #//                fnMnu -> upMenuItem = fnMnuItm;
        #//                upMenuFlag = 0;
        #//            }
        #//            else
        #//                fnMnu -> add_item(fnMnuItm);
        #            break;
        #        case AS_INIT_BUTTON:
        elif self.writer.has_mode(Mode.AS_INIT_BUTTON):
            return Mode.AS_NONE
        #            curMode = AS_NONE;
        #//            if(aBt -> type == INTERF_BUTTON)
        #//                aScrDisp -> intButtons -> connect((iListElement*)aBt);
        #//            if(aBt -> type == INV_BUTTON)
        #//                aScrDisp -> invButtons -> connect((iListElement*)aBt);
        #//            if(aBt -> type == INFO_BUTTON)
        #//                aScrDisp -> infButtons -> connect((iListElement*)aBt);
        #            break;
        #        case AS_INIT_COUNTER:
        elif self.writer.has_mode(Mode.AS_INIT_COUNTER):
            return Mode.AS_NONE
        #            curMode = AS_NONE;
        #//            if(self.iScreenFlag){
        #//                aScrDisp -> i_Counters -> connect((iListElement*)cP);
        #//            }
        #//            else {
        #//                if(cP -> type == CP_INT)
        #//                    aScrDisp -> intCounters -> connect((iListElement*)cP);
        #//                if(cP -> type == CP_INV)
        #//                    aScrDisp -> invCounters -> connect((iListElement*)cP);
        #//                if(cP -> type == CP_INF)
        #//                    aScrDisp -> infCounters -> connect((iListElement*)cP);
        #//            }
        #            break;
        #        case AS_INIT_IBS:
        elif self.writer.has_mode(Mode.AS_INIT_IBS):
            return Mode.AS_NONE
        #//            aScrDisp -> ibsList -> connect((iListElement*)ibsObj);
        #            curMode = AS_NONE;
        #            break;
        #        case AS_INIT_BML:
        elif self.writer.has_mode(Mode.AS_INIT_BML):
            return Mode.AS_NONE
        #//            aScrDisp -> backList -> connect((iListElement*)bmlObj);
        #            curMode = AS_NONE;
        #            break;
        #        case AS_INIT_IND:
        elif self.writer.has_mode(Mode.AS_INIT_IND):
            return Mode.AS_NONE
        #//            aScrDisp -> add_ind(aInd);
        #            curMode = AS_NONE;
        #            break;
        #        case AS_INIT_INFO_PANEL:
        elif self.writer.has_mode(Mode.AS_INIT_INFO_PANEL):
            return Mode.AS_NONE
        #//            if(self.iScreenFlag){
        #//                if(!iPl -> type)
        #//                    aScrDisp -> iscr_iP = iPl;
        #//                else {
        #//                    aScrDisp -> i_infoPanels -> connect((iListElement*)iPl);
        #//                }
        #//            }
        #//            else {
        #//                if(!iPl -> type)
        #//                    aScrDisp -> iP = iPl;
        #//                else {
        #//                    aScrDisp -> infoPanels -> connect((iListElement*)iPl);
        #//                }
        #//            }
        #            curMode = AS_NONE;
        #            break;
        #        case AS_INIT_COLOR_SCHEME:
        elif self.writer.has_mode(Mode.AS_INIT_COLOR_SCHEME):
            return Mode.AS_NONE
        #            curMode = AS_NONE;
        #            break;
        #        case AS_INIT_LOC_DATA:
        elif self.writer.has_mode(Mode.AS_INIT_LOC_DATA):
            return Mode.AS_NONE
        #//            aScrDisp -> add_locdata(locData);
        #            curMode = AS_NONE;
        #            break;
        #        case AS_INIT_WORLD_MAP:
        elif self.writer.has_mode(Mode.AS_INIT_WORLD_MAP):
            return Mode.AS_NONE
        #//            aScrDisp -> wMap = wMap;
        #            curMode = AS_NONE;
        #            break;
        #        case AS_INIT_WORLD_DATA:
        elif self.writer.has_mode(Mode.AS_INIT_WORLD_DATA):
            return Mode.AS_INIT_WORLD_MAP
        #//            wMap -> world_list -> connect((iListElement*)wData);
        #//            wData -> owner = (iListElement*)wMap;
        #            curMode = AS_INIT_WORLD_MAP;
        #            break;
        #        case AML_INIT_DATA:
        elif self.writer.has_mode(Mode.AML_INIT_DATA):
            return Mode.AML_INIT_DATA_SET
        #//            mlDataSet -> add_data(mlData);
        #            curMode = AML_INIT_DATA_SET;
        #            break;
        #        case AML_INIT_DATA_SET:
        elif self.writer.has_mode(Mode.AML_INIT_DATA_SET):
            return Mode.AS_NONE
        #//            aciML_D -> add_data_set(mlDataSet);
        #            curMode = AS_NONE;
        #            break;
        #        case AML_INIT_EVENT:
        elif self.writer.has_mode(Mode.AML_INIT_EVENT):
            return Mode.AML_INIT_DATA
        #//            mlData -> add_event(mlEv);
        #            curMode = AML_INIT_DATA;
        #            break;
        #        case AML_INIT_EVENT_COMMAND:
        elif self.writer.has_mode(Mode.AML_INIT_EVENT_COMMAND):
            return Mode.AML_INIT_EVENT
        #//            mlEv -> add_command(mlEvComm);
        #            curMode = AML_INIT_EVENT;
        #            break;
        #        case BM_INIT_MENU_ITEM:
        elif self.writer.has_mode(Mode.BM_INIT_MENU_ITEM):
            return Mode.BM_INIT_MENU
        #//            aciBM -> add_item(aciBM_it);
        #            curMode = BM_INIT_MENU;
        #            break;
        #        case BM_INIT_MENU:
        elif self.writer.has_mode(Mode.BM_INIT_MENU):
            return Mode.AS_NONE
        #//            aScrDisp -> add_bmenu(aciBM);
        #            curMode = AS_NONE;
        #            break;
        #        case AS_INIT_SHUTTER:
        elif self.writer.has_mode(Mode.AS_INIT_SHUTTER):
            return Mode.AS_INIT_LOC_DATA
        #            curMode = AS_INIT_LOC_DATA;
        #//            locSh -> init();
        #            break;
        #        case AML_INIT_EVENT_SEQ:
        elif self.writer.has_mode(Mode.AML_INIT_EVENT_SEQ):
            return Mode.AML_INIT_DATA_SET
        #//            mlDataSet -> add_seq(mlEvSeq);
        #            curMode = AML_INIT_DATA_SET;
        #            break;
        #    }
        #    self.writer.mode(curMode);
        else:
            raise ValueError("ENDBLOCK: Unknown mode: {}".format(self.writer._mode))

    def convert(self):
        

        t = self.writer._reader.read('str0')
        cmprs = self.writer._reader.read('int32')
        print(t)
        print(cmprs)
        while True:
            section = self.writer.new_section()
            if section == None:
                break
            #    while(!script1 -> EOF_Flag){
            ##ifndef _BINARY_SCRIPT_
            #        if(script -> curBlock && *script -> curBlock -> data){
            ##endif
            #        id = self.writer.newSection();
            #
            ##ifndef _BINARY_SCRIPT_
            #        if(id == -1)
            #                _handle_error("Unknown keyword",script -> prevStrBuf);
            ##else
            #        if(id == iSCRIPT_EOF) script1 -> EOF_Flag = 1;
            #        if(id == -1)
            #            std::cerr<<"Unknown keyword"<<std::endl;
            ##endif
            #
            # //        self.writer.mode(curMode);
            #        switch(id){
            if section == Section.INIT_MECHOS_PRM:
                self.writer.composite(
                    ('unused', 'int32'),
                    ('matrixId', 'int32'),
                    ('shift', 'int32'),
                    ('data', 'str')
                )

                #            case INIT_MECHOS_PRM:
                #                self.writer.intValue("unused")
                #                self.writer.intValue("matrixId", "aScrDisp -> get_imatrix(t_id)");
                # //                mtx = aScrDisp -> get_imatrix(t_id);
                # //                if(mtx){
                # //                    t_id = script -> read_idata();
                #                self.writer.intValue("t_id2", "pData + t_id * ACI_MAX_PRM_LEN");
                #                self.writer.intValue("t_id3", nullptr);
                # //                    if(!mtx -> pData) mtx -> alloc_prm();
                # //                    ptr = mtx -> pData + t_id * ACI_MAX_PRM_LEN;
                #                self.writer.strValue("pdata");
                # //                }
                # //                else
                # //                    _handle_error("Bad matrix ID");
                #                break;
                #            case INIT_ITEM_PRM:
            elif section == Section.INIT_ITEM_PRM:
                self.writer.composite(('iitem', 'int32'),
                                 ('shift', 'int32'),
                                 ('data', 'str'))
        # //                t_id = script -> read_idata();
        # //                itm = aScrDisp -> get_iitem(t_id);
        #                self.writer.intValue("t_id1", "aScrDisp -> get_iitem(t_id)");
        # //                if(itm){
        # //                    t_id = script -> read_idata();
        # //                    if(!itm -> pData) itm -> alloc_prm();
        # //                    ptr = itm -> pData + t_id * ACI_MAX_PRM_LEN;
        #                self.writer.intValue("t_id2", "pData + t_id * ACI_MAX_PRM_LEN");
        # //                    script -> read_pdata(&ptr);
        #                self.writer.strValue("pdata");
        # //                }
        # //                else
        # //                    _handle_error("Bad item ID");
        #                break;
        #            case SET_PROMPT_TEXT:
            elif section == Section.SET_PROMPT_TEXT:
                self.writer.assert_mode(
                    Mode.AS_INIT_BUTTON,
                    Mode.AS_INIT_IND,
                    Mode.AS_INIT_ITEM,
                )
        #                if(curMode == AS_INIT_BUTTON){
                if self.writer.has_mode(Mode.AS_INIT_BUTTON):
                    self.writer.str('aBt_promptData')
        #                    self.writer.strValue("aBt_promptData");
        # //                    script -> read_pdata(&aBt -> promptData,1);
        #                }
        #                else {
        #                    if(curMode == AS_INIT_IND){
                elif self.writer.has_mode(Mode.AS_INIT_IND):
                    self.writer.str('aInd_promptData')
        #                        self.writer.strValue("aInd_promptData");
        # //                        script -> read_pdata(&aInd -> promptData,1);
        #                    }
        #                    else {
        #                        if(curMode == AS_INIT_ITEM){
                elif self.writer.has_mode(Mode.AS_INIT_ITEM):
                    self.writer.str('invItm_promptData')
                else:
                    raise ValueError("Misplaced option"+str(section))
        #                            self.writer.strValue("invItm_promptData");
        # //                            script -> read_pdata(&invItm -> promptData,1);
        #                        }
        #                        else{
        #                            _handle_error("Misplaced option",aOptIDs[id]);
        #                        }
        #
        #                    }
        #                }
        #                break;
        #            case INIT_NUM_GATE_SHUTTERS:
            elif section == Section.INIT_NUM_GATE_SHUTTERS:
                self.writer.assert_mode(Mode.AS_INIT_LOC_DATA)
                self.writer.int(comment="alloc_gate_shutters(t_id)")
        #                if(curMode == AS_INIT_LOC_DATA){
        # //                    t_id = script -> read_idata();
        # //                    locData -> alloc_gate_shutters(t_id);
        #                    self.writer.intValue("t_id1", "alloc_gate_shutters(t_id)");
        #                }
        #                else
        #                    _handle_error("Misplaced option",aOptIDs[id]);
        #                break;
        #            case ADD_MAP_INFO_FILE:
            elif section == Section.ADD_MAP_INFO_FILE:
                self.writer.assert_mode(Mode.AS_INIT_LOC_DATA)
                self.writer.str(comment="elemPtr -> init_id(script -> get_conv_ptr());")
        #                if(curMode == AS_INIT_LOC_DATA){
        #                    self.writer.strValue("id", "elemPtr -> init_id(script -> get_conv_ptr());");
        # //                    script -> prepare_pdata();
        # //                    elemPtr = new iListElement;
        # //                    elemPtr -> init_id(script -> get_conv_ptr());
        # //                    locData -> mapData -> connect(elemPtr);
        #
        #                }
        #                else
        #                    _handle_error("Misplaced option",aOptIDs[id]);
        #                break;
        #            case SET_SOUND_PATH:
            elif section == Section.SET_SOUND_PATH:
                self.writer.assert_mode(Mode.AS_INIT_LOC_DATA)
                self.writer.str(comment="&locData -> soundResPath")
        #                if(curMode == AS_INIT_LOC_DATA){
        #                    self.writer.strValue("&locData -> soundResPath");
        # //                    script -> read_pdata(&locData -> soundResPath,1);
        #                }
        #                else
        #                    _handle_error("Misplaced option",aOptIDs[id]);
        #                break;
        #            case INIT_NUM_MATRIX_SHUTTERS:
            elif section == Section.INIT_NUM_MATRIX_SHUTTERS:
                self.writer.assert_mode(Mode.AS_INIT_LOC_DATA)
                self.writer.composite(('i_id', 'int32'), ('sz', 'int32'))
                #                if(curMode == AS_INIT_LOC_DATA){
                # //                    t_id = script -> read_idata();
                # //                    sz = script -> read_idata();
                #                    self.writer.intValue("t_id");
                #                    self.writer.intValue("zs", "locData -> alloc_matrix_shutters(t_id,sz)");
                # //                    locData -> alloc_matrix_shutters(t_id,sz);
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_SHUTTER_POS:
            elif section == Section.INIT_SHUTTER_POS:
                self.writer.assert_mode(Mode.AS_INIT_SHUTTER)
                self.writer.composite(
                    ('id', 'int32'),
                    ('Pos[$id].X', 'int32'),
                    ('Pos[$id].Y', 'int32'),
                )
                #                if(curMode == AS_INIT_SHUTTER){
                # //                    t_id = script -> read_idata();
                #                    self.writer.intValue("t_id");
                # //                    locSh -> Pos[t_id].X = script -> read_idata();
                # //                    locSh -> Pos[t_id].Y = script -> read_idata();
                #                    self.writer.intValue("pos_x", "locSh -> Pos[t_id].X = script -> read_idata()");
                #                    self.writer.intValue("pos_y", "locSh -> Pos[t_id].Y = script -> read_idata()");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_SHUTTER_DELTA:
            elif section == Section.INIT_SHUTTER_DELTA:
                self.writer.assert_mode(Mode.AS_INIT_SHUTTER)
                self.writer.composite(
                    ('Delta.X', 'int32'),
                    ('Delta.Y', 'int32'),
                )
                #                if(curMode == AS_INIT_SHUTTER){
                # //                    locSh -> Delta.X = script -> read_idata();
                # //                    locSh -> Delta.Y = script -> read_idata();
                #                    self.writer.intValue("Delta.X", "locSh -> Delta.X = script -> read_idata()");
                #                    self.writer.intValue("Delta.Y", "locSh -> Delta.Y = script -> read_idata()");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case NEW_GATE_SHUTTER:
            elif section == Section.NEW_GATE_SHUTTER:
                self.writer.assert_mode(Mode.AS_INIT_LOC_DATA)
                
                self.writer.int(name='id')
                self.writer.set_mode(Mode.AS_INIT_SHUTTER)
                #                if(curMode == AS_INIT_LOC_DATA){
                #                    curMode = AS_INIT_SHUTTER;
                #                    self.writer.mode(curMode);
                # //                    locSh = new aciLocationShutterInfo;
                #
                # //                    t_id = script -> read_idata();
                #                    self.writer.intValue("t_id", "locData -> GateShutters[t_id] = locSh");
                # //                    if(t_id < 0 || t_id >= locData -> numGateShutters) ErrH.Abort("Bad shutter index...");
                # //                    locData -> GateShutters[t_id] = locSh;
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case NEW_MATRIX_SHUTTER:
            elif section == Section.NEW_MATRIX_SHUTTER:
                self.writer.assert_mode(Mode.AS_INIT_LOC_DATA)
                
                self.writer.composite(
                    ('shutterNum', 'int32'),
                    ('id', 'int32'),
                )
                self.writer.set_mode(Mode.AS_INIT_SHUTTER)
                #                if(curMode == AS_INIT_LOC_DATA){
                #                    curMode = AS_INIT_SHUTTER;
                #                    self.writer.mode(curMode);
                # //                    t_id = script -> read_idata();
                #                    self.writer.intValue("t_id", "locData -> MatrixShutters${t_id}[sz] = locSh");
                # //                    sz = script -> read_idata();
                #                    self.writer.intValue("sz");
                # //                    locSh = new aciLocationShutterInfo;
                # //                    if(t_id == 1) num = locData -> numMatrixShutters1;
                # //                    else num = locData -> numMatrixShutters2;
                # //                    if(sz < 0 || sz >= num)
                # //                        ErrH.Abort("Bad shutter index...");
                # //                    if(t_id == 1)
                # //                        locData -> MatrixShutters1[sz] = locSh;
                # //                    else
                # //                        locData -> MatrixShutters2[sz] = locSh;
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_STARTUP_TIME:
            elif section == Section.INIT_STARTUP_TIME:
                self.writer.int()
                # //                aciML_D -> startup_timer = script -> read_idata();
                #                self.writer.intValue("aciML_D.startup_timer");
                #                break;
            #            case SET_UPMENU_FLAG:
            elif section == Section.SET_UPMENU_FLAG:
                self.writer.flag('upMenuFlag')
                # //                upMenuFlag = 1;
                #                break;
            #            case INIT_SHUTDOWN_TIME:
            elif section == Section.INIT_SHUTDOWN_TIME:
                self.writer.int()
                # //                aciML_D -> shutdown_timer = script -> read_idata();
                #                self.writer.intValue("aciML_D.shutdown_timer");
                #                break;
            #            case NEW_ML_EVENT_COMMAND:
            elif section == Section.NEW_ML_EVENT_COMMAND:
                self.writer.assert_mode(Mode.AML_INIT_EVENT)
                self.writer.set_mode(Mode.AML_INIT_EVENT_COMMAND)
                #                if(curMode != AML_INIT_EVENT)
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                mlEvComm = new aciML_EventCommand;
                #                curMode = AML_INIT_EVENT_COMMAND;
                #                self.writer.mode(curMode);
                #                break;
            #            case NEW_ML_EVENT:
            elif section == Section.NEW_ML_EVENT:
                self.writer.assert_mode(Mode.AML_INIT_DATA)
                self.writer.set_mode(Mode.AML_INIT_EVENT)
                # //                if(curMode != AML_INIT_DATA)
                # //                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                mlEv = new aciML_Event;
                #                curMode = AML_INIT_EVENT;
                #                self.writer.mode(curMode);
                #                break;
            #            case NEW_ML_DATA:
            elif section == Section.NEW_ML_DATA:
                self.writer.assert_mode(Mode.AML_INIT_DATA_SET)
                self.writer.set_mode(Mode.AML_INIT_DATA)
                # //                if(curMode != AML_INIT_DATA_SET)
                # //                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                mlData = new aciML_Data;
                #                curMode = AML_INIT_DATA;
                #                self.writer.mode(curMode);
                #                break;
            #            case NEW_ML_EVENT_SEQ:
            elif section == Section.NEW_ML_EVENT_SEQ:
                self.writer.assert_mode(Mode.AML_INIT_DATA_SET)
                
                self.writer.int(name='id')
                self.mlEvSeqSize = self.writer.int(name='size')
                self.writer.set_mode(Mode.AML_INIT_EVENT_SEQ)
                # //                if(curMode != AML_INIT_DATA_SET)
                # //                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                mlEvSeq = new aciML_EventSeq;
                # //                mlEvSeq -> ID = script -> read_idata();
                #                self.writer.intValue("mlEvSeq.ID");
                # //                mlEvSeq -> size = script -> read_idata();
                #                self.mlEvSeqSize = self.writer.intValue("mlEvSeq.size");
                # //                mlEvSeq -> alloc_mem(mlEvSeq -> size);
                #                curMode = AML_INIT_EVENT_SEQ;
                #                self.writer.mode(curMode);
                #                break;
            #            case NEW_BITMAP_MENU:
            elif section == Section.NEW_BITMAP_MENU:
                self.writer.assert_mode(Mode.AS_NONE)
                self.writer.set_mode(Mode.BM_INIT_MENU)
                # //                if(curMode != AS_NONE)
                # //                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                aciBM = new aciBitmapMenu;
                #                curMode = BM_INIT_MENU;
                #                self.writer.mode(curMode);
                #                break;
            #            case NEW_BITMAP_MENU_ITEM:
            elif section == Section.NEW_BITMAP_MENU_ITEM:
                self.writer.assert_mode(Mode.BM_INIT_MENU)
                self.writer.set_mode(Mode.BM_INIT_MENU_ITEM)
                # //                if(curMode != BM_INIT_MENU)
                # //                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                aciBM_it = new aciBitmapMenuItem;
                #                curMode = BM_INIT_MENU_ITEM;
                #                self.writer.mode(curMode);
                #                break;
            #            case NEW_ML_DATA_SET:
            elif section == Section.NEW_ML_DATA_SET:
                self.writer.assert_mode(Mode.AS_NONE)
                self.writer.set_mode(Mode.AML_INIT_DATA_SET)
                # //                if(curMode != AS_NONE)
                # //                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                mlDataSet = new aciML_DataSet;
                #                curMode = AML_INIT_DATA_SET;
                #                self.writer.mode(curMode);
                #                break;
            #            case NEW_ML_ITEM_DATA:
            elif section == Section.NEW_ML_ITEM_DATA:
                self.writer.assert_mode(Mode.AML_INIT_DATA_SET)
                self.writer.composite(
                    ('ItemID', 'int32'),
                    ('NullLevel', 'int32'),
                    ('frameName', 'str'),
                )
                # //                if(curMode != AML_INIT_DATA_SET)
                # //                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                mlItm = new aciML_ItemData;
                # //
                # //                mlItm -> ItemID = script -> read_idata();
                #                self.writer.intValue("mlItm.ItemID");
                # //                mlItm -> NullLevel = script -> read_idata();
                #                self.writer.intValue("mlItm.NullLevel");
                # //                script -> read_pdata(&mlItm -> frameName,1);
                #                self.writer.strValue("mlItm.frameName");
                # //                mlDataSet -> add_item(mlItm);
                #                break;
            #            case INIT_ML_EVENT_KEY_CODE:
            elif section == Section.INIT_ML_EVENT_KEY_CODE:
                self.writer.assert_mode(Mode.AML_INIT_EVENT)
                self.writer.int(name="mvEv.keys.addKey")
                #                if(curMode == AML_INIT_EVENT){
                #                    self.writer.intValue("mvEv.keys.addKey", "mlEv -> keys -> add_key(script -> read_idata());");
                # //                    mlEv -> keys -> add_key(script -> read_idata());
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_RND_VALUE:
            elif section == Section.SET_RND_VALUE:
                self.writer.assert_mode(Mode.AML_INIT_EVENT)
                self.writer.int(name="mvEv.rndValue")
                #                if(curMode == AML_INIT_EVENT){
                # //                    mlEv -> rndValue = script -> read_idata();
                #                    self.writer.intValue("mvEv.rndValue", "mlEv -> rndValue = script -> read_idata();");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_SPEECH_CHANNEL:
            elif section == Section.SET_SPEECH_CHANNEL:
                self.writer.assert_mode(Mode.AML_INIT_DATA_SET)
                self.writer.int()
                #                if(curMode == AML_INIT_DATA_SET){
                # //                    mlDataSet -> SpeechChannel = script -> read_idata();
                #                    self.writer.intValue("mlDataSet.SpeechChannel");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_FRAME_CHECK_FLAG:
            elif section == Section.SET_FRAME_CHECK_FLAG:
                self.writer.assert_mode(Mode.AML_INIT_DATA)
                self.writer.flag('AML_FRAME_CHECK')
                #                if(curMode == AML_INIT_DATA){
                # //                    mlData -> flags |= AML_FRAME_CHECK;
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_SPEECH_LEVEL:
            elif section == Section.SET_SPEECH_LEVEL:
                self.writer.assert_mode(Mode.AML_INIT_DATA_SET)
                self.writer.comment("mlDataSet -> SpeechPriority[t_id] = script -> read_idata()")
                self.writer.composite(
                    ('t_id', 'int32'),
                    ('speech_level', 'int32'),
                )
                #                if(curMode == AML_INIT_DATA_SET){
                # //                    t_id = script -> read_idata();
                #                    self.writer.intValue("t_id");
                # //                    mlDataSet -> SpeechPriority[t_id] = script -> read_idata();
                #                    self.writer.intValue("mlDataSet.SpeechPriority.t_id", "mlDataSet -> SpeechPriority[t_id] = script -> read_idata()");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_ML_EVENT_SEQUENCE:
            elif section == Section.SET_ML_EVENT_SEQUENCE:
                self.writer.assert_mode(Mode.AML_INIT_EVENT, Mode.AML_INIT_EVENT_SEQ)
                if self.writer.has_mode(Mode.AML_INIT_EVENT):
                    self.writer.flag("AML_SEQUENCE_EVENT")
                elif self.writer.has_mode(Mode.AML_INIT_EVENT_SEQ):
                    self.writer.composite_array(
                        ('seq_id', 'int32'),
                        ('seq_mode', 'int32'),
                        length=self.mlEvSeqSize
                    )
                #                if(curMode == AML_INIT_EVENT){
                # //                    mlEv -> flags |= AML_SEQUENCE_EVENT;
                #                }
                #                else {
                #                    if(curMode == AML_INIT_EVENT_SEQ){
                #                        char buf[256];
                #                        for(t_id = 0; t_id < mlEvSeqSize; t_id ++){
                # //                            mlEvSeq -> SeqIDs[t_id] = script -> read_idata();
                #                            sprintf(buf, "mlEvSeq.SeqIDs[%d]", t_id);
                #                            self.writer.intValue(buf);
                # //                            mlEvSeq -> SeqModes[t_id] = script -> read_idata();
                #                            sprintf(buf, "mlEvSeq.SeqModes[%d]", t_id);
                #                            self.writer.intValue(buf);
                #
                #                        }
                #                    }
                #                    else
                #                        _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_ML_EVENT_CODE:
            elif section == Section.INIT_ML_EVENT_CODE:
                self.writer.assert_mode(Mode.AML_INIT_EVENT_COMMAND)
                self.writer.composite(
                    ('code', 'int32'),
                    ('data1', 'int32'),
                    ('data2', 'int32'),
                )
                #                if(curMode == AML_INIT_EVENT_COMMAND){
                # //                    mlEvComm -> code = script -> read_idata();
                #                    self.writer.intValue("mlEvComm.code");
                # //                    mlEvComm -> data0 = script -> read_idata();
                #                    self.writer.intValue("mlEvComm.data0");
                # //                    mlEvComm -> data1 = script -> read_idata();
                #                    self.writer.intValue("mlEvComm.data1");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_ML_EVENT_STARTUP:
            elif section == Section.INIT_ML_EVENT_STARTUP:
                self.writer.assert_mode(Mode.AML_INIT_EVENT)
                self.writer.int()
                #                if(curMode == AML_INIT_EVENT){
                # //                    mlEv -> startupType = script -> read_idata();
                #                    self.writer.intValue("mlEv.startupType");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_PRIORITY:
            elif section == Section.SET_PRIORITY:
                self.writer.assert_mode(Mode.AML_INIT_EVENT, Mode.AML_INIT_EVENT_SEQ)
                self.writer.int()
                #                if(curMode == AML_INIT_EVENT){
                # //                    mlEv -> priority = script -> read_idata();
                #                    self.writer.intValue("mlEv.priority");
                #                }
                #                else {
                #                    if(curMode == AML_INIT_EVENT_SEQ){
                # //                        mlEvSeq -> dropLevel[0] = script -> read_idata();
                #                        self.writer.intValue("mlEvSeq.dropLevel[0]");
                #                    }
                #                    else
                #                        _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_NOT_LOCKED_FLAG:
            elif section == Section.SET_NOT_LOCKED_FLAG:
                self.writer.assert_mode(Mode.AML_INIT_EVENT)
                self.writer.flag('AML_IF_NOT_LOCKED')
                #                if(curMode == AML_INIT_EVENT){
                # //                    mlEv -> flags |= AML_IF_NOT_LOCKED;
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_LOCKED_FLAG:
            elif section == Section.SET_LOCKED_FLAG:
                self.writer.assert_mode(Mode.AML_INIT_EVENT)
                self.writer.flag('AML_IF_LOCKED')
                #                if(curMode == AML_INIT_EVENT){
                # //                    mlEv -> flags |= AML_IF_LOCKED;
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_START_TIMER:
            elif section == Section.INIT_START_TIMER:
                self.writer.assert_mode(Mode.AML_INIT_EVENT_COMMAND)
                self.writer.int()
                #                if(curMode == AML_INIT_EVENT_COMMAND){
                # //                    mlEvComm -> start_timer = script -> read_idata();
                #                    self.writer.intValue("mlEvComm.start_timer");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_CHANNEL_ID:
            elif section == Section.INIT_CHANNEL_ID:
                self.writer.assert_mode(
                    Mode.AML_INIT_EVENT,
                    Mode.AML_INIT_DATA,
                    Mode.AML_INIT_EVENT_SEQ,
                )
                self.writer.int()
                #                if(curMode == AML_INIT_EVENT){
                # //                    mlEv -> ChannelID = script -> read_idata();
                #                    self.writer.intValue("mlEv.ChannelID");
                #                }
                #                else {
                #                    if(curMode == AML_INIT_DATA){
                # //                        mlData -> ChannelID = script -> read_idata();
                #                        self.writer.intValue("mlData.ChannelID");
                #                    }
                #                    else {
                #                        if(curMode == AML_INIT_EVENT_SEQ){
                # //                            mlEvSeq -> ChannelID = script -> read_idata();
                #                            self.writer.intValue("mlEvSeq.ChannelID");
                #                        }
                #                        else
                #                            _handle_error("Misplaced option",aOptIDs[id]);
                #                    }
                #                }
                #                break;
            #            case INIT_ML_EVENT_SDATA:
            elif section == Section.INIT_ML_EVENT_SDATA:
                self.writer.assert_mode(Mode.AML_INIT_EVENT)
                self.writer.int()
                #                if(curMode == AML_INIT_EVENT){
                # //                    mlEv -> data = script -> read_idata();
                #                    self.writer.intValue("mlEv.data");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_OFFS_X:
            elif section == Section.INIT_OFFS_X:
                self.writer.assert_mode(
                    Mode.AS_INIT_WORLD_MAP,
                    Mode.AS_INIT_IBS,
                )
                self.writer.composite(
                    ('id', 'int32'),
                    ('OffsX', 'int32'),
                )
                #                if(curMode == AS_INIT_WORLD_MAP){
                # //                    t_id = script -> read_idata();
                #                    self.writer.intValue("t_id");
                # //                    wMap -> ShapeOffsX[t_id] = script -> read_idata();
                #                    self.writer.intValue("wMap.ShapeOffsX[$t_id]", "wMap -> ShapeOffsX[t_id]");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_IBS){
                # //                        t_id = script -> read_idata();
                #                        self.writer.intValue("t_id");
                # //                        ibsObj -> indPosX[t_id] = script -> read_idata();
                #                        self.writer.intValue("ibsObj.indPosX[$t_id]", "ibsObj -> indPosX[t_id] = script -> read_idata()");
                #                    }
                #                    else
                #                        _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_WORLD_NAME:
            elif section == Section.SET_WORLD_NAME:
                self.writer.assert_mode(
                    Mode.AS_INIT_WORLD_DATA,
                    Mode.AML_INIT_DATA,
                    Mode.AS_INIT_LOC_DATA,
                    Mode.AS_INIT_SHUTTER,
                )
                if self.writer.has_mode(Mode.AS_INIT_WORLD_DATA):
                    self.writer.str()
                elif self.writer.has_mode(Mode.AML_INIT_DATA):
                    self.writer.str()
                elif self.writer.has_mode(Mode.AS_INIT_LOC_DATA):
                    self.writer.composite(
                        ('nameId', 'str'),
                        ('nameId2', 'str'),
                    )
                elif self.writer.has_mode(Mode.AS_INIT_SHUTTER):
                    self.writer.str()
                #                if(curMode == AS_INIT_WORLD_DATA){
                # //                    script -> read_pdata(&wData -> name,1);
                #                    self.writer.strValue("wData.name");
                #                }
                #                else {
                #                    if(curMode == AML_INIT_DATA){
                # //                        script -> read_pdata(&mlData -> name,1);
                #                        self.writer.strValue("mlData.name");
                #                    }
                #                    else {
                #                        if(curMode == AS_INIT_LOC_DATA){
                # //                            script -> read_pdata(&locData -> nameID,1);
                # //                            script -> read_pdata(&locData -> nameID2,1);
                #                            self.writer.strValue("locData.nameID");
                #                            self.writer.strValue("locData.nameID2");
                #                        }
                #                        else {
                #                            if(curMode == AS_INIT_SHUTTER){
                # //                                script -> read_pdata(&locSh -> name,1);
                #                                self.writer.strValue("locSh.name");
                #                            }
                #                            else
                #                                _handle_error("Misplaced option",aOptIDs[id]);
                #                        }
                #                    }
                #                }
                #                break;
            #            case ADD_FLAG:
            elif section == Section.ADD_FLAG:
                self.writer.assert_mode(Mode.AS_INIT_WORLD_DATA)
                self.writer.int(comment="wData -> flags |= t_id;")
                #                if(curMode == AS_INIT_WORLD_DATA){
                # //                    t_id = script -> read_idata();
                #                    self.writer.intValue("t_id", "wData -> flags |= t_id;");
                # //                    wData -> flags |= t_id;
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case ADD_LINK:
            elif section == Section.ADD_LINK:
                self.writer.assert_mode(Mode.AS_INIT_WORLD_DATA)
                self.writer.int()
                #                if(curMode == AS_INIT_WORLD_DATA){
                #                    self.writer.intValue("t_id", " wData -> links[${t_id}] = 1");
                # //                    t_id = script -> read_idata();
                # //                    wData -> links[t_id] = 1;
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_MAX_STR:
            elif section == Section.SET_MAX_STR:
                self.writer.assert_mode(Mode.AS_INIT_INFO_PANEL)
                self.writer.int()
                #                if(curMode == AS_INIT_INFO_PANEL){
                # //                    iPl -> MaxStr = script -> read_idata();
                #                    self.writer.intValue("iPl.MaxStr");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_INFO_OFFS_X:
            elif section == Section.INIT_INFO_OFFS_X:
                self.writer.assert_mode(Mode.AS_INIT_INFO_PANEL)
                self.writer.int()
                #                if(curMode == AS_INIT_INFO_PANEL){
                # //                    iPl -> OffsX = script -> read_idata();
                #                    self.writer.intValue("iPl.OffsX");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_BACK_COL:
            elif section == Section.INIT_BACK_COL:
                self.writer.assert_mode(
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_MENU,
                )
                self.writer.int()
                #                if(curMode == AS_INIT_INFO_PANEL){
                # //                    iPl -> bCol = script -> read_idata();
                #                    self.writer.intValue("iPl.bCol");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_MENU){
                # //                        fnMnu -> bCol = script -> read_idata();
                #                        self.writer.intValue("fnMnu.bCol");
                #                    }
                #                    else
                #                        _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_RANGE_FLAG:
            elif section == Section.SET_RANGE_FLAG:
                self.writer.assert_mode(
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_COUNTER,
                )
                if self.writer.has_mode(Mode.AS_INIT_INFO_PANEL):
                    self.writer.flag("IP_RANGE_FONT")
                elif self.writer.has_mode(Mode.AS_INIT_MENU):
                    self.writer.flag("FM_RANGE_FONT")
                    self.fnMenuFlags |= FM_RANGE_FONT
                elif self.writer.has_mode(Mode.AS_INIT_COUNTER):
                    self.writer.flag("CP_RANGE_FONT")
                #                if(curMode == AS_INIT_INFO_PANEL){
                # //                    iPl -> flags |= IP_RANGE_FONT;
                #                }
                #                else {
                #                    if(curMode == AS_INIT_MENU){
                # //                        fnMnu -> flags |= FM_RANGE_FONT;
                #                        self.fnMenuFlags |= FM_RANGE_FONT;
                #                    }
                #                    else {
                #                        if(curMode == AS_INIT_COUNTER){
                # //                            cP -> flags |= CP_RANGE_FONT;
                #                        }
                #                        else
                #                            _handle_error("Misplaced option",aOptIDs[id]);
                #                    }
                #                }
                #                break;
            #            case SET_SUBMENU_FLAG:
            elif section == Section.SET_SUBMENU_FLAG:
                self.writer.assert_mode(Mode.AS_INIT_MENU)
                self.writer.flag("FM_SUBMENU")
                self.fnMenuFlags |= FM_SUBMENU
                #                if(curMode == AS_INIT_MENU){
                # //                    fnMnu -> flags |= FM_SUBMENU;
                #                    self.fnMenuFlags |= FM_SUBMENU;
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_MAINMENU_FLAG:
            elif section == Section.SET_MAINMENU_FLAG:
                self.writer.assert_mode(Mode.AS_INIT_MENU)
                self.writer.flag("FM_MAIN_MENU")
                self.fnMenuFlags |= FM_MAIN_MENU
                #                if(curMode == AS_INIT_MENU){
                # //                    fnMnu -> flags |= FM_MAIN_MENU;
                #                    self.fnMenuFlags |= FM_MAIN_MENU;
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_INFO_OFFS_Y:
            elif section == Section.INIT_INFO_OFFS_Y:
                self.writer.assert_mode(Mode.AS_INIT_INFO_PANEL)
                self.writer.int()
                #                if(curMode == AS_INIT_INFO_PANEL){
                # //                    iPl -> OffsY = script -> read_idata();
                #                    self.writer.intValue("iPl.OffsY");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_NO_ALIGN:
            elif section == Section.SET_NO_ALIGN:
                self.writer.assert_mode(Mode.AS_INIT_INFO_PANEL)
                self.writer.flag("IP_NO_ALIGN")
                #                if(curMode == AS_INIT_INFO_PANEL){
                # //                    iPl -> flags |= IP_NO_ALIGN;
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_OFFS_Y:
            elif section == Section.INIT_OFFS_Y:
                self.writer.assert_mode(
                    Mode.AS_INIT_WORLD_MAP,
                    Mode.AS_INIT_IBS,
                )
                if self.writer.has_mode(Mode.AS_INIT_WORLD_MAP):
                    self.writer.int(name='id')
                    self.writer.int(name='ShapeOffsY')
                elif self.writer.has_mode(Mode.AS_INIT_IBS):
                    self.writer.int(name='id')
                    self.writer.int(name='PosY')
                #                if(curMode == AS_INIT_WORLD_MAP){
                # //                    t_id = script -> read_idata();
                #                    self.writer.intValue("t_id");
                # //                    wMap -> ShapeOffsY[t_id] = script -> read_idata();
                #                    self.writer.intValue("wMap.ShapeOffsY[$t_id]", "wMap -> ShapeOffsY[t_id] = script -> read_idata()");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_IBS){
                # //                        t_id = script -> read_idata();
                #                        self.writer.intValue("t_id");
                # //                        ibsObj -> indPosY[t_id] = script -> read_idata();
                #                        self.writer.intValue("ibsObj.indPosY[$t_id]", "ibsObj -> indPosY[t_id]");
                #                    }
                #                    else
                #                        _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case NEW_WORLD_MAP:
            elif section == Section.NEW_WORLD_MAP:
                self.writer.assert_mode(
                    Mode.AS_NONE,
                )
                self.writer.set_mode(Mode.AS_INIT_WORLD_MAP)
                #                if(curMode != AS_NONE)
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #
                # //                wMap = new aciWorldMap;
                #                curMode = AS_INIT_WORLD_MAP;
                #                self.writer.mode(curMode);
                #                break;
            #            case NEW_WORLD_DATA:
            elif section == Section.NEW_WORLD_DATA:
                self.writer.assert_mode(
                    Mode.AS_INIT_WORLD_MAP,
                )
                
                self.writer.int(name='id')
                self.writer.int(name='letter')
                self.writer.int(name='shape_id')
                self.writer.set_mode(Mode.AS_INIT_WORLD_DATA)
                #                if(curMode != AS_INIT_WORLD_MAP)
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #
                # //                wData = new aciWorldInfo;
                # //                wData -> ID = script -> read_idata();
                #                self.writer.intValue("wData.ID");
                # //                wData -> letter = script -> read_idata();
                #                self.writer.intValue("wData.letter");
                # //                wData -> shape_id = script -> read_idata();
                #                self.writer.intValue("wData.shape_id");
                #                curMode = AS_INIT_WORLD_DATA;
                #                self.writer.mode(curMode);
                #                break;
            #            case TOGGLE_ISCREEN_MODE:
            elif section == Section.TOGGLE_ISCREEN_MODE:
                self.writer.flag("iScreenFlag")
                self.iScreenFlag = 1;
                #                break;
            #            case I_END_BLOCK:
            elif section == Section.I_END_BLOCK:
                self.writer.end_block(self.get_prev_mode())
                #                endBlock(self.writer);
                #                break;
            #            case INIT_CELL_SIZE:
            elif section == Section.INIT_CELL_SIZE:
                if self.iScreenFlag:
                    self.writer.int(name='iCellSize')
                else:
                    self.writer.int(name='aCellSize')
                #                if(self.iScreenFlag){
                # //                    iCellSize = script -> read_idata();
                #                    self.writer.intValue("iCellSize");
                #                }
                #                else{
                # //                    aCellSize = script -> read_idata();
                #                    self.writer.intValue("aCellSize");
                #                }
                #                break;
            #            case NEW_INV_MATRIX:
            elif section == Section.NEW_INV_MATRIX:
                self.writer.assert_mode(
                    Mode.AS_NONE,
                )
                
                self.writer.int(name='internalId')
                self.writer.int(name='type')
                self.writer.set_mode(Mode.AS_INIT_MATRIX)
                #                if(curMode != AS_NONE)
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                invMat = new invMatrix;
                #                curMode = AS_INIT_MATRIX;
                #
                # //                invMat -> internalID = script -> read_idata();
                #                self.writer.intValue("invMat.internalID");
                # //                invMat -> type = script -> read_idata();
                #                self.writer.intValue("invMat.type");
                #                break;
            #            case NEW_INFO_PANEL:
            elif section == Section.NEW_INFO_PANEL:
                self.writer.assert_mode(
                    Mode.AS_NONE,
                )
                self.writer.set_mode(Mode.AS_INIT_INFO_PANEL)
                #                if(curMode != AS_NONE)
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                iPl = new InfoPanel;
                #                curMode = AS_INIT_INFO_PANEL;
                #                self.writer.mode(curMode);
                #                break;
            #            case NEW_IBS:
            elif section == Section.NEW_IBS:
                self.writer.assert_mode(
                    Mode.AS_NONE,
                )
                
                self.writer.int(name='id')
                self.writer.set_mode(Mode.AS_INIT_IBS)
                #                if(curMode != AS_NONE)
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                ibsObj = new ibsObject;
                #                curMode = AS_INIT_IBS;
                #
                # //                ibsObj -> ID = script -> read_idata();
                #                self.writer.intValue("ibsObj.ID");
                #                break;
            #            case NEW_IND:
            elif section == Section.NEW_IND:
                self.writer.assert_mode(
                    Mode.AS_NONE,
                )
                
                self.writer.int(name='id')
                self.writer.set_mode(Mode.AS_INIT_IND)
                #                if(curMode != AS_NONE)
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                aInd = new aIndData;
                #                curMode = AS_INIT_IND;
                #
                # //                aInd -> ID = script -> read_idata();
                #                self.writer.intValue("aInd.ID");
                #                break;
            #            case NEW_BML:
            elif section == Section.NEW_BML:
                self.writer.assert_mode(
                    Mode.AS_NONE,
                )
                
                self.writer.flag("BMP_FLAG")
                self.writer.int(name='id')
                self.writer.set_mode(Mode.AS_INIT_BML)
                #                if(curMode != AS_NONE)
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                bmlObj = new bmlObject;
                # //                bmlObj -> flags |= BMP_FLAG;
                #                curMode = AS_INIT_BML;
                #
                # //                bmlObj -> ID = script -> read_idata();
                #                self.writer.intValue("bmlObj.ID");
                #                break;
            #            case NEW_INV_ITEM:
            elif section == Section.NEW_INV_ITEM:
                self.writer.assert_mode(
                    Mode.AS_NONE,
                )
                
                self.writer.str(name="name")
                self.writer.set_mode(Mode.AS_INIT_ITEM)
                #                if(curMode != AS_NONE)
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                invItm = new invItem;
                #                curMode = AS_INIT_ITEM;
                #                self.writer.strValue("invItm.init_name(", " invItm -> init_name(script -> get_conv_ptr())");
                # //                script -> prepare_pdata();
                # //                invItm -> init_name(script -> get_conv_ptr());
                #                break;
            #            case NEW_COUNTER:
            elif section == Section.NEW_COUNTER:
                self.writer.assert_mode(
                    Mode.AS_NONE,
                )
                
                self.writer.int(name="type")
                self.writer.set_mode(Mode.AS_INIT_COUNTER)
                #                if(curMode != AS_NONE)
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #
                # //                cP = new CounterPanel;
                # //                cP -> type = script -> read_option(0) - NEW_COUNTER - 1;
                #                self.writer.intValue("cP.type", "cP -> type = script -> read_option(0) - NEW_COUNTER - 1");
                #                curMode = AS_INIT_COUNTER;
                #                break;
            #            case NEW_BUTTON:
            elif section == Section.NEW_BUTTON:
                self.writer.assert_mode(
                    Mode.AS_NONE,
                )
                
                self.writer.int(name="type")
                self.writer.set_mode(Mode.AS_INIT_BUTTON)
                #                if(curMode != AS_NONE)
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                aBt = new aButton;
                #                self.writer.intValue("aBt.type", "aBt -> type = script -> read_option(0) - NEW_BUTTON - 1");
                # //                aBt -> type = script -> read_option(0) - NEW_BUTTON - 1;
                #
                #                curMode = AS_INIT_BUTTON;
                #                break;
            #            case NEW_MENU:
            elif section == Section.NEW_MENU:
                self.writer.assert_mode(
                    Mode.AS_NONE,
                    Mode.AS_INIT_ITEM,
                )
                self.fnMenuFlags = 0
                if self.writer.has_mode(Mode.AS_INIT_ITEM):
                    self.fnMenuFlags = FM_ITEM_MENU
                self.writer.set_mode(Mode.AS_INIT_MENU)
                #                if(curMode != AS_NONE && curMode != AS_INIT_ITEM)
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                fnMnu = new fncMenu;
                #                self.fnMenuFlags = 0;
                #                if(curMode == AS_INIT_ITEM){
                # //                    fnMnu -> flags |= FM_ITEM_MENU;
                #                    self.fnMenuFlags |= FM_ITEM_MENU;
                #                }
                #                curMode = AS_INIT_MENU;
                #                break;
            #            case NEW_MENU_ITEM:
            elif section == Section.NEW_MENU_ITEM:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.writer.set_mode(Mode.AS_INIT_MENU_ITEM)
                #                if(curMode != AS_INIT_MENU)
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                fnMnuItm = new fncMenuItem;
                #                curMode = AS_INIT_MENU_ITEM;
                #                break;
            #            case INIT_NUMVALS:
            elif section == Section.INIT_NUMVALS:
                self.writer.assert_mode(
                    Mode.AS_INIT_IND,
                )
                self.writer.int()
                #                if(curMode == AS_INIT_IND){
                #                    self.writer.intValue("aInd.NumVals");
                # //                    aInd -> NumVals = script -> read_idata();
                # //                    aInd -> alloc_mem();
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_X:
            elif section == Section.INIT_X:
                self.writer.assert_mode(
                    Mode.AS_INIT_MATRIX,
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_BUTTON,
                    Mode.AS_INIT_IND,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_COUNTER,
                    Mode.AS_INIT_WORLD_DATA,
                    Mode.BM_INIT_MENU_ITEM,
                )
                self.writer.int()
                #                if(curMode == AS_INIT_MATRIX){
                # //                    invMat -> ScreenX = script -> read_idata();
                #                    self.writer.intValue("invMat.ScreenX");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_MENU){
                # //                        fnMnu -> PosX = script -> read_idata();
                #                        self.writer.intValue("fnMnu.PosX");
                #                    }
                #                    else {
                #                        if(curMode == AS_INIT_BUTTON){
                # //                            aBt -> PosX = script -> read_idata();
                #                            self.writer.intValue("aBt.PosX");
                #                        }
                #                        else {
                #                            if(curMode == AS_INIT_IND){
                # //                                aInd -> PosX = script -> read_idata();
                # //                                aInd -> dX = aInd -> PosX;
                #                                self.writer.intValue("aInd.PosX", "aInd -> dX = aInd -> PosX;");
                #                            }
                #                            else {
                #                                if(curMode == AS_INIT_INFO_PANEL){
                # //                                    iPl -> PosX = script -> read_idata();
                #                                    self.writer.intValue("iPl.PosX");
                #                                }
                #                                else {
                #                                    if(curMode == AS_INIT_COUNTER){
                # //                                        cP -> PosX = script -> read_idata();
                #                                        self.writer.intValue("cP.PosX");
                #                                    }
                #                                    else {
                #                                        if(curMode == AS_INIT_WORLD_DATA){
                # //                                            wData -> PosX = script -> read_idata();
                #                                            self.writer.intValue("wData.PosX");
                #                                        }
                #                                        else {
                #                                            if(curMode == BM_INIT_MENU_ITEM){
                # //                                                aciBM_it -> PosX = script -> read_idata();
                #                                                self.writer.intValue("aciBM_it.PosX");
                #                                            }
                #                                            else
                #                                                _handle_error("Misplaced option",aOptIDs[id]);
                #                                        }
                #                                    }
                #                                }
                #                            }
                #                        }
                #                    }
                #                }
                #                break;
            #            case INIT_Y:
            elif section == Section.INIT_Y:
                self.writer.assert_mode(
                    Mode.AS_INIT_MATRIX,
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_BUTTON,
                    Mode.AS_INIT_IND,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_COUNTER,
                    Mode.AS_INIT_WORLD_DATA,
                    Mode.BM_INIT_MENU_ITEM,
                )
                self.writer.int()
                #                if(curMode == AS_INIT_MATRIX){
                # //                    invMat -> ScreenY = script -> read_idata();
                #                    self.writer.intValue("invMat.ScreenY");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_MENU){
                # //                        fnMnu -> PosY = script -> read_idata();
                #                        self.writer.intValue("fnMnu.PosY");
                #                    }
                #                    else {
                #                        if(curMode == AS_INIT_BUTTON){
                # //                            aBt -> PosY = script -> read_idata();
                #                            self.writer.intValue("aBt.PosY");
                #                        }
                #                        else {
                #                            if(curMode == AS_INIT_IND){
                # //                                aInd -> PosY = script -> read_idata();
                # //                                aInd -> dY = aInd -> PosY;
                #                                self.writer.intValue("aInd.PosY", "aInd -> dY = aInd -> PosY");
                #                            }
                #                            else {
                #                                if(curMode == AS_INIT_INFO_PANEL){
                # //                                    iPl -> PosY = script -> read_idata();
                #                                    self.writer.intValue("iPl.PosY");
                #                                }
                #                                else {
                #                                    if(curMode == AS_INIT_COUNTER){
                # //                                        cP -> PosY = script -> read_idata();
                #                                        self.writer.intValue("cP.PosY");
                #                                    }
                #                                    else {
                #                                        if(curMode == AS_INIT_WORLD_DATA){
                # //                                            wData -> PosY = script -> read_idata();
                #                                            self.writer.intValue("wData.PosY");
                #                                        }
                #                                        else {
                #                                            if(curMode == BM_INIT_MENU_ITEM){
                # //                                                aciBM_it -> PosY = script -> read_idata();
                #                                                self.writer.intValue("aciBM_it.PosY");
                #                                            }
                #                                            else
                #                                                _handle_error("Misplaced option",aOptIDs[id]);
                #                                        }
                #                                    }
                #                                }
                #                            }
                #                        }
                #                    }
                #                }
                #                break;
            #            case INIT_MSX:
            elif section == Section.INIT_MSX:
                self.writer.assert_mode(
                    Mode.AS_INIT_MATRIX,
                )
                self.invMatSizeX = self.writer.int()
                #                if(curMode == AS_INIT_MATRIX){
                # //                    invMat -> SizeX = script -> read_idata();
                #                    self.invMatSizeX =  self.writer.intValue("invMat.SizeX");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_RAFFA_FLAG:
            elif section == Section.SET_RAFFA_FLAG:
                self.writer.assert_mode(
                    Mode.AS_INIT_MATRIX,
                )
                self.writer.flag('IM_RAFFA')
                #                if(curMode == AS_INIT_MATRIX){
                # //                    invMat -> flags |= IM_RAFFA;
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_NUM_AVI_ID:
            elif section == Section.SET_NUM_AVI_ID:
                self.writer.assert_mode(
                    Mode.AS_INIT_MATRIX,
                    Mode.AS_INIT_ITEM,
                )
                self.writer.int()
                #                if(curMode == AS_INIT_MATRIX){
                # //                    invMat -> numAviIDs = script -> read_idata();
                #                    self.writer.intValue("nvMat.numAviIDs");
                # //                    if(!invMat -> numAviIDs) _handle_error("Bad invMatrix::numAviIDs");
                # //                    invMat -> avi_ids = new char*[invMat -> numAviIDs];
                # //                    for(i = 0; i < invMat -> numAviIDs; i ++)
                # //                        invMat -> avi_ids[i] = NULL;
                #                }
                #                else {
                #                    if(curMode == AS_INIT_ITEM){
                # //                        invItm -> numAviIDs = script -> read_idata();
                #                        self.writer.intValue("invItm.numAviIDs");
                # //                        if(!invItm -> numAviIDs) _handle_error("Bad invItem::numAviIDs");
                # //                        invItm -> avi_ids = new char*[invItm -> numAviIDs];
                # //                        for(i = 0; i < invItm -> numAviIDs; i ++)
                # //                            invItm -> avi_ids[i] = NULL;
                #                    }
                #                    else {
                #                        _handle_error("Misplaced option",aOptIDs[id]);
                #                    }
                #                }
            #                break;
            #            case SET_ESCAVE_FLAG:
            elif section == Section.SET_ESCAVE_FLAG:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.writer.flag('INV_ITEM_SHOW_ESCAVE')
                #                if(curMode == AS_INIT_ITEM){
                # //                    invItm -> flags |= INV_ITEM_SHOW_ESCAVE;
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_SHOW_LOAD:
            elif section == Section.SET_SHOW_LOAD:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.writer.flag('INV_ITEM_SHOW_ESCAVE')
                #                if(curMode == AS_INIT_ITEM){
                # //                    invItm -> flags |= INV_ITEM_SHOW_LOAD;
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_TEMPLATE:
            elif section == Section.SET_TEMPLATE:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.writer.str(name="template")
                #                if(curMode == AS_INIT_ITEM){
                # //                    script -> prepare_pdata();
                # //                    if(strcasecmp(script -> get_conv_ptr(),"NONE"))
                # //                        invItm -> set_template(script -> get_conv_ptr());
                #                    self.writer.strValue("invItm -> set_template(");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_ACTIVATE_FLAG:
            elif section == Section.SET_ACTIVATE_FLAG:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.writer.flag("INV_ITEM_NO_ACTIVATE")
                #                if(curMode == AS_INIT_ITEM){
                # //                    invItm -> flags |= INV_ITEM_NO_ACTIVATE;
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_PART_DATA:
            elif section == Section.INIT_PART_DATA:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.writer.int(name="baseID[0]")
                self.writer.int(name="targetID[0]")
                self.writer.int(name="baseID[1]")
                self.writer.int(name="targetID[1]")
                #                if(curMode == AS_INIT_ITEM){
                # //                    invItm -> partData = new aciMechosPartInfo;
                # //                    invItm -> partData -> baseID[0] = script -> read_idata();
                #                    self.writer.intValue("invItm.partData.baseID[0]");
                # //                    invItm -> partData -> targetID[0] = script -> read_idata();
                #                    self.writer.intValue("invItm.partData.targetID[0]");
                # //                    invItm -> partData -> baseID[1] = script -> read_idata();
                #                    self.writer.intValue("invItm.partData.baseID[1]");
                # //                    invItm -> partData -> targetID[1] = script -> read_idata();
                #                    self.writer.intValue("invItm.partData.targetID[1]");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_NO_SHOW_LOAD:
            elif section == Section.SET_NO_SHOW_LOAD:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.writer.flag("&= ~INV_ITEM_SHOW_LOAD")
                #                if(curMode == AS_INIT_ITEM){
                # //                    invItm -> flags &= ~INV_ITEM_SHOW_LOAD;
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_NOT_COMPLETED_FLAG:
            elif section == Section.SET_NOT_COMPLETED_FLAG:
                self.writer.assert_mode(
                    Mode.AS_INIT_MATRIX,
                )
                self.writer.flag("IM_NOT_COMPLETE")
                #                if(curMode == AS_INIT_MATRIX){
                # //                    invMat -> flags |= IM_NOT_COMPLETE;
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_MSY:
            elif section == Section.INIT_MSY:
                self.writer.assert_mode(
                    Mode.AS_INIT_MATRIX,
                )
                self.invMatSizeY = self.writer.int(name="SizeY")
                #                if(curMode == AS_INIT_MATRIX){
                # //                    invMat -> SizeY = script -> read_idata();
                #                    self.invMatSizeY =self.writer.intValue("invMat.SizeY");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_RADIUS:
            elif section == Section.INIT_RADIUS:
                self.writer.assert_mode(
                    Mode.AS_INIT_IND,
                )
                self.writer.int(name="__no_key__")
                #                if(curMode == AS_INIT_IND){
                # //                    script -> read_idata();
                #                    self.writer.intValue("__no_key__");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_CORNER:
            elif section == Section.INIT_CORNER:
                self.writer.assert_mode(
                    Mode.AS_INIT_IND,
                )
                self.writer.int(name="CornerNum")
                #                if(curMode == AS_INIT_IND){
                # //                    aInd -> CornerNum = script -> read_idata();
                #                    self.writer.intValue("aInd.CornerNum");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_IND_TYPE:
            elif section == Section.INIT_IND_TYPE:
                self.writer.assert_mode(
                    Mode.AS_INIT_IND,
                )
                self.writer.int(name="type")
                #                if(curMode == AS_INIT_IND){
                # //                    aInd -> type = script -> read_idata();
                #                    self.writer.intValue("aInd.type");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_SX:
            elif section == Section.INIT_SX:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM,
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_BML,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_WORLD_MAP,
                    Mode.AS_INIT_COUNTER,
                    Mode.BM_INIT_MENU
                )
                self.writer.int(name="SizeX")
                #                if(curMode == AS_INIT_MATRIX){
                # //                    invMat -> ScreenSizeX = script -> read_idata();
                #                    self.writer.intValue("invMat.ScreenSizeX");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_ITEM){
                # //                        t_id = script -> read_idata();
                #                        self.writer.intValue("t_id", " lpenguin: unused?");
                #                    }
                #                    else {
                #                        if(curMode == AS_INIT_MENU){
                # //                            fnMnu -> SizeX = script -> read_idata();
                #                            self.writer.intValue("fnMnu.SizeX");
                #                        }
                #                        else {
                #                            if(curMode == AS_INIT_BML){
                # //                                bmlObj -> SizeX = script -> read_idata();
                #                                self.writer.intValue("bmlObj.SizeX");
                #                            }
                #                            else {
                #                                if(curMode == AS_INIT_INFO_PANEL){
                # //                                    iPl -> SizeX = script -> read_idata();
                #                                    self.writer.intValue("iPl.SizeX");
                #                                }
                #                                else {
                #                                    if(curMode == AS_INIT_WORLD_MAP){
                # //                                        wMap -> SizeX = script -> read_idata();
                #                                        self.writer.intValue("wMap.SizeX");
                #                                    }
                #                                    else {
                #                                        if(curMode == AS_INIT_COUNTER){
                # //                                            cP -> SizeX = script -> read_idata();
                #                                            self.writer.intValue("cP.SizeX");
                #                                        }
                #                                        else {
                #                                            if(curMode == BM_INIT_MENU){
                # //                                                aciBM -> SizeX = script -> read_idata();
                #                                                self.writer.intValue("aciBM.SizeX");
                #                                            }
                #                                            else
                #                                                _handle_error("Misplaced option",aOptIDs[id]);
                #                                        }
                #                                    }
                #                                }
                #                            }
                #                        }
                #                    }
                #                }
                #                break;
            #            case INIT_SY:
            elif section == Section.INIT_SY:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM,
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_BML,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_WORLD_MAP,
                    Mode.AS_INIT_COUNTER,
                    Mode.BM_INIT_MENU
                )
                self.writer.int(name="SizeY")
                #                if(curMode == AS_INIT_MATRIX){
                # //                    invMat -> ScreenSizeY = script -> read_idata();
                #                    self.writer.intValue("invMat.ScreenSizeY");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_ITEM){
                # //                        t_id = script -> read_idata();
                #                        self.writer.intValue("t_id", " lpenguin: unused?");
                #                    }
                #                    else {
                #                        if(curMode == AS_INIT_MENU){
                # //                            fnMnu -> SizeY = script -> read_idata();
                #                            self.writer.intValue("fnMnu.SizeX");
                #                        }
                #                        else {
                #                            if(curMode == AS_INIT_BML){
                # //                                bmlObj -> SizeY = script -> read_idata();
                #                                self.writer.intValue("bmlObj.SizeX");
                #                            }
                #                            else {
                #                                if(curMode == AS_INIT_INFO_PANEL){
                # //                                    iPl -> SizeY = script -> read_idata();
                #                                    self.writer.intValue("iPl.SizeX");
                #                                }
                #                                else {
                #                                    if(curMode == AS_INIT_WORLD_MAP){
                # //                                        wMap -> SizeY = script -> read_idata();
                #                                        self.writer.intValue("wMap.SizeX");
                #                                    }
                #                                    else {
                #                                        if(curMode == AS_INIT_COUNTER){
                # //                                            cP -> SizeY = script -> read_idata();
                #                                            self.writer.intValue("cP.SizeX");
                #                                        }
                #                                        else {
                #                                            if(curMode == BM_INIT_MENU){
                # //                                                aciBM -> SizeY = script -> read_idata();
                #                                                self.writer.intValue("aciBM.SizeX");
                #                                            }
                #                                            else
                #                                                _handle_error("Misplaced option",aOptIDs[id]);
                #                                        }
                #                                    }
                #                                }
                #                            }
                #                        }
                #                    }
                #                }
                #                break;
            #            case INIT_SLOT_TYPE:
            elif section == Section.INIT_SLOT_TYPE:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.writer.int(name="slotType")
                #                if(curMode == AS_INIT_ITEM){
                # //                    invItm -> slotType = script -> read_idata();
                #                    self.writer.intValue("invItm.slotType");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_AVI_ID:
            elif section == Section.INIT_AVI_ID:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM,
                    Mode.AS_INIT_MATRIX,
                )
                self.writer.int(name="t_id")
                self.writer.str(name="str_id")
                #                if(curMode == AS_INIT_ITEM){
                # //                    if(!invItm -> numAviIDs) _handle_error("Null item numAviIDs...");
                # //                    t_id = script -> read_idata();
                #                    self.writer.intValue("t_id");
                # //                    if(t_id >= invItm -> numAviIDs || invItm -> avi_ids[t_id])
                # //                        _handle_error("Bad AVI_ID number");
                # //                    script -> prepare_pdata();
                # //                    invItm -> init_avi_id(script -> get_pdata_ptr(),t_id);
                #                    self.writer.strValue("invItm.init_avi_id(${data}, ${id})", "invItm -> init_avi_id(script -> get_pdata_ptr(),t_id);");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_MATRIX){
                # //                        if(!invMat -> numAviIDs) _handle_error("Null matrix numAviIDs...");
                # //                        t_id = script -> read_idata();
                #                        self.writer.intValue("t_id");
                # //                        if(t_id >= invMat -> numAviIDs || invMat -> avi_ids[t_id])
                # //                            _handle_error("Bad AVI_ID number");
                # //                        script -> prepare_pdata();
                # //                        invMat -> init_avi_id(script -> get_pdata_ptr(),t_id);
                #                        self.writer.strValue("invMat.init_avi_id(${data}, ${id})", "invMat -> init_avi_id(script -> get_pdata_ptr(),t_id);");
                #                    }
                #                    else {
                #                        _handle_error("Misplaced option",aOptIDs[id]);
                #                    }
                #                }
                #                break;
            #            case INIT_COMMENTS:
            elif section == Section.INIT_COMMENTS:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.writer.composite_array(
                    ('comment', 'str')
                )
                
                #                if(curMode == AS_INIT_ITEM){
                # //                    invItm -> numComments = script -> read_idata();
                #                    int n = self.writer.intValue("invItm.numComments");
                # //                    if(invItm -> numComments){
                #                    if(n){
                # //                        invItm -> comments = new char*[invItm -> numComments];
                # //                        for(i = 0; i < invItm -> numComments; i ++){
                # //                            script -> read_pdata(&invItm -> comments[i],1);
                # //                        }
                #                        for(i = 0; i < n; i++){
                #                            self.writer.strValue("invItm->comments[i]", "script -> read_pdata(&invItm -> comments[i],1);");
                #                        }
                #                    }
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_NUM_INDEX:
            elif section == Section.INIT_NUM_INDEX:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM,
                    Mode.AS_INIT_LOC_DATA,
                )
                if self.writer.has_mode(Mode.AS_INIT_ITEM):
                    self.writer.int('NumIndex')
                elif self.writer.has_mode(Mode.AS_INIT_LOC_DATA):
                    self.writer.int('i')
                    self.writer.int('numIndex')
                #                if(curMode == AS_INIT_ITEM){
                # //                    invItm -> NumIndex = script -> read_idata();
                #                    self.writer.intValue("invItm.NumIndex");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_LOC_DATA){
                # //                        t_id = script -> read_idata();
                #                        self.writer.intValue("t_id");
                # //                        if(t_id < 0 || t_id >= ACI_LOCATION_INDEX_SIZE)
                # //                            ErrH.Abort("Bad aciLocationInfo::numIndex ID...");
                # //                        locData -> numIndex[t_id] = script -> read_idata();
                #                        self.writer.intValue("locData.numIndex[$t_id]");
                #                    }
                #                    else
                #                        _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_SHAPE_LEN:
            elif section == Section.INIT_SHAPE_LEN:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM,
                )
                self.invItmShapeLen = self.writer.int('ShapeLen')
                #                if(curMode == AS_INIT_ITEM){
                # //                    invItm -> ShapeLen = script -> read_idata();
                #                    self.invItmShapeLen = self.writer.intValue("invItm.ShapeLen");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_SHAPE:
            elif section == Section.INIT_SHAPE:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM,
                    Mode.AS_INIT_WORLD_MAP,
                )
                if self.writer.has_mode(Mode.AS_INIT_ITEM):
                    
                    self.writer.composite_array(
                        ('ShapeX', 'int32'),
                        ('ShapeY', 'int32'),
                        length=self.invItmShapeLen
                    )
                    self.writer.set_mode(Mode.AS_INIT_SHAPE_OFFS)

                elif self.writer.has_mode(Mode.AS_INIT_WORLD_MAP):
                    self.writer.int('t_id')
                    self.writer.str('shape_files[t_id]')
                #                if(curMode == AS_INIT_ITEM){
                #                    curMode = AS_INIT_SHAPE_OFFS;
                #                    load_item_shape(self.invItmShapeLen, self.writer);
                #                }
                #                else {
                #                    if(curMode == AS_INIT_WORLD_MAP){
                # //                        t_id = script -> read_idata();
                #                        self.writer.intValue("t_id");
                # //                        script -> read_pdata(&wMap -> shape_files[t_id],1);
                #                        self.writer.strValue("wMap.shape_files[${t_id}]");
                #                    }
                #                    else
                #                        _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_MATRIX_EL:
            elif section == Section.INIT_MATRIX_EL:
                self.writer.assert_mode(
                    Mode.AS_INIT_MATRIX
                )
                
                self.writer.composite_array(
                    ('matrix[index].type', 'int32'),
                    length=self.invMatSizeX * self.invMatSizeY
                )
                self.writer.set_mode(Mode.AS_INIT_MATRIX_EL)
                #                if(curMode == AS_INIT_MATRIX){
                #                    curMode = AS_INIT_MATRIX_EL;
                #                    load_matrix(self.invMatSizeX, self.invMatSizeY, self.writer);
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_SLOT_NUMS:
            elif section == Section.INIT_SLOT_NUMS:
                self.writer.assert_mode(
                    Mode.AS_INIT_MATRIX
                )
                
                self.writer.composite_array(
                    ('matrix[index].slotNumber', 'int32'),
                    length=self.invMatSizeX * self.invMatSizeY
                )
                self.writer.set_mode(Mode.AS_INIT_MATRIX_EL)
                #                if(curMode == AS_INIT_MATRIX){
                #                    curMode = AS_INIT_MATRIX_EL;
                #                    load_slot_nums(self.invMatSizeX, self.invMatSizeY, self.writer);
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_SLOT_TYPES:
            elif section == Section.INIT_SLOT_TYPES:
                self.writer.assert_mode(
                    Mode.AS_INIT_MATRIX
                )
                
                self.writer.composite_array(
                    ('matrix[index].slotType', 'int32'),
                    length=self.invMatSizeX * self.invMatSizeY
                )
                self.writer.set_mode(Mode.AS_INIT_MATRIX_EL)
                #                if(curMode == AS_INIT_MATRIX){
                #                    curMode = AS_INIT_MATRIX_EL;
                #                    load_slot_types(self.invMatSizeX, self.invMatSizeY, self.writer);
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_CLASS:
            elif section == Section.INIT_CLASS:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM
                )
                self.writer.int(name="classId")
                #                if(curMode == AS_INIT_ITEM){
                # //                    t_id = script -> read_option(0) - INIT_CLASS - 1;
                # //                    invItm -> classID = t_id;
                #                    self.writer.intValue("invItm.classID", "invItm -> classID script -> read_option(0) - INIT_CLASS - 1");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_FNAME:
            elif section == Section.INIT_FNAME:
                self.writer.assert_mode(
                    Mode.AS_INIT_ITEM
                )
                self.writer.str(name="fname")
                #                if(curMode == AS_INIT_ITEM){
                # //                    script -> prepare_pdata();
                # //                    invItm -> init_fname(script -> get_conv_ptr());
                #                    self.writer.strValue("invItm.init_fname(");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_FILE:
            elif section == Section.INIT_FILE:
                self.writer.assert_mode(
                    Mode.AS_INIT_IBS,
                    Mode.AS_INIT_BML,
                )
                self.writer.str(name="name")
                # //                script -> prepare_pdata();
                #                if(curMode == AS_INIT_IBS){
                # //                    ibsObj -> set_name(script -> get_conv_ptr());
                #                    self.writer.strValue("bsObj.set_name(");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_BML){
                # //                        bmlObj -> init_name(script -> get_conv_ptr());
                #                        self.writer.strValue("bmlObj.init_name(");
                #                    }
                #                    else
                #                        _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_BGROUND:
            elif section == Section.INIT_BGROUND:
                self.writer.assert_mode(
                    Mode.AS_INIT_IBS,
                )
                self.writer.int(name="backObjID")
                #                if(curMode == AS_INIT_IBS){
                # //                    ibsObj -> backObjID = script -> read_idata();
                #                    self.writer.intValue("ibsObj.backObjID");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_SEQ_NAME:
            elif section == Section.INIT_SEQ_NAME:
                self.writer.assert_mode(
                    Mode.AS_INIT_BUTTON,
                )
                self.writer.str(name="fname")
                # //                script -> prepare_pdata();
                #                if(curMode == AS_INIT_BUTTON){
                # //                    aBt -> set_fname(script -> get_conv_ptr());
                #                    self.writer.strValue("aBt.set_fname(");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_CONTROL_ID:
            elif section == Section.SET_CONTROL_ID:
                self.writer.assert_mode(
                    Mode.AS_INIT_BUTTON,
                )
                self.writer.int(name="ControlID")
                #                if(curMode == AS_INIT_BUTTON){
                # //                    aBt -> ControlID = script -> read_idata();
                #                    self.writer.intValue("aBt.ControlID");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_EVENT_CODE:
            elif section == Section.INIT_EVENT_CODE:
                self.writer.assert_mode(
                    Mode.AS_INIT_BUTTON,
                    Mode.AS_INIT_ITEM,
                    Mode.AS_INIT_MENU_ITEM,
                )
                if self.writer.has_mode(Mode.AS_INIT_BUTTON):
                    self.writer.int(name="code")
                    self.writer.int(name="data");
                elif self.writer.has_mode(Mode.AS_INIT_ITEM):
                    self.writer.int(name='code')
                elif self.writer.has_mode(Mode.AS_INIT_MENU_ITEM):
                    self.writer.int(name='code')
                    self.writer.int(name="data")
                #                if(curMode == AS_INIT_BUTTON){
                # //                    t_id = script -> read_idata();
                #                    self.writer.intValue("t_id");
                # //                    init_event_code(t_id);
                # //                    void init_event_code(int cd)
                # //                    {
                # //                        aBt -> eventCode = cd + ACI_MAX_EVENT;
                # //                        aBt -> eventData = script -> read_idata();
                #                    self.writer.intValue("aBt.eventData");
                # //                    }
                #                }
                #                else {
                #                    if(curMode == AS_INIT_ITEM){
                # //                        invItm -> EvCode = script -> read_idata() + ACI_MAX_EVENT;
                #                        self.writer.intValue("invItm.EvCode", "invItm -> EvCode = script -> read_idata() + ACI_MAX_EVENT");
                #                    }
                #                    else {
                #                        if(curMode == AS_INIT_MENU_ITEM){
                # //                            fnMnuItm -> eventPtr = new actEvent;
                # //                            fnMnuItm -> eventPtr -> code = script -> read_idata() + ACI_MAX_EVENT;
                #                            self.writer.intValue("fnMnuItm.eventPtr.code", "fnMnuItm -> eventPtr -> code = script -> read_idata() + ACI_MAX_EVENT;");
                # //                            fnMnuItm -> eventPtr -> data = script -> read_idata();
                #                            self.writer.intValue("fnMnuItm.eventPtr.data");
                #                        }
                #                        else
                #                            _handle_error("Misplaced option",aOptIDs[id]);
                #                    }
                #                }
                #                break;
            #            case SET_UNPRESS:
            elif section == Section.SET_UNPRESS:
                self.writer.assert_mode(
                    Mode.AS_INIT_BUTTON,
                )
                self.writer.flag("B_UNPRESS")
                #                if(curMode == AS_INIT_BUTTON){
                # //                    aBt -> flags |= B_UNPRESS;
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_ACTIVE_TIME:
            elif section == Section.INIT_ACTIVE_TIME:
                self.writer.assert_mode(
                    Mode.AS_INIT_BUTTON,
                    Mode.AS_INIT_MENU,
                    Mode.AML_INIT_EVENT,
                    Mode.BM_INIT_MENU,
                )
                self.writer.int(name="activeCount")
                #                if(curMode == AS_INIT_BUTTON){
                # //                    aBt -> activeCount = script -> read_idata();
                #                    self.writer.intValue("aBt.activeCount");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_MENU){
                # //                        fnMnu -> activeCount = script -> read_idata();
                #                        self.writer.intValue("fnMnu.activeCount");
                #                    }
                #                    else {
                #                        if(curMode == AML_INIT_EVENT){
                # //                            mlEv -> active_time = script -> read_idata();
                #                            self.writer.intValue("mlEv.active_time");
                #                        }
                #                        else {
                #                            if(curMode == BM_INIT_MENU){
                # //                                aciBM -> activeCount = script -> read_idata();
                #                                self.writer.intValue("aciBM.activeCount");
                #                            }
                #                            else
                #                                _handle_error("Misplaced option",aOptIDs[id]);
                #                        }
                #                    }
                #                }
                #                break;
            #            case INIT_FNC_CODE:
            elif section == Section.INIT_FNC_CODE:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU_ITEM,
                )
                self.writer.int(name="fnc_code")
                #                if(curMode == AS_INIT_MENU_ITEM){
                # //                    fnMnuItm -> fnc_code = script -> read_idata();
                #                    self.writer.intValue("fnMnuItm.fnc_code");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_NO_DELETE_FLAG:
            elif section == Section.SET_NO_DELETE_FLAG:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU_ITEM,
                )
                self.writer.flag('FM_NO_DELETE')
                #                if(curMode == AS_INIT_MENU_ITEM){
                # //                    fnMnuItm -> flags |= FM_NO_DELETE;
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_SUBMENU_ID:
            elif section == Section.SET_SUBMENU_ID:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU_ITEM,
                )
                self.writer.int(name='submenuID')
                self.writer.flag('FM_SUBMENU_ITEM')
                #                if(curMode == AS_INIT_MENU_ITEM){
                # //                    fnMnuItm -> submenuID = script -> read_idata();
                #                    self.writer.intValue("fnMnuItm.submenuID");
                # //                    fnMnuItm -> flags |= FM_SUBMENU_ITEM;
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_BSUBMENU_ID:
            elif section == Section.SET_BSUBMENU_ID:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU_ITEM,
                )
                self.writer.int(name='submenuID')
                self.writer.flag('FM_BSUBMENU_ITEM')
                #                if(curMode == AS_INIT_MENU_ITEM){
                # //                    fnMnuItm -> submenuID = script -> read_idata();
                #                    self.writer.intValue("fnMnuItm.submenuID");
                # //                    fnMnuItm -> flags |= FM_BSUBMENU_ITEM;
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_NUM_V_ITEMS:
            elif section == Section.SET_NUM_V_ITEMS:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.writer.int(name='VItems')
                #                if(curMode == AS_INIT_MENU){
                # //                    fnMnu -> VItems = script -> read_idata();
                #                    self.writer.intValue("fnMnu.VItems");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_SPACE:
            elif section == Section.INIT_SPACE:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_MENU_ITEM,
                )
                self.writer.int(name='vSpace')
                #                if(curMode == AS_INIT_MENU){
                # //                    fnMnu -> vSpace = script -> read_idata();
                #                    self.writer.intValue("fnMnu.vSpace");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_MENU_ITEM){
                # //                        fnMnuItm -> space = script -> read_idata();
                #                        self.writer.intValue("fnMnuItm.vSpace");
                #                    }
                #                    else
                #                        _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_NO_DEACTIVATE_FLAG:
            elif section == Section.SET_NO_DEACTIVATE_FLAG:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU,
                    Mode.AML_INIT_EVENT,
                )
                self.writer.flag('FM_NO_DEACTIVATE')
                #                if(curMode == AS_INIT_MENU){
                # //                    fnMnu -> flags |= FM_NO_DEACTIVATE;
                #                }
                #                else {
                #                    if(curMode == AML_INIT_EVENT){
                # //                        mlEv -> flags |= AML_NO_DEACTIVATE;
                #                    }
                #                    else
                #                        _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_LOCATION_MENU_FLAG:
            elif section == Section.SET_LOCATION_MENU_FLAG:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.writer.flag('FM_LOCATION_MENU')
                #                if(curMode == AS_INIT_MENU){
                # //                    fnMnu -> flags |= FM_LOCATION_MENU;
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_BML_NAME:
            elif section == Section.SET_BML_NAME:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_IND,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.BM_INIT_MENU_ITEM,
                )
                if self.writer.has_mode(Mode.AS_INIT_MENU):
                    self.writer.str('bml_name')
                elif self.writer.has_mode(Mode.AS_INIT_IND):
                    self.writer.str('bml.name')
                elif self.writer.has_mode(Mode.AS_INIT_INFO_PANEL):
                    self.writer.str('bml_name')
                elif self.writer.has_mode(Mode.BM_INIT_MENU_ITEM):
                    self.writer.str('fname')

                #                if(curMode == AS_INIT_MENU){
                # //                    script -> read_pdata(&fnMnu -> bml_name,1);
                #                    self.writer.strValue("fnMnu.bml_name");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_IND){
                # //                        script -> prepare_pdata();
                # //
                # //                        if(aInd -> bml)
                # //                            _handle_error("aIndData::bml already inited");
                # //
                # //                        aInd -> bml = new bmlObject;
                # //                        aInd -> bml -> init_name(script -> get_conv_ptr());
                #                        self.writer.strValue("aInd.bml.init_name(");
                #                    }
                #                    else {
                #                        if(curMode == AS_INIT_INFO_PANEL){
                # //                            script -> read_pdata(&iPl -> bml_name,1);
                #                            self.writer.strValue("iPl.bml_name");
                #                        }
                #                        else {
                #                            if(curMode == BM_INIT_MENU_ITEM){
                # //                                script -> read_pdata(&aciBM_it -> fname,1);
                #                                self.writer.strValue("aciBM_it.fname");
                #                            }
                #                            else
                #                                _handle_error("Misplaced option",aOptIDs[id]);
                #                        }
                #                    }
                #                }
                #                break;
            #            case INIT_BACK_BML:
            elif section == Section.INIT_BACK_BML:
                self.writer.assert_mode(
                    Mode.AS_INIT_MATRIX,
                )
                self.writer.str()
                #                if(curMode == AS_INIT_MATRIX){
                # //                    script -> prepare_pdata();
                # //
                # //                    if(invMat -> back)
                # //                        _handle_error("invMatrix::back already inited");
                # //
                # //                    invMat -> back = new bmlObject;
                # //                    invMat -> back -> init_name(script -> get_conv_ptr());
                #                    self.writer.strValue("invMat.back.init_name(");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case SET_IBS_NAME:
            elif section == Section.SET_IBS_NAME:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_COUNTER,
                )
                self.writer.str()
                #                if(curMode == AS_INIT_MENU){
                # //                    script -> read_pdata(&fnMnu -> ibs_name,1);
                #                    self.writer.strValue("fnMnu.ibs_name");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_INFO_PANEL){
                # //                        script -> read_pdata(&iPl -> ibs_name,1);
                #                        self.writer.strValue("iPl.ibs_name");
                #                    }
                #                    else {
                #                        if(curMode == AS_INIT_COUNTER){
                # //                            script -> read_pdata(&cP -> ibs_name,1);
                #                            self.writer.strValue("cP.ibs_name");
                #                        }
                #                        else
                #                            _handle_error("Misplaced option",aOptIDs[id]);
                #                    }
                #                }
                #                break;
            #            case SET_MAP_NAME:
            elif section == Section.SET_MAP_NAME:
                if self.writer.has_mode(Mode.AS_INIT_LOC_DATA):
                    self.writer.str()
                else:
                    self.writer.int('t_id')
                    self.writer.str()
                #                if(curMode == AS_INIT_LOC_DATA){
                # //                    script -> read_pdata(&locData -> mapName,1);
                #                    self.writer.strValue("locData.mapName");
                #                }
                #                else {
                # //                    t_id = script -> read_idata();
                #                    self.writer.intValue("t_id");
                # //                    script -> read_pdata(&aScrDisp -> map_names[t_id],1);
                #                    self.writer.strValue("aScrDisp.map_names[$t_id]");
                #                }
                #                break;
            #            case SET_SAVE_SCREEN_ID:
            elif section == Section.SET_SAVE_SCREEN_ID:
                self.writer.assert_mode(
                    Mode.AS_INIT_LOC_DATA,
                )
                self.writer.int('SaveScreenID')
                #                if(curMode == AS_INIT_LOC_DATA){
                # //                    locData -> SaveScreenID = script -> read_idata();
                #                    self.writer.intValue("locData.SaveScreenID");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_WORLD_ID:
            elif section == Section.SET_WORLD_ID:
                self.writer.assert_mode(
                    Mode.AS_INIT_LOC_DATA,
                )
                self.writer.int('WorldID')
                #                if(curMode == AS_INIT_LOC_DATA){
                # //                    locData -> WorldID = script -> read_idata();
                #                    self.writer.intValue("locData.WorldID");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case SET_EXCLUDE:
            elif section == Section.SET_EXCLUDE:
                self.writer.assert_mode(
                    Mode.AS_INIT_LOC_DATA,
                )
                self.writer.int('t_id')
                #                if(curMode == AS_INIT_LOC_DATA){
                # //                    t_id = script -> read_idata();
                #                    self.writer.intValue("t_id", "locData -> ExcludeItems[t_id] = 1;");
                # //                    locData -> ExcludeItems[t_id] = 1;
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_SCREEN_ID:
            elif section == Section.INIT_SCREEN_ID:
                self.writer.assert_mode(
                    Mode.AS_INIT_LOC_DATA,
                )
                self.writer.str('screenID')
                #                if(curMode == AS_INIT_LOC_DATA){
                # //                    script -> read_pdata(&locData -> screenID,1);
                #                    self.writer.strValue("locData.screenID");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_PAL_NAME:
            elif section == Section.INIT_PAL_NAME:
                self.writer.assert_mode(
                    Mode.AS_INIT_LOC_DATA,
                )
                self.writer.str('palName')
                #                if(curMode == AS_INIT_LOC_DATA){
                # //                    script -> read_pdata(&locData -> palName,1);
                #                    self.writer.strValue("locData.palName");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_CUR_FNC:
            elif section == Section.INIT_CUR_FNC:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.writer.int('curFunction')
                #                if(curMode == AS_INIT_MENU){
                # //                    fnMnu -> curFunction = script -> read_idata();
                #                    self.writer.intValue("fnMnu.curFunction");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_FONT:
            elif section == Section.INIT_FONT:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU_ITEM,
                    Mode.AS_INIT_INFO_PANEL,
                    Mode.AS_INIT_WORLD_DATA,
                    Mode.AS_INIT_COUNTER,
                    Mode.AS_INIT_IBS,
                )
                self.writer.int('font')
                #                if(curMode == AS_INIT_MENU_ITEM){
                # //                    fnMnuItm -> font = script -> read_idata();
                #                    self.writer.intValue("fnMnuItm.font");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_INFO_PANEL){
                # //                        iPl -> font = script -> read_idata();
                #                        self.writer.intValue("iPl.font");
                #                    }
                #                    else {
                #                        if(curMode == AS_INIT_WORLD_DATA){
                # //                            wData -> font = script -> read_idata();
                #                            self.writer.intValue("wData.font");
                #                        }
                #                        else {
                #                            if(curMode == AS_INIT_COUNTER){
                # //                                cP -> font = script -> read_idata();
                #                                self.writer.intValue("cP.font");
                #                            }
                #                            else {
                #                                if(curMode == AS_INIT_IBS){
                # //                                    ibsObj -> fontID = script -> read_idata();
                #                                    self.writer.intValue("ibsObj.font");
                #                                }
                #                                else
                #                                    _handle_error("Misplaced option",aOptIDs[id]);
                #                            }
                #                        }
                #                    }
                #                }
                #                break;
            #            case INIT_VSPACE:
            elif section == Section.INIT_VSPACE:
                self.writer.assert_mode(
                    Mode.AS_INIT_INFO_PANEL,
                )
                self.writer.int('vSpace')
                #                if(curMode == AS_INIT_INFO_PANEL){
                # //                    iPl -> vSpace = script -> read_idata();
                #                    self.writer.intValue("iPl.vSpace");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_HSPACE:
            elif section == Section.INIT_HSPACE:
                self.writer.assert_mode(
                    Mode.AS_INIT_INFO_PANEL,
                )
                self.writer.int('hSpace')
                #                if(curMode == AS_INIT_INFO_PANEL){
                # //                    iPl -> hSpace = script -> read_idata();
                #                    self.writer.intValue("iPl.hSpace");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_STRING:
            elif section == Section.INIT_STRING:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU_ITEM,
                )
                self.writer.str('name')
                #                if(curMode == AS_INIT_MENU_ITEM){
                # //                    script -> prepare_pdata();
                # //                    fnMnuItm -> init_name(script -> get_conv_ptr());
                #                    self.writer.strValue("fnMnuItm.init_name(");
                #                }
                #                else
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                break;
            #            case INIT_SCANCODE:
            elif section == Section.INIT_SCANCODE:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU,
                    Mode.AS_INIT_MENU_ITEM,
                    Mode.AS_INIT_BUTTON,
                    Mode.AML_INIT_EVENT,
                )
                self.writer.int('key')
                #                if(curMode == AS_INIT_MENU){
                # //                    fnMnu -> add_key(script -> read_key());
                #                    self.writer.intValue("fnMnu.add_key(");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_MENU_ITEM){
                # //                        fnMnuItm -> add_key(script -> read_key());
                #                        self.writer.intValue("fnMnuItm.add_key(");
                #                    }
                #                    else {
                #                        if(curMode == AS_INIT_BUTTON){
                # //                            aBt -> add_key(script -> read_key());
                #                            self.writer.intValue("aBt.add_key(");
                #                        }
                #                        else {
                #                            if(curMode == AML_INIT_EVENT){
                # //                                mlEv -> add_key(script -> read_key());
                #                                self.writer.intValue("mlEv.add_key(");
                #                            }
                #                            else
                #                                _handle_error("Misplaced option",aOptIDs[id]);
                #                        }
                #                    }
                #                }
                #                break;
            #            case INIT_MENU_TYPE:
            elif section == Section.INIT_MENU_TYPE:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.writer.int('type')
                #                if(curMode == AS_INIT_MENU){
                # //                    fnMnu -> type = script -> read_idata();
                #                    self.writer.intValue("fnMnu.type");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_UP_KEY:
            elif section == Section.INIT_UP_KEY:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.writer.int('up_key')
                #                if(curMode == AS_INIT_MENU){
                # //                    fnMnu -> up_key -> add_key(script -> read_key());
                #                    self.writer.intValue("fnMnu.up_key.add_key(");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_DOWN_KEY:
            elif section == Section.INIT_DOWN_KEY:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.writer.int('down_key')
                #                if(curMode == AS_INIT_MENU){
                # //                    fnMnu -> down_key -> add_key(script -> read_key());
                #                    self.writer.intValue("fnMnu.down_key.add_key(");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_TRIGGER:
            elif section == Section.INIT_TRIGGER:
                self.writer.assert_mode(
                    Mode.AS_INIT_MENU,
                )
                self.writer.int('trigger_code')
                #                if(curMode == AS_INIT_MENU){
                # //                    fnMnu -> trigger_code = script -> read_idata();
                #                    self.writer.intValue("fnMnu.trigger_code");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_ID:
            elif section == Section.INIT_ID:
                self.writer.assert_mode(
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
                if self.writer.has_mode(Mode.AS_INIT_LOC_DATA):
                    self.writer.int('t_id')
                    self.writer.str('id')
                elif self.writer.has_mode(Mode.AS_INIT_MATRIX):
                    self.writer.str('id')
                else:
                    self.writer.int('id')
                #                if(curMode == AS_INIT_BUTTON){
                # //                    aBt -> ID = script -> read_idata();
                #                    self.writer.intValue("aBt.ID");
                #                }
                #                else {
                #                    if(curMode == AS_INIT_ITEM){
                # //                        invItm -> ID = script -> read_idata();
                #                        self.writer.intValue("invItm.ID");
                #                    }
                #                    else {
                #                        if(curMode == AS_INIT_LOC_DATA){
                # //                            t_id = script -> read_idata();
                #                            self.writer.intValue("t_id");
                # //                            script -> read_pdata(&locData -> objIDs[t_id],1);
                #                            self.writer.strValue("locData.objIDs[${t_id}]");
                #                        }
                #                        else {
                #                            if(curMode == AS_INIT_MATRIX){
                # //                                script -> read_pdata(&invMat -> mech_name,1);
                #                                self.writer.strValue("invMat.mech_name");
                #                            }
                #                            else {
                #                                if(curMode == AS_INIT_INFO_PANEL){
                # //                                    iPl -> type = script -> read_idata();
                #                                    self.writer.intValue("iPl.type");
                #                                }
                #                                else {
                #                                    if(curMode == AS_INIT_COUNTER){
                # //                                        cP -> ID = script -> read_idata();
                #                                        self.writer.intValue("cP.ID");
                #                                    }
                #                                    else {
                #                                        if(curMode == AML_INIT_DATA_SET){
                # //                                            mlDataSet -> ID = script -> read_idata();
                #                                            self.writer.intValue("mlDataSet.ID");
                #                                        }
                #                                        else {
                #                                            if(curMode == AML_INIT_DATA){
                # //                                                mlData -> ID = script -> read_idata();
                #                                                self.writer.intValue("mlData.ID");
                #                                            }
                #                                            else {
                #                                                if(curMode == BM_INIT_MENU_ITEM){
                # //                                                    aciBM_it -> ID = script -> read_idata();
                #                                                    self.writer.intValue("aciBM_it.ID");
                #                                                }
                #                                                else {
                #                                                    if(curMode == BM_INIT_MENU){
                # //                                                        aciBM -> ID = script -> read_idata();
                #                                                        self.writer.intValue("aciBM.ID");
                #                                                    }
                #                                                    else {
                #                                                        if(curMode == AML_INIT_EVENT_SEQ){
                # //                                                            mlEvSeq -> add_id(script -> read_idata());
                #                                                            self.writer.intValue("mlEvSeq.add_id(");
                #                                                        }
                #                                                        else
                #                                                            _handle_error("Misplaced option",aOptIDs[id]);
                #                                                    }
                #                                                }
                #                                            }
                #                                        }
                #                                    }
                #                                }
                #                            }
                #                        }
                #                    }
                #                }
                #                break;
            #            case INIT_S_ID:
            elif section == Section.INIT_S_ID:
                self.writer.assert_mode(
                    Mode.AS_INIT_LOC_DATA,
                )
                self.writer.int('t_id')
                self.writer.str('s_objIDs[$t_id]')
                #                if(curMode == AS_INIT_LOC_DATA){
                # //                    t_id = script -> read_idata();
                #                    self.writer.intValue("t_id");
                # //                    script -> read_pdata(&locData -> s_objIDs[t_id],1);
                #                    self.writer.strValue("locData.s_objIDs[$t_id]");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
            #            case INIT_MODE_KEY:
            elif section == Section.INIT_MODE_KEY:
                self.writer.int('key')
                # //                aScrDisp -> ModeObj -> add_key(script -> read_key());
                #                self.writer.intValue("aScrDisp.ModeObj.add_key");
                #                break;
            #            case INIT_INV_KEY:
            elif section == Section.INIT_INV_KEY:
                self.writer.int('key')
                # //                aScrDisp -> InvObj -> add_key(script -> read_key());
                #                self.writer.intValue("aScrDisp.InvObj.add_key");
                #                break;
            #            case INIT_INFO_KEY:
            elif section == Section.INIT_INFO_KEY:
                self.writer.int('key')
                # //                aScrDisp -> InfoObj -> add_key(script -> read_key());
                #                self.writer.intValue("aScrDisp.InfoObj.add_key");
                #                break;
            #            case SET_CURMATRIX:
            elif section == Section.SET_CURMATRIX:
                self.writer.int('curMatrix')
                # //                curMatrix = script -> read_idata();
                #                self.writer.intValue("curMatrix");
                #                break;
            #            case INIT_CUR_IBS:
            elif section == Section.INIT_CUR_IBS:
                self.writer.int('curIbsID')
                # //                aScrDisp -> curIbsID = script -> read_idata();
                #                self.writer.intValue("aScrDisp.curIbsID");
                #                break;
            #            case NEW_LOC_DATA:
            elif section == Section.NEW_LOC_DATA:
                self.writer.assert_mode(Mode.AS_NONE)
                
                self.writer.int(name='id')
                self.writer.set_mode(Mode.AS_INIT_LOC_DATA)
                # //                if(curMode != AS_NONE){
                # //                    _handle_error("Misplaced option",aOptIDs[id]);
                # //                }
                # //                locData = new aciLocationInfo;
                # //                locData -> ID = script -> read_idata();
                #                self.writer.intValue("locData.ID");
                #                curMode = AS_INIT_LOC_DATA;
                #                self.writer.mode(curMode);
                #                break;
            #            case NEW_COL_SCHEME:
            elif section == Section.NEW_COL_SCHEME:
                if self.writer.has_mode(Mode.AS_INIT_LOC_DATA):
                    self.writer.int(name='numColorScheme')
                self.writer.int('curScheme')
                self.writer.set_mode(Mode.AS_INIT_COLOR_SCHEME)
                #                if(curMode != AS_NONE){
                #                    if(curMode == AS_INIT_LOC_DATA){
                # //                        locData -> numColorScheme = script -> read_idata();
                #                        self.writer.intValue("locData.numColorScheme");
                #                    }
                #                    else
                #                        _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                curMode = AS_INIT_COLOR_SCHEME;
                #                self.writer.mode(curMode);
                # //                t_id = script -> read_idata();
                #                self.writer.intValue("curScheme", "aciColorSchemes[t_id] = new unsigned char[aciColSchemeLen]; memset(aciColorSchemes[t_id],0,aciColSchemeLen)");
                # //                curScheme = t_id;
                # //                aciColorSchemes[t_id] = new unsigned char[aciColSchemeLen];
                # //                memset(aciColorSchemes[t_id],0,aciColSchemeLen);
                #                break;
            #            case INIT_NUM_SCHEMES:
            elif section == Section.INIT_NUM_SCHEMES:
                self.writer.int('aciNumColSchemes')
                # //                aciNumColSchemes = script -> read_idata();
                #                self.writer.intValue("aciNumColSchemes");
                # //                aciColorSchemes = new unsigned char*[aciNumColSchemes];
                # //                for(i = 0; i < aciNumColSchemes; i ++)
                # //                    aciColorSchemes[i] = NULL;
                #                break;
            #            case INIT_SCHEME_LEN:
            elif section == Section.INIT_SCHEME_LEN:
                self.writer.int('aciColSchemeLen')
            # //                aciColSchemeLen = script -> read_idata();
            #                self.writer.intValue("aciColSchemeLen");
            #                break;
            #            case INIT_COLOR:
            elif section == Section.INIT_COLOR:
                self.writer.assert_mode(Mode.AS_INIT_COLOR_SCHEME)
                self.writer.int('t_id')
                self.writer.int('scheme')
                #                if(curMode == AS_INIT_COLOR_SCHEME){
                # //                    t_id = script -> read_idata();
                #                    self.writer.intValue("t_id");
                # //                    aciColorSchemes[curScheme][t_id] = script -> read_idata();
                #                    self.writer.intValue("aciColorSchemes[curScheme][${t_id}]");
                #                }
                #                else {
                #                    _handle_error("Misplaced option",aOptIDs[id]);
                #                }
                #                break;
                #        }
            else:
                raise ValueError("Invalid section: {}".format(section))
            self.writer.end_section()
        self.writer.flush()
