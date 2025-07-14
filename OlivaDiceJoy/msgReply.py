# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgReply.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceJoy
import OlivaDiceCore

import hashlib
import time
import traceback
from functools import wraps
import copy

def unity_init(plugin_event, Proc):
    pass

def data_init(plugin_event, Proc):
    OlivaDiceJoy.msgCustomManager.initMsgCustom(Proc.Proc_data['bot_info_dict'])
    OlivaDiceCore.crossHook.dictHookFunc['pokeHook'] = add_poke_rd_func(OlivaDiceCore.crossHook.dictHookFunc['pokeHook'])
    OlivaDiceCore.crossHook.dictHookFunc['msgFormatHook'] = add_chance_custom_msg_func(OlivaDiceCore.crossHook.dictHookFunc['msgFormatHook'])
    OlivaDiceCore.crossHook.dictHookFunc['drawFormatHook'] = add_chance_custom_to_deck_func(OlivaDiceCore.crossHook.dictHookFunc['drawFormatHook'])

def add_poke_rd_func(target_func):
    @wraps(target_func)
    def poke_rd_func(plugin_event, type):
        flag_need = OlivaDiceCore.console.getConsoleSwitchByHash(
            'joyPokeMode',
            plugin_event.bot_info.hash
        )
        if flag_need == 1:
            res = poke_rd(plugin_event, type)
        elif flag_need == 2:
            res = poke_jrrp(plugin_event, type)
        elif flag_need == 3:
            res = ""
        else:
            res = target_func(plugin_event, type)
        return res
    return poke_rd_func

def poke_jrrp(plugin_event, type):
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictTValue['tName'] = '你'
    tmp_pcName = None
    tmp_plName = None
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)
    dictTValue = OlivaDiceCore.msgCustomManager.dictTValueInit(plugin_event, dictTValue)
    tmp_pc_id = plugin_event.data.user_id
    tmp_pc_platform = plugin_event.platform['platform']
    if tmp_pcName == None:
        tmp_userHash = OlivaDiceCore.userConfig.getUserHash(
            userId = tmp_pc_id,
            userType = 'user',
            platform = tmp_pc_platform
        )
        tmp_userId = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
            userHash = tmp_userHash,
            userDataKey = 'userId',
            botHash = plugin_event.bot_info.hash
        )
        if tmp_userId != None:
            tmp_pcName = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                userHash = tmp_userHash,
                userConfigKey = 'userName',
                botHash = plugin_event.bot_info.hash
            )
    res = plugin_event.get_stranger_info(user_id = plugin_event.data.user_id)
    if res != None:
        if tmp_pcName == None:
            tmp_pcName = res['data']['name']
        tmp_plName = res['data']['name']
    dictTValue['tUserName'] = tmp_plName if tmp_plName else tmp_pc_id
    if tmp_pcName != None:
        dictTValue['tName'] = tmp_pcName
        hash_tmp = hashlib.new('md5')
        hash_tmp.update(str(time.strftime('%Y-%m-%d', time.localtime())).encode(encoding='UTF-8'))
        hash_tmp.update(str(plugin_event.data.user_id).encode(encoding='UTF-8'))
        tmp_jrrp_int = int(int(hash_tmp.hexdigest(), 16) % 100) + 1
        dictTValue['tJrrpResult'] = str(tmp_jrrp_int)
        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strJoyJrrp'], dictTValue)
    return tmp_reply_str

