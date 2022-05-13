# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgCustom.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore
import OlivaDiceJoy

dictConsoleSwitchTemplate = {
    'default' : {
        'joyPokeMode': 0
    }
}

dictStrCustomDict = {}

dictStrCustom = {
    'strJoyJrrp': '[{tName}]的今日人品为[{tJrrpResult}]',
    'strJoyZrrp': '[{tName}]的昨日人品为[{tJrrpResult}]',
    'strJoyMrrp': '[{tName}]的明日人品为[{tJrrpResult}]'
}

dictStrConst = {
}

dictGValue = {
}

dictTValue = {
    'tJrrpResult': 'N/A'
}

dictHelpDocTemp = {
    'jrrp': '''每日人品
.jrrp 今日人品
.zrrp 昨日人品
.mrrp 明日人品
此功能采用源自《梅花易数》的卜算方法，以日期与八字起卦进行推演，结果仅供参考。''',

    'OlivaDiceJoy': '''[OlivaDiceJoy]
OlivaDice娱乐模块
本模块为青果跑团掷骰机器人(OlivaDice)娱乐模块，集成与跑团无关的历史遗留娱乐功能（如今日人品等）。
核心开发者: lunzhiPenxil仑质
[.help OlivaDiceJoy更新] 查看本模块更新日志
注: 本模块为可选不重要模块。''',

    'OlivaDiceJoy更新': '''[OlivaDiceJoy]
3.0.2: 用户记录优化
3.0.0: 初始化项目''',

    'zrrp': '&jrrp',
    'mrrp': '&jrrp',
    '今日人品': '&jrrp',
    '昨日人品': '&jrrp',
    '明日人品': '&jrrp',
}
