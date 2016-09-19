from vangers_utils.script.options import Section, Mode
from vangers_utils.script.writer import Writer


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

def convert(in_file: str, out_file: str):
    #    int i,id,t_id = 0,sz = 0,num;
    #
    #    char* ptr;
    #    char* pdata = new char[512];
    # //    iListElement* elemPtr;
    # //
    # //    invMatrix* mtx;
    # //    invItem* itm;
    # //
    # //    aScrDisp = new actIntDispatcher;
    # //    aciML_D = new aciML_Dispatcher;
    #    ScriptFile *script1 = new ScriptFile;
    #    ScriptWriter writer(outTxtFileName, script1);
    ##ifndef _BINARY_SCRIPT_
    #    _sALLOC_HEAP_(3000000,char);
    ##endif
    #
    ##ifndef _BINARY_SCRIPT_
    #    script -> set_bscript_name(bname);
    ##endif
    #    script1 -> load(fname);
    #    script1 -> prepare();
    #
    #    int mlEvSeqSize = 0;
    writer = Writer(in_file, out_file)
    mlEvSeqSize = None
    fnMenuFlags = 0

    while True:
        section = writer.new_section()

        #    while(!script1 -> EOF_Flag){
        ##ifndef _BINARY_SCRIPT_
        #        if(script -> curBlock && *script -> curBlock -> data){
        ##endif
        #        id = writer.newSection();
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
        # //        writer.mode(curMode);
        #        switch(id){
        if section == Section.INIT_MECHOS_PRM:
            writer.composite(('unused', 'int32'),
                             ('matrixId', 'int32'),
                             ('shift', 'int32'),
                             ('data', 'str'))

            #            case INIT_MECHOS_PRM:
            #                writer.intValue("unused")
            #                writer.intValue("matrixId", "aScrDisp -> get_imatrix(t_id)");
            # //                mtx = aScrDisp -> get_imatrix(t_id);
            # //                if(mtx){
            # //                    t_id = script -> read_idata();
            #                writer.intValue("t_id2", "pData + t_id * ACI_MAX_PRM_LEN");
            #                writer.intValue("t_id3", nullptr);
            # //                    if(!mtx -> pData) mtx -> alloc_prm();
            # //                    ptr = mtx -> pData + t_id * ACI_MAX_PRM_LEN;
            #                writer.strValue("pdata");
            # //                }
            # //                else
            # //                    _handle_error("Bad matrix ID");
            #                break;
            #            case INIT_ITEM_PRM:
        elif section == Section.INIT_ITEM_PRM:
            writer.composite(('iitem', 'int32'),
                             ('shift', 'int32'),
                             ('data', 'str'))
    # //                t_id = script -> read_idata();
    # //                itm = aScrDisp -> get_iitem(t_id);
    #                writer.intValue("t_id1", "aScrDisp -> get_iitem(t_id)");
    # //                if(itm){
    # //                    t_id = script -> read_idata();
    # //                    if(!itm -> pData) itm -> alloc_prm();
    # //                    ptr = itm -> pData + t_id * ACI_MAX_PRM_LEN;
    #                writer.intValue("t_id2", "pData + t_id * ACI_MAX_PRM_LEN");
    # //                    script -> read_pdata(&ptr);
    #                writer.strValue("pdata");
    # //                }
    # //                else
    # //                    _handle_error("Bad item ID");
    #                break;
    #            case SET_PROMPT_TEXT:
        elif section == Section.SET_PROMPT_TEXT:
    #                if(curMode == AS_INIT_BUTTON){
            if writer.has_mode(Mode.AS_INIT_BUTTON):
                writer.str('aBt_promptData')
    #                    writer.strValue("aBt_promptData");
    # //                    script -> read_pdata(&aBt -> promptData,1);
    #                }
    #                else {
    #                    if(curMode == AS_INIT_IND){
            elif writer.has_mode(Mode.AS_INIT_IND):
                writer.str('aInd_promptData')
    #                        writer.strValue("aInd_promptData");
    # //                        script -> read_pdata(&aInd -> promptData,1);
    #                    }
    #                    else {
    #                        if(curMode == AS_INIT_ITEM){
            elif writer.has_mode(Mode.AS_INIT_ITEM):
                writer.str('invItm_promptData')
            else:
                raise ValueError("Misplaced option"+str(section))
    #                            writer.strValue("invItm_promptData");
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
            writer.assert_mode(Mode.AS_INIT_LOC_DATA)
            writer.int("alloc_gate_shutters(t_id)")
    #                if(curMode == AS_INIT_LOC_DATA){
    # //                    t_id = script -> read_idata();
    # //                    locData -> alloc_gate_shutters(t_id);
    #                    writer.intValue("t_id1", "alloc_gate_shutters(t_id)");
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case ADD_MAP_INFO_FILE:
        elif section == Section.ADD_MAP_INFO_FILE:
            writer.assert_mode(Mode.AS_INIT_LOC_DATA)
            writer.str("elemPtr -> init_id(script -> get_conv_ptr());")
    #                if(curMode == AS_INIT_LOC_DATA){
    #                    writer.bufValue("id", "elemPtr -> init_id(script -> get_conv_ptr());");
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
            writer.assert_mode(Mode.AS_INIT_LOC_DATA)
            writer.str("&locData -> soundResPath")
    #                if(curMode == AS_INIT_LOC_DATA){
    #                    writer.strValue("&locData -> soundResPath");
    # //                    script -> read_pdata(&locData -> soundResPath,1);
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case INIT_NUM_MATRIX_SHUTTERS:
        elif section == Section.INIT_NUM_MATRIX_SHUTTERS:
            writer.assert_mode(Mode.AS_INIT_LOC_DATA)
            writer.composite(('i_id', 'int32'), ('sz', 'int32'))
            #                if(curMode == AS_INIT_LOC_DATA){
            # //                    t_id = script -> read_idata();
            # //                    sz = script -> read_idata();
            #                    writer.intValue("t_id");
            #                    writer.intValue("zs", "locData -> alloc_matrix_shutters(t_id,sz)");
            # //                    locData -> alloc_matrix_shutters(t_id,sz);
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case INIT_SHUTTER_POS:
        elif section == Section.INIT_NUM_MATRIX_SHUTTERS:
            writer.assert_mode(Mode.AS_INIT_SHUTTER)
            writer.composite(
                ('id', 'int32'),
                ('Pos[$id].X', 'int32'),
                ('Pos[$id].Y', 'int32'),
            )
            #                if(curMode == AS_INIT_SHUTTER){
            # //                    t_id = script -> read_idata();
            #                    writer.intValue("t_id");
            # //                    locSh -> Pos[t_id].X = script -> read_idata();
            # //                    locSh -> Pos[t_id].Y = script -> read_idata();
            #                    writer.intValue("pos_x", "locSh -> Pos[t_id].X = script -> read_idata()");
            #                    writer.intValue("pos_y", "locSh -> Pos[t_id].Y = script -> read_idata()");
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case INIT_SHUTTER_DELTA:
        elif section == Section.INIT_SHUTTER_DELTA:
            writer.assert_mode(Mode.AS_INIT_SHUTTER)
            writer.composite(
                ('id', 'int32'),
                ('Delta.X', 'int32'),
                ('Delta.Y', 'int32'),
            )
            #                if(curMode == AS_INIT_SHUTTER){
            # //                    locSh -> Delta.X = script -> read_idata();
            # //                    locSh -> Delta.Y = script -> read_idata();
            #                    writer.intValue("Delta.X", "locSh -> Delta.X = script -> read_idata()");
            #                    writer.intValue("Delta.Y", "locSh -> Delta.Y = script -> read_idata()");
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case NEW_GATE_SHUTTER:
        elif section == Section.NEW_GATE_SHUTTER:
            writer.assert_mode(Mode.AS_INIT_LOC_DATA)
            writer.set_mode(Mode.AS_INIT_SHUTTER)
            writer.int(name='id')
            #                if(curMode == AS_INIT_LOC_DATA){
            #                    curMode = AS_INIT_SHUTTER;
            #                    writer.mode(curMode);
            # //                    locSh = new aciLocationShutterInfo;
            #
            # //                    t_id = script -> read_idata();
            #                    writer.intValue("t_id", "locData -> GateShutters[t_id] = locSh");
            # //                    if(t_id < 0 || t_id >= locData -> numGateShutters) ErrH.Abort("Bad shutter index...");
            # //                    locData -> GateShutters[t_id] = locSh;
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case NEW_MATRIX_SHUTTER:
        elif section == Section.NEW_MATRIX_SHUTTER:
            writer.assert_mode(Mode.AS_INIT_LOC_DATA)
            writer.set_mode(Mode.AS_INIT_SHUTTER)
            writer.composite(
                ('shutterNum', 'int32'),
                ('id', 'int32'),
            )
            #                if(curMode == AS_INIT_LOC_DATA){
            #                    curMode = AS_INIT_SHUTTER;
            #                    writer.mode(curMode);
            # //                    t_id = script -> read_idata();
            #                    writer.intValue("t_id", "locData -> MatrixShutters${t_id}[sz] = locSh");
            # //                    sz = script -> read_idata();
            #                    writer.intValue("sz");
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
            writer.int()
            # //                aciML_D -> startup_timer = script -> read_idata();
            #                writer.intValue("aciML_D.startup_timer");
            #                break;
        #            case SET_UPMENU_FLAG:
        elif section == Section.SET_UPMENU_FLAG:
            writer.flag('upMenuFlag')
            # //                upMenuFlag = 1;
            #                break;
        #            case INIT_SHUTDOWN_TIME:
        elif section == Section.SET_UPMENU_FLAG:
            writer.int()
            # //                aciML_D -> shutdown_timer = script -> read_idata();
            #                writer.intValue("aciML_D.shutdown_timer");
            #                break;
        #            case NEW_ML_EVENT_COMMAND:
        elif section == Section.SET_UPMENU_FLAG:
            writer.assert_mode(Mode.AML_INIT_EVENT)
            writer.set_mode(Mode.AML_INIT_EVENT_COMMAND)
            #                if(curMode != AML_INIT_EVENT)
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            # //                mlEvComm = new aciML_EventCommand;
            #                curMode = AML_INIT_EVENT_COMMAND;
            #                writer.mode(curMode);
            #                break;
        #            case NEW_ML_EVENT:
        elif section == Section.NEW_ML_EVENT:
            writer.assert_mode(Mode.AML_INIT_DATA)
            writer.set_mode(Mode.AML_INIT_EVENT)
            # //                if(curMode != AML_INIT_DATA)
            # //                    _handle_error("Misplaced option",aOptIDs[id]);
            # //                mlEv = new aciML_Event;
            #                curMode = AML_INIT_EVENT;
            #                writer.mode(curMode);
            #                break;
        #            case NEW_ML_DATA:
        elif section == Section.NEW_ML_DATA:
            writer.assert_mode(Mode.AML_INIT_DATA_SET)
            writer.set_mode(Mode.AML_INIT_DATA)
            # //                if(curMode != AML_INIT_DATA_SET)
            # //                    _handle_error("Misplaced option",aOptIDs[id]);
            # //                mlData = new aciML_Data;
            #                curMode = AML_INIT_DATA;
            #                writer.mode(curMode);
            #                break;
        #            case NEW_ML_EVENT_SEQ:
        elif section == Section.NEW_ML_EVENT_SEQ:
            writer.assert_mode(Mode.AML_INIT_DATA_SET)
            writer.set_mode(Mode.AML_INIT_EVENT_SEQ)
            writer.int(name='id')
            mlEvSeqSize = writer.int(name='size')
            # //                if(curMode != AML_INIT_DATA_SET)
            # //                    _handle_error("Misplaced option",aOptIDs[id]);
            # //                mlEvSeq = new aciML_EventSeq;
            # //                mlEvSeq -> ID = script -> read_idata();
            #                writer.intValue("mlEvSeq.ID");
            # //                mlEvSeq -> size = script -> read_idata();
            #                mlEvSeqSize = writer.intValue("mlEvSeq.size");
            # //                mlEvSeq -> alloc_mem(mlEvSeq -> size);
            #                curMode = AML_INIT_EVENT_SEQ;
            #                writer.mode(curMode);
            #                break;
        #            case NEW_BITMAP_MENU:
        elif section == Section.NEW_ML_EVENT_SEQ:
            writer.assert_mode(Mode.AS_NONE)
            writer.set_mode(Mode.BM_INIT_MENU)
            # //                if(curMode != AS_NONE)
            # //                    _handle_error("Misplaced option",aOptIDs[id]);
            # //                aciBM = new aciBitmapMenu;
            #                curMode = BM_INIT_MENU;
            #                writer.mode(curMode);
            #                break;
        #            case NEW_BITMAP_MENU_ITEM:
        elif section == Section.NEW_BITMAP_MENU_ITEM:
            writer.assert_mode(Mode.BM_INIT_MENU)
            writer.set_mode(Mode.BM_INIT_MENU_ITEM)
            # //                if(curMode != BM_INIT_MENU)
            # //                    _handle_error("Misplaced option",aOptIDs[id]);
            # //                aciBM_it = new aciBitmapMenuItem;
            #                curMode = BM_INIT_MENU_ITEM;
            #                writer.mode(curMode);
            #                break;
        #            case NEW_ML_DATA_SET:
        elif section == Section.NEW_ML_DATA_SET:
            writer.assert_mode(Mode.AS_NONE)
            writer.set_mode(Mode.AML_INIT_DATA_SET)
            # //                if(curMode != AS_NONE)
            # //                    _handle_error("Misplaced option",aOptIDs[id]);
            # //                mlDataSet = new aciML_DataSet;
            #                curMode = AML_INIT_DATA_SET;
            #                writer.mode(curMode);
            #                break;
        #            case NEW_ML_ITEM_DATA:
        elif section == Section.NEW_ML_ITEM_DATA:
            writer.assert_mode(Mode.AML_INIT_DATA_SET)
            writer.composite(
                ('ItemID', 'int32'),
                ('NullLevel', 'int32'),
                ('frameName', 'str'),
            )
            # //                if(curMode != AML_INIT_DATA_SET)
            # //                    _handle_error("Misplaced option",aOptIDs[id]);
            # //                mlItm = new aciML_ItemData;
            # //
            # //                mlItm -> ItemID = script -> read_idata();
            #                writer.intValue("mlItm.ItemID");
            # //                mlItm -> NullLevel = script -> read_idata();
            #                writer.intValue("mlItm.NullLevel");
            # //                script -> read_pdata(&mlItm -> frameName,1);
            #                writer.strValue("mlItm.frameName");
            # //                mlDataSet -> add_item(mlItm);
            #                break;
        #            case INIT_ML_EVENT_KEY_CODE:
        elif section == Section.INIT_ML_EVENT_KEY_CODE:
            writer.assert_mode(Mode.AML_INIT_EVENT)
            writer.int(name="mvEv.keys.addKey")
            #                if(curMode == AML_INIT_EVENT){
            #                    writer.intValue("mvEv.keys.addKey", "mlEv -> keys -> add_key(script -> read_idata());");
            # //                    mlEv -> keys -> add_key(script -> read_idata());
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case SET_RND_VALUE:
        elif section == Section.SET_RND_VALUE:
            writer.assert_mode(Mode.AML_INIT_EVENT)
            writer.int(name="mvEv.rndValue")
            #                if(curMode == AML_INIT_EVENT){
            # //                    mlEv -> rndValue = script -> read_idata();
            #                    writer.intValue("mvEv.rndValue", "mlEv -> rndValue = script -> read_idata();");
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case SET_SPEECH_CHANNEL:
        elif section == Section.SET_SPEECH_CHANNEL:
            writer.assert_mode(Mode.AML_INIT_DATA_SET)
            writer.int()
            #                if(curMode == AML_INIT_DATA_SET){
            # //                    mlDataSet -> SpeechChannel = script -> read_idata();
            #                    writer.intValue("mlDataSet.SpeechChannel");
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case SET_FRAME_CHECK_FLAG:
        elif section == Section.SET_FRAME_CHECK_FLAG:
            writer.assert_mode(Mode.AML_INIT_DATA)
            writer.flag('AML_FRAME_CHECK')
            #                if(curMode == AML_INIT_DATA){
            # //                    mlData -> flags |= AML_FRAME_CHECK;
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case SET_SPEECH_LEVEL:
        elif section == Section.SET_SPEECH_LEVEL:
            writer.assert_mode(Mode.AML_INIT_DATA_SET)
            writer.comment("mlDataSet -> SpeechPriority[t_id] = script -> read_idata()")
            writer.composite(
                ('t_id', 'int32'),
                ('speech_level', 'int32'),
            )
            #                if(curMode == AML_INIT_DATA_SET){
            # //                    t_id = script -> read_idata();
            #                    writer.intValue("t_id");
            # //                    mlDataSet -> SpeechPriority[t_id] = script -> read_idata();
            #                    writer.intValue("mlDataSet.SpeechPriority.t_id", "mlDataSet -> SpeechPriority[t_id] = script -> read_idata()");
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case SET_ML_EVENT_SEQUENCE:
        elif section == Section.SET_ML_EVENT_SEQUENCE:
            writer.assert_mode(Mode.AML_INIT_EVENT, Mode.AML_INIT_EVENT_SEQ)
            if writer.has_mode(Mode.AML_INIT_EVENT):
                writer.flag("AML_SEQUENCE_EVENT")
            elif writer.has_mode(Mode.AML_INIT_EVENT_SEQ):
                writer.composite_array(
                    ('seq_id', 'int32'),
                    ('seq_mode', 'int32'),
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
            #                            writer.intValue(buf);
            # //                            mlEvSeq -> SeqModes[t_id] = script -> read_idata();
            #                            sprintf(buf, "mlEvSeq.SeqModes[%d]", t_id);
            #                            writer.intValue(buf);
            #
            #                        }
            #                    }
            #                    else
            #                        _handle_error("Misplaced option",aOptIDs[id]);
            #                }
            #                break;
        #            case INIT_ML_EVENT_CODE:
        elif section == Section.INIT_ML_EVENT_CODE:
            writer.assert_mode(Mode.AML_INIT_EVENT_COMMAND)
            writer.composite(
                ('code', 'int32'),
                ('data1', 'int32'),
                ('data2', 'int32'),
            )
            #                if(curMode == AML_INIT_EVENT_COMMAND){
            # //                    mlEvComm -> code = script -> read_idata();
            #                    writer.intValue("mlEvComm.code");
            # //                    mlEvComm -> data0 = script -> read_idata();
            #                    writer.intValue("mlEvComm.data0");
            # //                    mlEvComm -> data1 = script -> read_idata();
            #                    writer.intValue("mlEvComm.data1");
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case INIT_ML_EVENT_STARTUP:
        elif section == Section.INIT_ML_EVENT_STARTUP:
            writer.assert_mode(Mode.AML_INIT_EVENT)
            writer.int()
            #                if(curMode == AML_INIT_EVENT){
            # //                    mlEv -> startupType = script -> read_idata();
            #                    writer.intValue("mlEv.startupType");
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case SET_PRIORITY:
        elif section == Section.SET_PRIORITY:
            writer.assert_mode(Mode.AML_INIT_EVENT, Mode.AML_INIT_EVENT_SEQ)
            writer.int()
            #                if(curMode == AML_INIT_EVENT){
            # //                    mlEv -> priority = script -> read_idata();
            #                    writer.intValue("mlEv.priority");
            #                }
            #                else {
            #                    if(curMode == AML_INIT_EVENT_SEQ){
            # //                        mlEvSeq -> dropLevel[0] = script -> read_idata();
            #                        writer.intValue("mlEvSeq.dropLevel[0]");
            #                    }
            #                    else
            #                        _handle_error("Misplaced option",aOptIDs[id]);
            #                }
            #                break;
        #            case SET_NOT_LOCKED_FLAG:
        elif section == Section.SET_NOT_LOCKED_FLAG:
            writer.assert_mode(Mode.AML_INIT_EVENT)
            writer.flag('AML_IF_NOT_LOCKED')
            #                if(curMode == AML_INIT_EVENT){
            # //                    mlEv -> flags |= AML_IF_NOT_LOCKED;
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case SET_LOCKED_FLAG:
        elif section == Section.SET_LOCKED_FLAG:
            writer.assert_mode(Mode.AML_INIT_EVENT)
            writer.flag('AML_IF_LOCKED')
            #                if(curMode == AML_INIT_EVENT){
            # //                    mlEv -> flags |= AML_IF_LOCKED;
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case INIT_START_TIMER:
        elif section == Section.INIT_START_TIMER:
            writer.assert_mode(Mode.AML_INIT_EVENT_COMMAND)
            writer.int()
            #                if(curMode == AML_INIT_EVENT_COMMAND){
            # //                    mlEvComm -> start_timer = script -> read_idata();
            #                    writer.intValue("mlEvComm.start_timer");
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case INIT_CHANNEL_ID:
        elif section == Section.INIT_CHANNEL_ID:
            writer.assert_mode(
                Mode.AML_INIT_EVENT,
                Mode.AML_INIT_DATA,
                Mode.AML_INIT_EVENT_SEQ,
            )
            writer.int()
            #                if(curMode == AML_INIT_EVENT){
            # //                    mlEv -> ChannelID = script -> read_idata();
            #                    writer.intValue("mlEv.ChannelID");
            #                }
            #                else {
            #                    if(curMode == AML_INIT_DATA){
            # //                        mlData -> ChannelID = script -> read_idata();
            #                        writer.intValue("mlData.ChannelID");
            #                    }
            #                    else {
            #                        if(curMode == AML_INIT_EVENT_SEQ){
            # //                            mlEvSeq -> ChannelID = script -> read_idata();
            #                            writer.intValue("mlEvSeq.ChannelID");
            #                        }
            #                        else
            #                            _handle_error("Misplaced option",aOptIDs[id]);
            #                    }
            #                }
            #                break;
        #            case INIT_ML_EVENT_SDATA:
        elif section == Section.INIT_ML_EVENT_SDATA:
            writer.assert_mode(Mode.AML_INIT_EVENT)
            writer.int()
            #                if(curMode == AML_INIT_EVENT){
            # //                    mlEv -> data = script -> read_idata();
            #                    writer.intValue("mlEv.data");
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case INIT_OFFS_X:
        elif section == Section.INIT_OFFS_X:
            writer.assert_mode(
                Mode.AS_INIT_WORLD_MAP,
                Mode.AS_INIT_IBS,
            )
            writer.composite(
                ('id', 'int32'),
                ('OffsX', 'int32'),
            )
            #                if(curMode == AS_INIT_WORLD_MAP){
            # //                    t_id = script -> read_idata();
            #                    writer.intValue("t_id");
            # //                    wMap -> ShapeOffsX[t_id] = script -> read_idata();
            #                    writer.intValue("wMap.ShapeOffsX[$t_id]", "wMap -> ShapeOffsX[t_id]");
            #                }
            #                else {
            #                    if(curMode == AS_INIT_IBS){
            # //                        t_id = script -> read_idata();
            #                        writer.intValue("t_id");
            # //                        ibsObj -> indPosX[t_id] = script -> read_idata();
            #                        writer.intValue("ibsObj.indPosX[$t_id]", "ibsObj -> indPosX[t_id] = script -> read_idata()");
            #                    }
            #                    else
            #                        _handle_error("Misplaced option",aOptIDs[id]);
            #                }
            #                break;
        #            case SET_WORLD_NAME:
        elif section == Section.SET_WORLD_NAME:
            writer.assert_mode(
                Mode.AS_INIT_WORLD_DATA,
                Mode.AML_INIT_DATA,
                Mode.AS_INIT_LOC_DATA,
                Mode.AS_INIT_SHUTTER,
            )
            if writer.has_mode(Mode.AS_INIT_WORLD_DATA):
                writer.str()
            elif writer.has_mode(Mode.AML_INIT_DATA):
                writer.str()
            elif writer.has_mode(Mode.AS_INIT_LOC_DATA):
                writer.composite(
                    ('nameId', 'str'),
                    ('nameId2', 'str'),
                )
            elif writer.has_mode(Mode.AS_INIT_SHUTTER):
                writer.str()
            #                if(curMode == AS_INIT_WORLD_DATA){
            # //                    script -> read_pdata(&wData -> name,1);
            #                    writer.strValue("wData.name");
            #                }
            #                else {
            #                    if(curMode == AML_INIT_DATA){
            # //                        script -> read_pdata(&mlData -> name,1);
            #                        writer.strValue("mlData.name");
            #                    }
            #                    else {
            #                        if(curMode == AS_INIT_LOC_DATA){
            # //                            script -> read_pdata(&locData -> nameID,1);
            # //                            script -> read_pdata(&locData -> nameID2,1);
            #                            writer.strValue("locData.nameID");
            #                            writer.strValue("locData.nameID2");
            #                        }
            #                        else {
            #                            if(curMode == AS_INIT_SHUTTER){
            # //                                script -> read_pdata(&locSh -> name,1);
            #                                writer.strValue("locSh.name");
            #                            }
            #                            else
            #                                _handle_error("Misplaced option",aOptIDs[id]);
            #                        }
            #                    }
            #                }
            #                break;
        #            case ADD_FLAG:
        elif section == Section.ADD_FLAG:
            writer.assert_mode(Mode.AS_INIT_WORLD_DATA)
            writer.int(comment="wData -> flags |= t_id;")
            #                if(curMode == AS_INIT_WORLD_DATA){
            # //                    t_id = script -> read_idata();
            #                    writer.intValue("t_id", "wData -> flags |= t_id;");
            # //                    wData -> flags |= t_id;
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case ADD_LINK:
        elif section == Section.ADD_LINK:
            writer.assert_mode(Mode.AS_INIT_WORLD_DATA)
            writer.int()
            #                if(curMode == AS_INIT_WORLD_DATA){
            #                    writer.intValue("t_id", " wData -> links[${t_id}] = 1");
            # //                    t_id = script -> read_idata();
            # //                    wData -> links[t_id] = 1;
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case SET_MAX_STR:
        elif section == Section.SET_MAX_STR:
            writer.assert_mode(Mode.AS_INIT_INFO_PANEL)
            writer.int()
            #                if(curMode == AS_INIT_INFO_PANEL){
            # //                    iPl -> MaxStr = script -> read_idata();
            #                    writer.intValue("iPl.MaxStr");
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case INIT_INFO_OFFS_X:
        elif section == Section.INIT_INFO_OFFS_X:
            writer.assert_mode(Mode.AS_INIT_INFO_PANEL)
            writer.int()
            #                if(curMode == AS_INIT_INFO_PANEL){
            # //                    iPl -> OffsX = script -> read_idata();
            #                    writer.intValue("iPl.OffsX");
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case INIT_BACK_COL:
        elif section == Section.INIT_BACK_COL:
            writer.assert_mode(
                Mode.AS_INIT_INFO_PANEL,
                Mode.AS_INIT_MENU,
            )
            writer.int()
            #                if(curMode == AS_INIT_INFO_PANEL){
            # //                    iPl -> bCol = script -> read_idata();
            #                    writer.intValue("iPl.bCol");
            #                }
            #                else {
            #                    if(curMode == AS_INIT_MENU){
            # //                        fnMnu -> bCol = script -> read_idata();
            #                        writer.intValue("fnMnu.bCol");
            #                    }
            #                    else
            #                        _handle_error("Misplaced option",aOptIDs[id]);
            #                }
            #                break;
        #            case SET_RANGE_FLAG:
        elif section == Section.SET_RANGE_FLAG:
            writer.assert_mode(
                Mode.AS_INIT_INFO_PANEL,
                Mode.AS_INIT_MENU,
                Mode.AS_INIT_COUNTER,
            )
            if writer.has_mode(Mode.AS_INIT_INFO_PANEL):
                writer.flag("IP_RANGE_FONT")
            elif writer.has_mode(Mode.AS_INIT_MENU):
                writer.flag("FM_RANGE_FONT")
                fnMenuFlags |= FM_RANGE_FONT
            elif writer.has_mode(Mode.AS_INIT_COUNTER):
                writer.flag("CP_RANGE_FONT")
            #                if(curMode == AS_INIT_INFO_PANEL){
            # //                    iPl -> flags |= IP_RANGE_FONT;
            #                }
            #                else {
            #                    if(curMode == AS_INIT_MENU){
            # //                        fnMnu -> flags |= FM_RANGE_FONT;
            #                        fnMenuFlags |= FM_RANGE_FONT;
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
            writer.assert_mode(Mode.AS_INIT_MENU)
            writer.flag("FM_SUBMENU")
            fnMenuFlags |= FM_SUBMENU
            #                if(curMode == AS_INIT_MENU){
            # //                    fnMnu -> flags |= FM_SUBMENU;
            #                    fnMenuFlags |= FM_SUBMENU;
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case SET_MAINMENU_FLAG:
        elif section == Section.SET_MAINMENU_FLAG:
            writer.assert_mode(Mode.AS_INIT_MENU)
            writer.flag("FM_MAIN_MENU")
            fnMenuFlags |= FM_MAIN_MENU
            #                if(curMode == AS_INIT_MENU){
            # //                    fnMnu -> flags |= FM_MAIN_MENU;
            #                    fnMenuFlags |= FM_MAIN_MENU;
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case INIT_INFO_OFFS_Y:
        elif section == Section.INIT_INFO_OFFS_Y:
            writer.assert_mode(Mode.AS_INIT_INFO_PANEL)
            writer.int()
            #                if(curMode == AS_INIT_INFO_PANEL){
            # //                    iPl -> OffsY = script -> read_idata();
            #                    writer.intValue("iPl.OffsY");
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case SET_NO_ALIGN:
        elif section == Section.SET_NO_ALIGN:
            writer.assert_mode(Mode.AS_INIT_INFO_PANEL)
            writer.flag("IP_NO_ALIGN")
            #                if(curMode == AS_INIT_INFO_PANEL){
            # //                    iPl -> flags |= IP_NO_ALIGN;
            #                }
            #                else
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #                break;
        #            case INIT_OFFS_Y:
        elif section == Section.INIT_OFFS_Y:
            writer.assert_mode(
                Mode.AS_INIT_WORLD_MAP,
                Mode.AS_INIT_IBS,
            )
            if writer.has_mode(Mode.AS_INIT_WORLD_MAP):
                writer.composite(
                    ('id', 'int32'),
                    ('ShapeOffsY', 'int32'),
                )
            elif writer.has_mode(Mode.AS_INIT_IBS):
                writer.composite(
                    ('id', 'int32'),
                    ('PosY', 'int32'),
                )
            #                if(curMode == AS_INIT_WORLD_MAP){
            # //                    t_id = script -> read_idata();
            #                    writer.intValue("t_id");
            # //                    wMap -> ShapeOffsY[t_id] = script -> read_idata();
            #                    writer.intValue("wMap.ShapeOffsY[$t_id]", "wMap -> ShapeOffsY[t_id] = script -> read_idata()");
            #                }
            #                else {
            #                    if(curMode == AS_INIT_IBS){
            # //                        t_id = script -> read_idata();
            #                        writer.intValue("t_id");
            # //                        ibsObj -> indPosY[t_id] = script -> read_idata();
            #                        writer.intValue("ibsObj.indPosY[$t_id]", "ibsObj -> indPosY[t_id]");
            #                    }
            #                    else
            #                        _handle_error("Misplaced option",aOptIDs[id]);
            #                }
            #                break;
        #            case NEW_WORLD_MAP:
        elif section == Section.NEW_WORLD_MAP:
            writer.assert_mode(
                Mode.AS_NONE,
            )
            writer.set_mode(Mode.AS_INIT_WORLD_MAP)
            #                if(curMode != AS_NONE)
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #
            # //                wMap = new aciWorldMap;
            #                curMode = AS_INIT_WORLD_MAP;
            #                writer.mode(curMode);
            #                break;
        #            case NEW_WORLD_DATA:
        elif section == Section.NEW_WORLD_DATA:
            writer.assert_mode(
                Mode.AS_INIT_WORLD_MAP,
            )
            writer.set_mode(Mode.AS_INIT_WORLD_DATA)
            writer.composite(
                ('id', 'int32'),
                ('letter', 'int32'),
                ('shape_id', 'int32'),
            )
            #                if(curMode != AS_INIT_WORLD_MAP)
            #                    _handle_error("Misplaced option",aOptIDs[id]);
            #
            # //                wData = new aciWorldInfo;
            # //                wData -> ID = script -> read_idata();
            #                writer.intValue("wData.ID");
            # //                wData -> letter = script -> read_idata();
            #                writer.intValue("wData.letter");
            # //                wData -> shape_id = script -> read_idata();
            #                writer.intValue("wData.shape_id");
            #                curMode = AS_INIT_WORLD_DATA;
            #                writer.mode(curMode);
            #                break;
        #            case TOGGLE_ISCREEN_MODE:
        elif section == Section.TOGGLE_ISCREEN_MODE:
            writer.flag("iScreenFlag")
            #                iScreenFlag = 1;
            #                break;
        #            case I_END_BLOCK:
        elif section == Section.I_END_BLOCK:
            writer.end_block()
            #                endBlock(writer);
            #                break;
    #            case INIT_CELL_SIZE:
    #                if(iScreenFlag){
    # //                    iCellSize = script -> read_idata();
    #                    writer.intValue("iCellSize");
    #                }
    #                else{
    # //                    aCellSize = script -> read_idata();
    #                    writer.intValue("aCellSize");
    #                }
    #                break;
    #            case NEW_INV_MATRIX:
    #                if(curMode != AS_NONE)
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    # //                invMat = new invMatrix;
    #                curMode = AS_INIT_MATRIX;
    #
    # //                invMat -> internalID = script -> read_idata();
    #                writer.intValue("invMat.internalID");
    # //                invMat -> type = script -> read_idata();
    #                writer.intValue("invMat.type");
    #                break;
    #            case NEW_INFO_PANEL:
    #                if(curMode != AS_NONE)
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    # //                iPl = new InfoPanel;
    #                curMode = AS_INIT_INFO_PANEL;
    #                writer.mode(curMode);
    #                break;
    #            case NEW_IBS:
    #                if(curMode != AS_NONE)
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    # //                ibsObj = new ibsObject;
    #                curMode = AS_INIT_IBS;
    #
    # //                ibsObj -> ID = script -> read_idata();
    #                writer.intValue("ibsObj.ID");
    #                break;
    #            case NEW_IND:
    #                if(curMode != AS_NONE)
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    # //                aInd = new aIndData;
    #                curMode = AS_INIT_IND;
    #
    # //                aInd -> ID = script -> read_idata();
    #                writer.intValue("aInd.ID");
    #                break;
    #            case NEW_BML:
    #                if(curMode != AS_NONE)
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    # //                bmlObj = new bmlObject;
    # //                bmlObj -> flags |= BMP_FLAG;
    #                curMode = AS_INIT_BML;
    #
    # //                bmlObj -> ID = script -> read_idata();
    #                writer.intValue("bmlObj.ID");
    #                break;
    #            case NEW_INV_ITEM:
    #                if(curMode != AS_NONE)
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    # //                invItm = new invItem;
    #                curMode = AS_INIT_ITEM;
    #                writer.bufValue("invItm.init_name(", " invItm -> init_name(script -> get_conv_ptr())");
    # //                script -> prepare_pdata();
    # //                invItm -> init_name(script -> get_conv_ptr());
    #                break;
    #            case NEW_COUNTER:
    #                if(curMode != AS_NONE)
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #
    # //                cP = new CounterPanel;
    # //                cP -> type = script -> read_option(0) - NEW_COUNTER - 1;
    #                writer.intValue("cP.type", "cP -> type = script -> read_option(0) - NEW_COUNTER - 1");
    #                curMode = AS_INIT_COUNTER;
    #                break;
    #            case NEW_BUTTON:
    #                if(curMode != AS_NONE)
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    # //                aBt = new aButton;
    #                writer.intValue("aBt.type", "aBt -> type = script -> read_option(0) - NEW_BUTTON - 1");
    # //                aBt -> type = script -> read_option(0) - NEW_BUTTON - 1;
    #
    #                curMode = AS_INIT_BUTTON;
    #                break;
    #            case NEW_MENU:
    #                if(curMode != AS_NONE && curMode != AS_INIT_ITEM)
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    # //                fnMnu = new fncMenu;
    #                fnMenuFlags = 0;
    #                if(curMode == AS_INIT_ITEM){
    # //                    fnMnu -> flags |= FM_ITEM_MENU;
    #                    fnMenuFlags |= FM_ITEM_MENU;
    #                }
    #                curMode = AS_INIT_MENU;
    #                break;
    #            case NEW_MENU_ITEM:
    #                if(curMode != AS_INIT_MENU)
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    # //                fnMnuItm = new fncMenuItem;
    #                curMode = AS_INIT_MENU_ITEM;
    #                break;
    #            case INIT_NUMVALS:
    #                if(curMode == AS_INIT_IND){
    #                    writer.intValue("aInd.NumVals");
    # //                    aInd -> NumVals = script -> read_idata();
    # //                    aInd -> alloc_mem();
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case INIT_X:
    #                if(curMode == AS_INIT_MATRIX){
    # //                    invMat -> ScreenX = script -> read_idata();
    #                    writer.intValue("invMat.ScreenX");
    #                }
    #                else {
    #                    if(curMode == AS_INIT_MENU){
    # //                        fnMnu -> PosX = script -> read_idata();
    #                        writer.intValue("fnMnu.PosX");
    #                    }
    #                    else {
    #                        if(curMode == AS_INIT_BUTTON){
    # //                            aBt -> PosX = script -> read_idata();
    #                            writer.intValue("aBt.PosX");
    #                        }
    #                        else {
    #                            if(curMode == AS_INIT_IND){
    # //                                aInd -> PosX = script -> read_idata();
    # //                                aInd -> dX = aInd -> PosX;
    #                                writer.intValue("aInd.PosX", "aInd -> dX = aInd -> PosX;");
    #                            }
    #                            else {
    #                                if(curMode == AS_INIT_INFO_PANEL){
    # //                                    iPl -> PosX = script -> read_idata();
    #                                    writer.intValue("iPl.PosX");
    #                                }
    #                                else {
    #                                    if(curMode == AS_INIT_COUNTER){
    # //                                        cP -> PosX = script -> read_idata();
    #                                        writer.intValue("cP.PosX");
    #                                    }
    #                                    else {
    #                                        if(curMode == AS_INIT_WORLD_DATA){
    # //                                            wData -> PosX = script -> read_idata();
    #                                            writer.intValue("wData.PosX");
    #                                        }
    #                                        else {
    #                                            if(curMode == BM_INIT_MENU_ITEM){
    # //                                                aciBM_it -> PosX = script -> read_idata();
    #                                                writer.intValue("aciBM_it.PosX");
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
    #                if(curMode == AS_INIT_MATRIX){
    # //                    invMat -> ScreenY = script -> read_idata();
    #                    writer.intValue("invMat.ScreenY");
    #                }
    #                else {
    #                    if(curMode == AS_INIT_MENU){
    # //                        fnMnu -> PosY = script -> read_idata();
    #                        writer.intValue("fnMnu.PosY");
    #                    }
    #                    else {
    #                        if(curMode == AS_INIT_BUTTON){
    # //                            aBt -> PosY = script -> read_idata();
    #                            writer.intValue("aBt.PosY");
    #                        }
    #                        else {
    #                            if(curMode == AS_INIT_IND){
    # //                                aInd -> PosY = script -> read_idata();
    # //                                aInd -> dY = aInd -> PosY;
    #                                writer.intValue("aInd.PosY", "aInd -> dY = aInd -> PosY");
    #                            }
    #                            else {
    #                                if(curMode == AS_INIT_INFO_PANEL){
    # //                                    iPl -> PosY = script -> read_idata();
    #                                    writer.intValue("iPl.PosY");
    #                                }
    #                                else {
    #                                    if(curMode == AS_INIT_COUNTER){
    # //                                        cP -> PosY = script -> read_idata();
    #                                        writer.intValue("cP.PosY");
    #                                    }
    #                                    else {
    #                                        if(curMode == AS_INIT_WORLD_DATA){
    # //                                            wData -> PosY = script -> read_idata();
    #                                            writer.intValue("wData.PosY");
    #                                        }
    #                                        else {
    #                                            if(curMode == BM_INIT_MENU_ITEM){
    # //                                                aciBM_it -> PosY = script -> read_idata();
    #                                                writer.intValue("aciBM_it.PosY");
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
    #                if(curMode == AS_INIT_MATRIX){
    # //                    invMat -> SizeX = script -> read_idata();
    #                    invMatSizeX =  writer.intValue("invMat.SizeX");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case SET_RAFFA_FLAG:
    #                if(curMode == AS_INIT_MATRIX){
    # //                    invMat -> flags |= IM_RAFFA;
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case SET_NUM_AVI_ID:
    #                if(curMode == AS_INIT_MATRIX){
    # //                    invMat -> numAviIDs = script -> read_idata();
    #                    writer.intValue("nvMat.numAviIDs");
    # //                    if(!invMat -> numAviIDs) _handle_error("Bad invMatrix::numAviIDs");
    # //                    invMat -> avi_ids = new char*[invMat -> numAviIDs];
    # //                    for(i = 0; i < invMat -> numAviIDs; i ++)
    # //                        invMat -> avi_ids[i] = NULL;
    #                }
    #                else {
    #                    if(curMode == AS_INIT_ITEM){
    # //                        invItm -> numAviIDs = script -> read_idata();
    #                        writer.intValue("invItm.numAviIDs");
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
    #                if(curMode == AS_INIT_ITEM){
    # //                    invItm -> flags |= INV_ITEM_SHOW_ESCAVE;
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case SET_SHOW_LOAD:
    #                if(curMode == AS_INIT_ITEM){
    # //                    invItm -> flags |= INV_ITEM_SHOW_LOAD;
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case SET_TEMPLATE:
    #                if(curMode == AS_INIT_ITEM){
    # //                    script -> prepare_pdata();
    # //                    if(strcasecmp(script -> get_conv_ptr(),"NONE"))
    # //                        invItm -> set_template(script -> get_conv_ptr());
    #                    writer.bufValue("invItm -> set_template(");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case SET_ACTIVATE_FLAG:
    #                if(curMode == AS_INIT_ITEM){
    # //                    invItm -> flags |= INV_ITEM_NO_ACTIVATE;
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_PART_DATA:
    #                if(curMode == AS_INIT_ITEM){
    # //                    invItm -> partData = new aciMechosPartInfo;
    #
    # //                    invItm -> partData -> baseID[0] = script -> read_idata();
    #                    writer.intValue("invItm.partData.baseID[0]");
    # //                    invItm -> partData -> targetID[0] = script -> read_idata();
    #                    writer.intValue("invItm.partData.targetID[0]");
    #
    # //                    invItm -> partData -> baseID[1] = script -> read_idata();
    #                    writer.intValue("invItm.partData.baseID[1]");
    # //                    invItm -> partData -> targetID[1] = script -> read_idata();
    #                    writer.intValue("invItm.partData.targetID[1]");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case SET_NO_SHOW_LOAD:
    #                if(curMode == AS_INIT_ITEM){
    # //                    invItm -> flags &= ~INV_ITEM_SHOW_LOAD;
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case SET_NOT_COMPLETED_FLAG:
    #                if(curMode == AS_INIT_MATRIX){
    # //                    invMat -> flags |= IM_NOT_COMPLETE;
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_MSY:
    #                if(curMode == AS_INIT_MATRIX){
    # //                    invMat -> SizeY = script -> read_idata();
    #                    invMatSizeY =writer.intValue("invMat.SizeY");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_RADIUS:
    #                if(curMode == AS_INIT_IND){
    # //                    script -> read_idata();
    #                    writer.intValue("__no_key__");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_CORNER:
    #                if(curMode == AS_INIT_IND){
    # //                    aInd -> CornerNum = script -> read_idata();
    #                    writer.intValue("aInd.CornerNum");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_IND_TYPE:
    #                if(curMode == AS_INIT_IND){
    # //                    aInd -> type = script -> read_idata();
    #                    writer.intValue("aInd.type");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_SX:
    #                if(curMode == AS_INIT_MATRIX){
    # //                    invMat -> ScreenSizeX = script -> read_idata();
    #                    writer.intValue("invMat.ScreenSizeX");
    #                }
    #                else {
    #                    if(curMode == AS_INIT_ITEM){
    # //                        t_id = script -> read_idata();
    #                        writer.intValue("t_id", " lpenguin: unused?");
    #                    }
    #                    else {
    #                        if(curMode == AS_INIT_MENU){
    # //                            fnMnu -> SizeX = script -> read_idata();
    #                            writer.intValue("fnMnu.SizeX");
    #                        }
    #                        else {
    #                            if(curMode == AS_INIT_BML){
    # //                                bmlObj -> SizeX = script -> read_idata();
    #                                writer.intValue("bmlObj.SizeX");
    #                            }
    #                            else {
    #                                if(curMode == AS_INIT_INFO_PANEL){
    # //                                    iPl -> SizeX = script -> read_idata();
    #                                    writer.intValue("iPl.SizeX");
    #                                }
    #                                else {
    #                                    if(curMode == AS_INIT_WORLD_MAP){
    # //                                        wMap -> SizeX = script -> read_idata();
    #                                        writer.intValue("wMap.SizeX");
    #                                    }
    #                                    else {
    #                                        if(curMode == AS_INIT_COUNTER){
    # //                                            cP -> SizeX = script -> read_idata();
    #                                            writer.intValue("cP.SizeX");
    #                                        }
    #                                        else {
    #                                            if(curMode == BM_INIT_MENU){
    # //                                                aciBM -> SizeX = script -> read_idata();
    #                                                writer.intValue("aciBM.SizeX");
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
    #                if(curMode == AS_INIT_MATRIX){
    # //                    invMat -> ScreenSizeY = script -> read_idata();
    #                    writer.intValue("invMat.ScreenSizeY");
    #                }
    #                else {
    #                    if(curMode == AS_INIT_ITEM){
    # //                        t_id = script -> read_idata();
    #                        writer.intValue("t_id", " lpenguin: unused?");
    #                    }
    #                    else {
    #                        if(curMode == AS_INIT_MENU){
    # //                            fnMnu -> SizeY = script -> read_idata();
    #                            writer.intValue("fnMnu.SizeX");
    #                        }
    #                        else {
    #                            if(curMode == AS_INIT_BML){
    # //                                bmlObj -> SizeY = script -> read_idata();
    #                                writer.intValue("bmlObj.SizeX");
    #                            }
    #                            else {
    #                                if(curMode == AS_INIT_INFO_PANEL){
    # //                                    iPl -> SizeY = script -> read_idata();
    #                                    writer.intValue("iPl.SizeX");
    #                                }
    #                                else {
    #                                    if(curMode == AS_INIT_WORLD_MAP){
    # //                                        wMap -> SizeY = script -> read_idata();
    #                                        writer.intValue("wMap.SizeX");
    #                                    }
    #                                    else {
    #                                        if(curMode == AS_INIT_COUNTER){
    # //                                            cP -> SizeY = script -> read_idata();
    #                                            writer.intValue("cP.SizeX");
    #                                        }
    #                                        else {
    #                                            if(curMode == BM_INIT_MENU){
    # //                                                aciBM -> SizeY = script -> read_idata();
    #                                                writer.intValue("aciBM.SizeX");
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
    #                if(curMode == AS_INIT_ITEM){
    # //                    invItm -> slotType = script -> read_idata();
    #                    writer.intValue("invItm.slotType");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_AVI_ID:
    #                if(curMode == AS_INIT_ITEM){
    # //                    if(!invItm -> numAviIDs) _handle_error("Null item numAviIDs...");
    # //                    t_id = script -> read_idata();
    #                    writer.intValue("t_id");
    # //                    if(t_id >= invItm -> numAviIDs || invItm -> avi_ids[t_id])
    # //                        _handle_error("Bad AVI_ID number");
    # //                    script -> prepare_pdata();
    # //                    invItm -> init_avi_id(script -> get_pdata_ptr(),t_id);
    #                    writer.bufValue("invItm.init_avi_id(${data}, ${id})", "invItm -> init_avi_id(script -> get_pdata_ptr(),t_id);");
    #                }
    #                else {
    #                    if(curMode == AS_INIT_MATRIX){
    # //                        if(!invMat -> numAviIDs) _handle_error("Null matrix numAviIDs...");
    # //                        t_id = script -> read_idata();
    #                        writer.intValue("t_id");
    # //                        if(t_id >= invMat -> numAviIDs || invMat -> avi_ids[t_id])
    # //                            _handle_error("Bad AVI_ID number");
    # //                        script -> prepare_pdata();
    # //                        invMat -> init_avi_id(script -> get_pdata_ptr(),t_id);
    #                        writer.bufValue("invMat.init_avi_id(${data}, ${id})", "invMat -> init_avi_id(script -> get_pdata_ptr(),t_id);");
    #                    }
    #                    else {
    #                        _handle_error("Misplaced option",aOptIDs[id]);
    #                    }
    #                }
    #                break;
    #            case INIT_COMMENTS:
    #                if(curMode == AS_INIT_ITEM){
    # //                    invItm -> numComments = script -> read_idata();
    #                    int n = writer.intValue("invItm.numComments");
    # //                    if(invItm -> numComments){
    #                    if(n){
    # //                        invItm -> comments = new char*[invItm -> numComments];
    # //                        for(i = 0; i < invItm -> numComments; i ++){
    # //                            script -> read_pdata(&invItm -> comments[i],1);
    # //                        }
    #                        for(i = 0; i < n; i++){
    #                            writer.strValue("invItm->comments[i]", "script -> read_pdata(&invItm -> comments[i],1);");
    #                        }
    #                    }
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_NUM_INDEX:
    #                if(curMode == AS_INIT_ITEM){
    # //                    invItm -> NumIndex = script -> read_idata();
    #                    writer.intValue("invItm.NumIndex");
    #                }
    #                else {
    #                    if(curMode == AS_INIT_LOC_DATA){
    # //                        t_id = script -> read_idata();
    #                        writer.intValue("t_id");
    # //                        if(t_id < 0 || t_id >= ACI_LOCATION_INDEX_SIZE)
    # //                            ErrH.Abort("Bad aciLocationInfo::numIndex ID...");
    # //                        locData -> numIndex[t_id] = script -> read_idata();
    #                        writer.intValue("locData.numIndex[$t_id]");
    #                    }
    #                    else
    #                        _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_SHAPE_LEN:
    #                if(curMode == AS_INIT_ITEM){
    # //                    invItm -> ShapeLen = script -> read_idata();
    #                    invItmShapeLen = writer.intValue("invItm.ShapeLen");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_SHAPE:
    #                if(curMode == AS_INIT_ITEM){
    #                    curMode = AS_INIT_SHAPE_OFFS;
    #                    load_item_shape(invItmShapeLen, writer);
    #                }
    #                else {
    #                    if(curMode == AS_INIT_WORLD_MAP){
    # //                        t_id = script -> read_idata();
    #                        writer.intValue("t_id");
    # //                        script -> read_pdata(&wMap -> shape_files[t_id],1);
    #                        writer.strValue("wMap.shape_files[${t_id}]");
    #                    }
    #                    else
    #                        _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_MATRIX_EL:
    #                if(curMode == AS_INIT_MATRIX){
    #                    curMode = AS_INIT_MATRIX_EL;
    #                    load_matrix(invMatSizeX, invMatSizeY, writer);
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_SLOT_NUMS:
    #                if(curMode == AS_INIT_MATRIX){
    #                    curMode = AS_INIT_MATRIX_EL;
    #                    load_slot_nums(invMatSizeX, invMatSizeY, writer);
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_SLOT_TYPES:
    #                if(curMode == AS_INIT_MATRIX){
    #                    curMode = AS_INIT_MATRIX_EL;
    #                    load_slot_types(invMatSizeX, invMatSizeY, writer);
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_CLASS:
    #                if(curMode == AS_INIT_ITEM){
    # //                    t_id = script -> read_option(0) - INIT_CLASS - 1;
    # //                    invItm -> classID = t_id;
    #                    writer.intValue("invItm.classID", "invItm -> classID script -> read_option(0) - INIT_CLASS - 1");
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case INIT_FNAME:
    #                if(curMode == AS_INIT_ITEM){
    # //                    script -> prepare_pdata();
    # //                    invItm -> init_fname(script -> get_conv_ptr());
    #                    writer.bufValue("invItm.init_fname(");
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case INIT_FILE:
    # //                script -> prepare_pdata();
    #                if(curMode == AS_INIT_IBS){
    # //                    ibsObj -> set_name(script -> get_conv_ptr());
    #                    writer.bufValue("bsObj.set_name(");
    #                }
    #                else {
    #                    if(curMode == AS_INIT_BML){
    # //                        bmlObj -> init_name(script -> get_conv_ptr());
    #                        writer.bufValue("bmlObj.init_name(");
    #                    }
    #                    else
    #                        _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_BGROUND:
    #                if(curMode == AS_INIT_IBS){
    # //                    ibsObj -> backObjID = script -> read_idata();
    #                    writer.intValue("ibsObj.backObjID");
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case INIT_SEQ_NAME:
    # //                script -> prepare_pdata();
    #                if(curMode == AS_INIT_BUTTON){
    # //                    aBt -> set_fname(script -> get_conv_ptr());
    #                    writer.bufValue("aBt.set_fname(");
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case SET_CONTROL_ID:
    #                if(curMode == AS_INIT_BUTTON){
    # //                    aBt -> ControlID = script -> read_idata();
    #                    writer.intValue("aBt.ControlID");
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case INIT_EVENT_CODE:
    #                if(curMode == AS_INIT_BUTTON){
    # //                    t_id = script -> read_idata();
    #                    writer.intValue("t_id");
    # //                    init_event_code(t_id);
    # //                    void init_event_code(int cd)
    # //                    {
    # //                        aBt -> eventCode = cd + ACI_MAX_EVENT;
    # //                        aBt -> eventData = script -> read_idata();
    #                    writer.intValue("aBt.eventData");
    # //                    }
    #                }
    #                else {
    #                    if(curMode == AS_INIT_ITEM){
    # //                        invItm -> EvCode = script -> read_idata() + ACI_MAX_EVENT;
    #                        writer.intValue("invItm.EvCode", "invItm -> EvCode = script -> read_idata() + ACI_MAX_EVENT");
    #                    }
    #                    else {
    #                        if(curMode == AS_INIT_MENU_ITEM){
    # //                            fnMnuItm -> eventPtr = new actEvent;
    # //                            fnMnuItm -> eventPtr -> code = script -> read_idata() + ACI_MAX_EVENT;
    #                            writer.intValue("fnMnuItm.eventPtr.code", "fnMnuItm -> eventPtr -> code = script -> read_idata() + ACI_MAX_EVENT;");
    # //                            fnMnuItm -> eventPtr -> data = script -> read_idata();
    #                            writer.intValue("fnMnuItm.eventPtr.data");
    #                        }
    #                        else
    #                            _handle_error("Misplaced option",aOptIDs[id]);
    #                    }
    #                }
    #                break;
    #            case SET_UNPRESS:
    #                if(curMode == AS_INIT_BUTTON){
    # //                    aBt -> flags |= B_UNPRESS;
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case INIT_ACTIVE_TIME:
    #                if(curMode == AS_INIT_BUTTON){
    # //                    aBt -> activeCount = script -> read_idata();
    #                    writer.intValue("aBt.activeCount");
    #                }
    #                else {
    #                    if(curMode == AS_INIT_MENU){
    # //                        fnMnu -> activeCount = script -> read_idata();
    #                        writer.intValue("fnMnu.activeCount");
    #                    }
    #                    else {
    #                        if(curMode == AML_INIT_EVENT){
    # //                            mlEv -> active_time = script -> read_idata();
    #                            writer.intValue("mlEv.active_time");
    #                        }
    #                        else {
    #                            if(curMode == BM_INIT_MENU){
    # //                                aciBM -> activeCount = script -> read_idata();
    #                                writer.intValue("aciBM.activeCount");
    #                            }
    #                            else
    #                                _handle_error("Misplaced option",aOptIDs[id]);
    #                        }
    #                    }
    #                }
    #                break;
    #            case INIT_FNC_CODE:
    #                if(curMode == AS_INIT_MENU_ITEM){
    # //                    fnMnuItm -> fnc_code = script -> read_idata();
    #                    writer.intValue("fnMnuItm.fnc_code");
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case SET_NO_DELETE_FLAG:
    #                if(curMode == AS_INIT_MENU_ITEM){
    # //                    fnMnuItm -> flags |= FM_NO_DELETE;
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case SET_SUBMENU_ID:
    #                if(curMode == AS_INIT_MENU_ITEM){
    # //                    fnMnuItm -> submenuID = script -> read_idata();
    #                    writer.intValue("fnMnuItm.submenuID");
    # //                    fnMnuItm -> flags |= FM_SUBMENU_ITEM;
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case SET_BSUBMENU_ID:
    #                if(curMode == AS_INIT_MENU_ITEM){
    # //                    fnMnuItm -> submenuID = script -> read_idata();
    #                    writer.intValue("fnMnuItm.submenuID");
    # //                    fnMnuItm -> flags |= FM_BSUBMENU_ITEM;
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case SET_NUM_V_ITEMS:
    #                if(curMode == AS_INIT_MENU){
    # //                    fnMnu -> VItems = script -> read_idata();
    #                    writer.intValue("fnMnu.VItems");
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case INIT_SPACE:
    #                if(curMode == AS_INIT_MENU){
    # //                    fnMnu -> vSpace = script -> read_idata();
    #                    writer.intValue("fnMnu.vSpace");
    #                }
    #                else {
    #                    if(curMode == AS_INIT_MENU_ITEM){
    # //                        fnMnuItm -> space = script -> read_idata();
    #                        writer.intValue("fnMnuItm.vSpace");
    #                    }
    #                    else
    #                        _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case SET_NO_DEACTIVATE_FLAG:
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
    #                if(curMode == AS_INIT_MENU){
    # //                    fnMnu -> flags |= FM_LOCATION_MENU;
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case SET_BML_NAME:
    #                if(curMode == AS_INIT_MENU){
    # //                    script -> read_pdata(&fnMnu -> bml_name,1);
    #                    writer.strValue("fnMnu.bml_name");
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
    #                        writer.bufValue("aInd.bml.init_name(");
    #                    }
    #                    else {
    #                        if(curMode == AS_INIT_INFO_PANEL){
    # //                            script -> read_pdata(&iPl -> bml_name,1);
    #                            writer.strValue("iPl.bml_name");
    #                        }
    #                        else {
    #                            if(curMode == BM_INIT_MENU_ITEM){
    # //                                script -> read_pdata(&aciBM_it -> fname,1);
    #                                writer.strValue("aciBM_it.fname");
    #                            }
    #                            else
    #                                _handle_error("Misplaced option",aOptIDs[id]);
    #                        }
    #                    }
    #                }
    #                break;
    #            case INIT_BACK_BML:
    #                if(curMode == AS_INIT_MATRIX){
    # //                    script -> prepare_pdata();
    # //
    # //                    if(invMat -> back)
    # //                        _handle_error("invMatrix::back already inited");
    # //
    # //                    invMat -> back = new bmlObject;
    # //                    invMat -> back -> init_name(script -> get_conv_ptr());
    #                    writer.bufValue("invMat.back.init_name(");
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case SET_IBS_NAME:
    #                if(curMode == AS_INIT_MENU){
    # //                    script -> read_pdata(&fnMnu -> ibs_name,1);
    #                    writer.strValue("fnMnu.ibs_name");
    #                }
    #                else {
    #                    if(curMode == AS_INIT_INFO_PANEL){
    # //                        script -> read_pdata(&iPl -> ibs_name,1);
    #                        writer.strValue("iPl.ibs_name");
    #                    }
    #                    else {
    #                        if(curMode == AS_INIT_COUNTER){
    # //                            script -> read_pdata(&cP -> ibs_name,1);
    #                            writer.strValue("cP.ibs_name");
    #                        }
    #                        else
    #                            _handle_error("Misplaced option",aOptIDs[id]);
    #                    }
    #                }
    #                break;
    #            case SET_MAP_NAME:
    #                if(curMode == AS_INIT_LOC_DATA){
    # //                    script -> read_pdata(&locData -> mapName,1);
    #                    writer.strValue("locData.mapName");
    #                }
    #                else {
    # //                    t_id = script -> read_idata();
    #                    writer.intValue("t_id");
    # //                    script -> read_pdata(&aScrDisp -> map_names[t_id],1);
    #                    writer.strValue("aScrDisp.map_names[$t_id]");
    #                }
    #                break;
    #            case SET_SAVE_SCREEN_ID:
    #                if(curMode == AS_INIT_LOC_DATA){
    # //                    locData -> SaveScreenID = script -> read_idata();
    #                    writer.intValue("locData.SaveScreenID");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case SET_WORLD_ID:
    #                if(curMode == AS_INIT_LOC_DATA){
    # //                    locData -> WorldID = script -> read_idata();
    #                    writer.intValue("locData.WorldID");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case SET_EXCLUDE:
    #                if(curMode == AS_INIT_LOC_DATA){
    # //                    t_id = script -> read_idata();
    #                    writer.intValue("t_id", "locData -> ExcludeItems[t_id] = 1;");
    # //                    locData -> ExcludeItems[t_id] = 1;
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_SCREEN_ID:
    #                if(curMode == AS_INIT_LOC_DATA){
    # //                    script -> read_pdata(&locData -> screenID,1);
    #                    writer.strValue("locData.screenID");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_PAL_NAME:
    #                if(curMode == AS_INIT_LOC_DATA){
    # //                    script -> read_pdata(&locData -> palName,1);
    #                    writer.strValue("locData.palName");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_CUR_FNC:
    #                if(curMode == AS_INIT_MENU){
    # //                    fnMnu -> curFunction = script -> read_idata();
    #                    writer.intValue("fnMnu.curFunction");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_FONT:
    #                if(curMode == AS_INIT_MENU_ITEM){
    # //                    fnMnuItm -> font = script -> read_idata();
    #                    writer.intValue("fnMnuItm.font");
    #                }
    #                else {
    #                    if(curMode == AS_INIT_INFO_PANEL){
    # //                        iPl -> font = script -> read_idata();
    #                        writer.intValue("iPl.font");
    #                    }
    #                    else {
    #                        if(curMode == AS_INIT_WORLD_DATA){
    # //                            wData -> font = script -> read_idata();
    #                            writer.intValue("wData.font");
    #                        }
    #                        else {
    #                            if(curMode == AS_INIT_COUNTER){
    # //                                cP -> font = script -> read_idata();
    #                                writer.intValue("cP.font");
    #                            }
    #                            else {
    #                                if(curMode == AS_INIT_IBS){
    # //                                    ibsObj -> fontID = script -> read_idata();
    #                                    writer.intValue("ibsObj.font");
    #                                }
    #                                else
    #                                    _handle_error("Misplaced option",aOptIDs[id]);
    #                            }
    #                        }
    #                    }
    #                }
    #                break;
    #            case INIT_VSPACE:
    #                if(curMode == AS_INIT_INFO_PANEL){
    # //                    iPl -> vSpace = script -> read_idata();
    #                    writer.intValue("iPl.vSpace");
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case INIT_HSPACE:
    #                if(curMode == AS_INIT_INFO_PANEL){
    # //                    iPl -> hSpace = script -> read_idata();
    #                    writer.intValue("iPl.hSpace");
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case INIT_STRING:
    #                if(curMode == AS_INIT_MENU_ITEM){
    # //                    script -> prepare_pdata();
    # //                    fnMnuItm -> init_name(script -> get_conv_ptr());
    #                    writer.bufValue("fnMnuItm.init_name(");
    #                }
    #                else
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                break;
    #            case INIT_SCANCODE:
    #                if(curMode == AS_INIT_MENU){
    # //                    fnMnu -> add_key(script -> read_key());
    #                    writer.intValue("fnMnu.add_key(");
    #                }
    #                else {
    #                    if(curMode == AS_INIT_MENU_ITEM){
    # //                        fnMnuItm -> add_key(script -> read_key());
    #                        writer.intValue("fnMnuItm.add_key(");
    #                    }
    #                    else {
    #                        if(curMode == AS_INIT_BUTTON){
    # //                            aBt -> add_key(script -> read_key());
    #                            writer.intValue("aBt.add_key(");
    #                        }
    #                        else {
    #                            if(curMode == AML_INIT_EVENT){
    # //                                mlEv -> add_key(script -> read_key());
    #                                writer.intValue("mlEv.add_key(");
    #                            }
    #                            else
    #                                _handle_error("Misplaced option",aOptIDs[id]);
    #                        }
    #                    }
    #                }
    #                break;
    #            case INIT_MENU_TYPE:
    #                if(curMode == AS_INIT_MENU){
    # //                    fnMnu -> type = script -> read_idata();
    #                    writer.intValue("fnMnu.type");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_UP_KEY:
    #                if(curMode == AS_INIT_MENU){
    # //                    fnMnu -> up_key -> add_key(script -> read_key());
    #                    writer.intValue("fnMnu.up_key.add_key(");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_DOWN_KEY:
    #                if(curMode == AS_INIT_MENU){
    # //                    fnMnu -> down_key -> add_key(script -> read_key());
    #                    writer.intValue("fnMnu.down_key.add_key(");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_TRIGGER:
    #                if(curMode == AS_INIT_MENU){
    # //                    fnMnu -> trigger_code = script -> read_idata();
    #                    writer.intValue("fnMnu.trigger_code");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_ID:
    #                if(curMode == AS_INIT_BUTTON){
    # //                    aBt -> ID = script -> read_idata();
    #                    writer.intValue("aBt.ID");
    #                }
    #                else {
    #                    if(curMode == AS_INIT_ITEM){
    # //                        invItm -> ID = script -> read_idata();
    #                        writer.intValue("invItm.ID");
    #                    }
    #                    else {
    #                        if(curMode == AS_INIT_LOC_DATA){
    # //                            t_id = script -> read_idata();
    #                            writer.intValue("t_id");
    # //                            script -> read_pdata(&locData -> objIDs[t_id],1);
    #                            writer.strValue("locData.objIDs[${t_id}]");
    #                        }
    #                        else {
    #                            if(curMode == AS_INIT_MATRIX){
    # //                                script -> read_pdata(&invMat -> mech_name,1);
    #                                writer.strValue("invMat.mech_name");
    #                            }
    #                            else {
    #                                if(curMode == AS_INIT_INFO_PANEL){
    # //                                    iPl -> type = script -> read_idata();
    #                                    writer.intValue("iPl.type");
    #                                }
    #                                else {
    #                                    if(curMode == AS_INIT_COUNTER){
    # //                                        cP -> ID = script -> read_idata();
    #                                        writer.intValue("cP.ID");
    #                                    }
    #                                    else {
    #                                        if(curMode == AML_INIT_DATA_SET){
    # //                                            mlDataSet -> ID = script -> read_idata();
    #                                            writer.intValue("mlDataSet.ID");
    #                                        }
    #                                        else {
    #                                            if(curMode == AML_INIT_DATA){
    # //                                                mlData -> ID = script -> read_idata();
    #                                                writer.intValue("mlData.ID");
    #                                            }
    #                                            else {
    #                                                if(curMode == BM_INIT_MENU_ITEM){
    # //                                                    aciBM_it -> ID = script -> read_idata();
    #                                                    writer.intValue("aciBM_it.ID");
    #                                                }
    #                                                else {
    #                                                    if(curMode == BM_INIT_MENU){
    # //                                                        aciBM -> ID = script -> read_idata();
    #                                                        writer.intValue("aciBM.ID");
    #                                                    }
    #                                                    else {
    #                                                        if(curMode == AML_INIT_EVENT_SEQ){
    # //                                                            mlEvSeq -> add_id(script -> read_idata());
    #                                                            writer.intValue("mlEvSeq.add_id(");
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
    #                if(curMode == AS_INIT_LOC_DATA){
    # //                    t_id = script -> read_idata();
    #                    writer.intValue("t_id");
    # //                    script -> read_pdata(&locData -> s_objIDs[t_id],1);
    #                    writer.strValue("locData.s_objIDs[$t_id]");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #            case INIT_MODE_KEY:
    # //                aScrDisp -> ModeObj -> add_key(script -> read_key());
    #                writer.intValue("aScrDisp.ModeObj.add_key");
    #                break;
    #            case INIT_INV_KEY:
    # //                aScrDisp -> InvObj -> add_key(script -> read_key());
    #                writer.intValue("aScrDisp.InvObj.add_key");
    #                break;
    #            case INIT_INFO_KEY:
    # //                aScrDisp -> InfoObj -> add_key(script -> read_key());
    #                writer.intValue("aScrDisp.InfoObj.add_key");
    #                break;
    #            case SET_CURMATRIX:
    # //                curMatrix = script -> read_idata();
    #                writer.intValue("curMatrix");
    #                break;
    #            case INIT_CUR_IBS:
    # //                aScrDisp -> curIbsID = script -> read_idata();
    #                writer.intValue("aScrDisp.curIbsID");
    #                break;
    #            case NEW_LOC_DATA:
    # //                if(curMode != AS_NONE){
    # //                    _handle_error("Misplaced option",aOptIDs[id]);
    # //                }
    # //                locData = new aciLocationInfo;
    # //                locData -> ID = script -> read_idata();
    #                writer.intValue("locData.ID");
    #                curMode = AS_INIT_LOC_DATA;
    #                writer.mode(curMode);
    #                break;
    #            case NEW_COL_SCHEME:
    #                if(curMode != AS_NONE){
    #                    if(curMode == AS_INIT_LOC_DATA){
    # //                        locData -> numColorScheme = script -> read_idata();
    #                        writer.intValue("locData.numColorScheme");
    #                    }
    #                    else
    #                        _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                curMode = AS_INIT_COLOR_SCHEME;
    #                writer.mode(curMode);
    # //                t_id = script -> read_idata();
    #                writer.intValue("curScheme", "aciColorSchemes[t_id] = new unsigned char[aciColSchemeLen]; memset(aciColorSchemes[t_id],0,aciColSchemeLen)");
    # //                curScheme = t_id;
    # //                aciColorSchemes[t_id] = new unsigned char[aciColSchemeLen];
    # //                memset(aciColorSchemes[t_id],0,aciColSchemeLen);
    #                break;
    #            case INIT_NUM_SCHEMES:
    # //                aciNumColSchemes = script -> read_idata();
    #                writer.intValue("aciNumColSchemes");
    # //                aciColorSchemes = new unsigned char*[aciNumColSchemes];
    # //                for(i = 0; i < aciNumColSchemes; i ++)
    # //                    aciColorSchemes[i] = NULL;
    #                break;
    #            case INIT_SCHEME_LEN:
    # //                aciColSchemeLen = script -> read_idata();
    #                writer.intValue("aciColSchemeLen");
    #                break;
    #            case INIT_COLOR:
    #                if(curMode == AS_INIT_COLOR_SCHEME){
    # //                    t_id = script -> read_idata();
    #                    writer.intValue("t_id");
    # //                    aciColorSchemes[curScheme][t_id] = script -> read_idata();
    #                    writer.intValue("aciColorSchemes[curScheme][${t_id}]");
    #                }
    #                else {
    #                    _handle_error("Misplaced option",aOptIDs[id]);
    #                }
    #                break;
    #        }
    pass