def poke_rd(plugin_event, event_type):
    tmp_group_id = None
    if 'group_id' in plugin_event.data.__dict__:
        tmp_group_id = plugin_event.data.group_id
    tmp_user_platform = plugin_event.platform['platform']
    tmp_hagID = None
    if event_type == 'group':
        if tmp_group_id == -1:
            tmp_hagID = None
        elif tmp_group_id == None:
            tmp_hagID = None
        elif type(tmp_group_id) == str:
            tmp_hagID = tmp_group_id
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictTValue['tName'] = '你'
    tmp_pcName = None
    tmp_plName = None
    rd_para_str = '1D100'
    tmp_template_customDefault = None
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)
    dictTValue = OlivaDiceCore.msgCustomManager.dictTValueInit(plugin_event, dictTValue)
    tmp_pc_id = plugin_event.data.user_id
    tmp_pc_platform = plugin_event.platform['platform']
    tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
        tmp_pc_id,
        tmp_pc_platform
    )
    skill_valueTable = OlivaDiceCore.pcCard.pcCardDataGetByPcName(tmp_pcHash, hagId = tmp_hagID)
    tmp_pcName = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash, hagId = tmp_hagID)
    if tmp_pcName != None:
        tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pcName)
        tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
        if tmp_template != None:
            if 'customDefault' in tmp_template:
                tmp_template_customDefault = tmp_template['customDefault']
            if 'mainDice' in tmp_template:
                rd_para_str = tmp_template['mainDice']
    rd_para_main_str = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = tmp_user_platform,
        userConfigKey = 'groupMainDice',
        botHash = plugin_event.bot_info.hash
    )
    rd_para_main_D_right = OlivaDiceCore.userConfig.getUserConfigByKey(
        userId = tmp_hagID,
        userType = 'group',
        platform = tmp_user_platform,
        userConfigKey = 'groupMainDiceDRight',
        botHash = plugin_event.bot_info.hash
    )
    if rd_para_main_str != None:
        rd_para_str = rd_para_main_str
    tmp_template_customDefault = copy.deepcopy(tmp_template_customDefault)
    if type(rd_para_main_D_right) == int:
        if type(tmp_template_customDefault) != dict:
            tmp_template_customDefault = {}
            if 'd' not in tmp_template_customDefault:
                tmp_template_customDefault['d'] = {}
        tmp_template_customDefault['d']['rightD'] = rd_para_main_D_right
    rd = OlivaDiceCore.onedice.RD(rd_para_str, tmp_template_customDefault, valueTable = skill_valueTable)
    rd.roll()
    if tmp_pcName == None:
        tmp_userHash = OlivaDiceCore.userConfig.getUserHash(
            userId = tmp_pc_id,
            userType = 'user',
            platform = tmp_pc_platform
        )
        tmp_userId = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
            userHash = tmp_userHash,
            userDataKey = 'userId',
            botHash = plugin_event.bot_info.hash
        )
        if tmp_userId != None:
            tmp_pcName = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                userHash = tmp_userHash,
                userConfigKey = 'userName',
                botHash = plugin_event.bot_info.hash
            )
    res = plugin_event.get_stranger_info(user_id = plugin_event.data.user_id)
    if res != None:
        if tmp_pcName == None:
            tmp_pcName = res['data']['name']
        tmp_plName = res['data']['name']
    if tmp_pcName != None:
        dictTValue['tName'] = tmp_pcName
    dictTValue['tUserName'] = tmp_plName if tmp_plName else tmp_pc_id
    dictTValue['tRollResult'] = '%s=%s' % (rd_para_str, str(rd.resInt))
    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strRoll'], dictTValue)
    return tmp_reply_str

def unity_reply(plugin_event, Proc):
    OlivaDiceCore.userConfig.setMsgCount()
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictTValue['tUserName'] = plugin_event.data.sender['name']
    dictTValue['tName'] = plugin_event.data.sender['name']
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)
    dictTValue = OlivaDiceCore.msgCustomManager.dictTValueInit(plugin_event, dictTValue)

    replyMsg = OlivaDiceCore.msgReply.replyMsg
    isMatchWordStart = OlivaDiceCore.msgReply.isMatchWordStart
    getMatchWordStartRight = OlivaDiceCore.msgReply.getMatchWordStartRight
    skipSpaceStart = OlivaDiceCore.msgReply.skipSpaceStart
    skipToRight = OlivaDiceCore.msgReply.skipToRight
    msgIsCommand = OlivaDiceCore.msgReply.msgIsCommand

    tmp_at_str = OlivOS.messageAPI.PARA.at(plugin_event.base_info['self_id']).CQ()
    tmp_at_str_sub = None
    if 'sub_self_id' in plugin_event.data.extend:
        if plugin_event.data.extend['sub_self_id'] != None:
            tmp_at_str_sub = OlivOS.messageAPI.PARA.at(plugin_event.data.extend['sub_self_id']).CQ()
    tmp_command_str_1 = '.'
    tmp_command_str_2 = '。'
    tmp_command_str_3 = '/'
    tmp_reast_str = plugin_event.data.message
    flag_force_reply = False
    flag_is_command = False
    flag_is_from_host = False
    flag_is_from_group = False
    flag_is_from_group_admin = False
    flag_is_from_group_have_admin = False
    flag_is_from_master = False
    if isMatchWordStart(tmp_reast_str, '[CQ:reply,id='):
        tmp_reast_str = skipToRight(tmp_reast_str, ']')
        tmp_reast_str = tmp_reast_str[1:]
        if isMatchWordStart(tmp_reast_str, tmp_at_str):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str)
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            flag_force_reply = True
    if isMatchWordStart(tmp_reast_str, tmp_at_str):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str)
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        flag_force_reply = True
    if tmp_at_str_sub != None:
        if isMatchWordStart(tmp_reast_str, tmp_at_str_sub):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str_sub)
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            flag_force_reply = True
    [tmp_reast_str, flag_is_command] = msgIsCommand(
        tmp_reast_str,
        OlivaDiceCore.crossHook.dictHookList['prefix']
    )
    if flag_is_command:
        tmp_hagID = None
        if plugin_event.plugin_info['func_type'] == 'group_message':
            if plugin_event.data.host_id != None:
                flag_is_from_host = True
            flag_is_from_group = True
        elif plugin_event.plugin_info['func_type'] == 'private_message':
            flag_is_from_group = False
        if flag_is_from_group:
            if 'role' in plugin_event.data.sender:
                flag_is_from_group_have_admin = True
                if plugin_event.data.sender['role'] in ['owner', 'admin']:
                    flag_is_from_group_admin = True
                elif plugin_event.data.sender['role'] in ['sub_admin']:
                    flag_is_from_group_admin = True
                    flag_is_from_group_sub_admin = True
        if flag_is_from_host and flag_is_from_group:
            tmp_hagID = '%s|%s' % (str(plugin_event.data.host_id), str(plugin_event.data.group_id))
        elif flag_is_from_group:
            tmp_hagID = str(plugin_event.data.group_id)
        flag_hostEnable = True
        if flag_is_from_host:
            flag_hostEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = plugin_event.data.host_id,
                userType = 'host',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'hostEnable',
                botHash = plugin_event.bot_info.hash
            )
        flag_hostLocalEnable = True
        if flag_is_from_host:
            flag_hostLocalEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = plugin_event.data.host_id,
                userType = 'host',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'hostLocalEnable',
                botHash = plugin_event.bot_info.hash
            )
        flag_groupEnable = True
        if flag_is_from_group:
            if flag_is_from_host:
                if flag_hostEnable:
                    flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupEnable',
                        botHash = plugin_event.bot_info.hash
                    )
                else:
                    flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupWithHostEnable',
                        botHash = plugin_event.bot_info.hash
                    )
            else:
                flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = plugin_event.platform['platform'],
                    userConfigKey = 'groupEnable',
                    botHash = plugin_event.bot_info.hash
                )
        #此频道关闭时中断处理
        if not flag_hostLocalEnable and not flag_force_reply:
            return
        #此群关闭时中断处理
        if not flag_groupEnable and not flag_force_reply:
            return
        if isMatchWordStart(tmp_reast_str, 'jrrp', isCommand = True):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'jrrp')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            tmp_reply_str = None
            hash_tmp = hashlib.new('md5')
            hash_tmp.update(str(time.strftime('%Y-%m-%d', time.localtime())).encode(encoding='UTF-8'))
            hash_tmp.update(str(plugin_event.data.user_id).encode(encoding='UTF-8'))
            tmp_jrrp_int = int(int(hash_tmp.hexdigest(), 16) % 100) + 1
            dictTValue['tJrrpResult'] = str(tmp_jrrp_int)
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strJoyJrrp'], dictTValue)
            if tmp_reply_str != None:
                replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'zrrp', isCommand = True):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'zrrp')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            tmp_reply_str = None
            hash_tmp = hashlib.new('md5')
            hash_tmp.update(str(time.strftime('%Y-%m-%d', time.localtime(int(time.mktime(time.localtime())) - 24 * 60 * 60))).encode(encoding='UTF-8'))
            hash_tmp.update(str(plugin_event.data.user_id).encode(encoding='UTF-8'))
            tmp_jrrp_int = int(int(hash_tmp.hexdigest(), 16) % 100) + 1
            dictTValue['tJrrpResult'] = str(tmp_jrrp_int)
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strJoyZrrp'], dictTValue)
            if tmp_reply_str != None:
                replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'mrrp', isCommand = True):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'mrrp')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            tmp_reply_str = None
            hash_tmp = hashlib.new('md5')
            hash_tmp.update(str(time.strftime('%Y-%m-%d', time.localtime(int(time.mktime(time.localtime())) + 24 * 60 * 60))).encode(encoding='UTF-8'))
            hash_tmp.update(str(plugin_event.data.user_id).encode(encoding='UTF-8'))
            tmp_jrrp_int = int(int(hash_tmp.hexdigest(), 16) % 100) + 1
            dictTValue['tJrrpResult'] = str(tmp_jrrp_int)
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strJoyMrrp'], dictTValue)
            if tmp_reply_str != None:
                replyMsg(plugin_event, tmp_reply_str)
            return

def add_chance_custom_msg_func(target_func):
    @wraps(target_func)
    def msg_func(data:str, valDict:dict):
        bot_hash = None
        plugin_event = None
        if 'tBotHash' in valDict:
            bot_hash = valDict['tBotHash']
        if 'vValDict' in valDict:
            if 'vPluginEvent' in valDict['vValDict']:
                plugin_event = valDict['vValDict']['vPluginEvent']
        flag_need = OlivaDiceCore.console.getConsoleSwitchByHash(
            'joyEnableCCPK',
            bot_hash
        )
        if flag_need == 1 and plugin_event != None:
            res = chance_custom_msg(plugin_event, data)
        else:
            res = target_func(data, valDict)
        return res
    return msg_func

def add_chance_custom_to_deck_func(target_func):
    @wraps(target_func)
    def msg_func(data:str, plugin_event:OlivOS.API.Event):
        bot_hash = plugin_event.bot_info.hash
        res = data
        for key_this in ['【程心】', '【铃心】', '【EPK】', '【CCPK】']:
            if res.startswith('%s::' % key_this) or res.startswith('::%s::' % key_this):
                if res.startswith('::'):
                    res = res[len('::'):]
                if res.startswith('%s::' % key_this):
                    res = res[len('%s::' % key_this):]
                res = chance_custom_msg(plugin_event, res)
                break
        return res
    return msg_func

def chance_custom_msg(plugin_event:OlivOS.API.Event, data:str):
    msg = data
    if 'ChanceCustom' in OlivaDiceJoy.data.listPlugin:
        import ChanceCustom
        chance_valDict = {}
        event_name = None
        if type(plugin_event.data) == OlivOS.API.Event.group_message:
            event_name = 'group_message'
        elif type(plugin_event.data) == OlivOS.API.Event.private_message:
            event_name = 'private_message'
        elif type(plugin_event.data) == OlivOS.API.Event.poke:
            if plugin_event.data.group_id in [-1, None]:
                event_name = 'poke_private'
            else:
                event_name = 'poke_group'
        if event_name != None:
            ChanceCustom.replyCore.getValDict(chance_valDict, plugin_event, OlivaDiceJoy.data.globalProc, event_name)
            chance_valDict['innerVal']['bot_hash'] = plugin_event.bot_info.hash
            chance_valDict['innerVal']['bot_hash_self'] = plugin_event.bot_info.hash
            try:
                msg_1 = data
                msg_1 = msg_1.replace('\r\n', '\n')
                msg_1 = msg_1.replace('\n', '【换行】')
                msg = ChanceCustom.replyReg.replyValueRegTotal(
                    msg_1,
                    chance_valDict
                )
            except:
                msg = data
                OlivaDiceJoy.data.globalProc.log(3, traceback.format_exc(), [
                    ('OlivaDice', 'default'),
                    ('joyCCPK', 'default')
                ])
    return msg
