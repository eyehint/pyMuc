# -*- coding: euc-kr -*-

import os
import sys
import glob
import traceback
import copy
import time
from random import randint
from twisted.internet import reactor

#from objs.object import Object
from objs.body import Body
from objs.item import Item, getItem, is_item
from objs.room import Room, getRoom
from objs.mob import Mob, getMob, is_mob
from objs.config import Config, MAIN_CONFIG
from objs.skill import Skill, MUGONG
from objs.emotion import Emotion, EMOTION
from objs.nickname import Nickname, NICKNAME
from objs.oneitem import Oneitem, ONEITEM
from objs.script import SCRIPT
from objs.doumi import DOUMI
from objs.help import HELP
from objs.box import Box, is_box
from objs.rank import Rank, RANK
from objs.guild import GUILD
from include.ansi import *
from include.path import *
from include.define import *

from lib.hangul import *
from lib.loader import load_script, save_script
from lib.func import *

from client import queue

class Host:
    host = ''

class Transport:

    def write(self, line):
        return
        
    def loseConnection(self):
        return

    def getPeer(self):
        host = Host()
        return host
        
class Channel:
    def __init__(self):
        self.transport = Transport()
        self.player = None
        self.players = []
        
    def write(self, line):
        return

class Player(Body):

    cmdList = {}
    chatHistory = []
    adultCH = []

    CFG = ['자동습득', '비교거부', '접촉거부', '동행거부', '전음거부', 
    '외침거부', '방파말거부', '간략설명', '엘피출력', '나침반제거',
    '운영자안시거부', '사용자안시거부', '입출입메세지거부', 
    '타인전투출력거부', '자동무공시전', '순위거부', '수련모드', '잡담시간보기',
    '자동채널입장']
	
    def __init__(self):
        Body.__init__(self)
        self.bPlayer = 1
        self.state = 0
        self.INTERACTIVE = 0
        self.loginRetry = 0
        self.stepDeath = 0
        self.dex = 0
        self.Configs = {}
        self.talkHistory = []
        self.alias = {}
        self.autoscript = None
        self.prevCmd = ''
        self.target = []
        self.skills = []
        self.skillMap = {}
        self.itemSkillMap = {}
        self.skillList = []
        self.insure = 0
        self.follower = []
        self.follow = None
        self._talker = None
        self.memo = {}
        self.channel = Channel()
        self.channel.player = self
        self.fightMode = False
        self.cmdCnt = 0
        self.idle = 0
        self.autoMoveList = []
        self._advance = False

    def __del__(self):
        pass
        #print 'Delete!!! ' + self.get('이름')

    def getNameA(self):
        return '[1m' + self.get('이름') + '[0;37m'

    def clearItems(self):
        objs = copy.copy(self.objs)
        for item in objs:
            item.env = None
            self.objs.remove(item)
            del item
        del objs
        self.objs = []
    
    def logout(self):
        self.delFollow()
        self.delFollower()
        self.clearTarget()

        if self in self.adultCH:
            self.adultCH.remove(self)
	    buf = '\r\n[1;31m①⑨[0;37m ' + self.getNameA() + '님이 퇴장하셨습니다.'
            for ply in self.adultCH:
                ply.sendLine(buf)
                ply.lpPrompt()

        if self._talker != None:
            self._talker._talker = None
        self._talker = None

        self.clearItems()
        if self['투명상태'] == 1:
            return

        buf = ''
        nick = self['무림별호']
        if nick == '':
            nick = '무명객'
        char = self['성격']
        if char == '선인':
            buf = '☞ [[1m선인[0;37m] 『[1m%s[0;37m』' % nick
        elif char == '기인':
            buf = '☞ [[1;33m기인이사[0;37m] 『[1;33m%s[0;37m』' % nick
        elif char == '정파':
            buf = '☞ [[1;32m정파[0;37m] 『[1;32m%s[0;37m』' % nick
        elif char == '사파':
            buf = '☞ [[1;31m사파[0;37m] 『[1;31m%s[0;37m』' % nick
        elif char == '은둔칩거':
            buf = '☞ [[1;35m은둔칩거[0;37m] 『[0;37m%s[0;37m』' % nick
        else:
            buf = '☞ [[0;30;47m무명객[0;37;40m] '
        msg = '%s %s 강호를 떠나 초옥에 은거 합니다.' % (buf, self.han_iga())
        self.channel.sendToAllInOut(msg, ex = self)

    def load(self, path):

        scr = load_script('data/user/' + path)

        if scr == None:
            return False

        try:
            self.attr = scr['사용자오브젝트']
        except:
            return False
        
        self.loadConfig()
        self.loadAlias()
        self.loadSkillList()
        self.loadSkillUp()
        
        items = None
        if '아이템' not in scr:
            return True

        items = scr['아이템']
        
        if type(items) == dict:
            items = [items]
        
        for item in items:
            obj = getItem(str(item['인덱스']))
            if obj == None:
                print '사용자아이템 로딩 실패 : %s' % str(item['인덱스'])
            if obj != None:
                obj = obj.deepclone()
                if '이름' in item:
                    obj['이름'] = item['이름']
                if '반응이름' in item:
                    obj['반응이름'] = item['반응이름']
                if '공격력' in item:
                    obj['공격력'] = item['공격력']
                if '방어력' in item:
                    obj['방어력'] = item['방어력']
                if '기량' in item:
                    obj['기량'] = item['기량']
                if '상태' in item:
                    obj.inUse = True
                    self.armor += getInt(obj['방어력'])
                    self.attpower += getInt(obj['공격력'])
                    if obj['종류'] == '무기':
                        self.weaponItem = obj
                if '아이템속성' in item:
                    obj.set('아이템속성', item['아이템속성'])
                if '옵션' in item:
                    obj.set('옵션', item['옵션'])
                    if obj.inUse:
                        option = obj.getOption()
                        if option != None:
                            for op in option:
                                if op == '힘':
                                    self._str += option[op]
                                elif op == '민첩성':
                                    self._dex += option[op]
                                elif op == '맷집':
                                    self._arm += option[op]
                                elif op == '체력':
                                    self._maxhp += option[op]
                                elif op == '내공':
                                    self._maxmp += option[op]
                                elif op == '필살':
                                    self._critical += option[op]
                                elif op == '운':
                                     self._criticalChance += option[op]
                                elif op == '회피':
                                    self._miss += option[op]
                                elif op == '명중':
                                    self._hit += option[op]
                                elif op == '경험치':
                                    self._exp += option[op]
                                elif op == '마법발견':
                                    self._magicChance += option[op]

                if '확장 이름' in item:
                    obj.set('확장 이름', item['확장 이름'])
                if '체력' in item:
                    obj.hp = item['체력']
                #if '시간' in item:
                #    obj.set('시간', item['시간'])
                self.insert(obj)
            
        for memo in scr:
            if memo.find('메모') == 0:
                self.memo[memo] = scr[memo]
        
        return True
        
    def save(self, mode = True):
        if mode == True:
            self['마지막저장시간'] = int(time.time())
        self.buildSkillList()
        self.buildSkillUp()
        self.buildSkills()
        
        o = {}
        o['사용자오브젝트'] = self.attr

        items = []
        for item in self.objs:
            obj = {}
            obj['인덱스'] = item.index
            obj['이름'] = item.get('이름')
            obj['반응이름'] = item['반응이름'].splitlines()
            if item.get('공격력') != '':
                obj['공격력'] = item.get('공격력')
            if item.get('방어력') != '':
                obj['방어력'] = item.get('방어력')
            if item.get('기량') != '':
                obj['기량'] = item.get('기량')
            if item.inUse:
                obj['상태'] = item.get('계층')
            if item.get('옵션') != '':
                obj['옵션'] = item.get('옵션').splitlines()
            if item.get('아이템속성') != '':
                obj['아이템속성'] = item.get('아이템속성').splitlines()
            if item.get('확장 이름') != '':
                obj['확장 이름'] = item.get('확장 이름')
            if item.isOneItem():
                obj['시간'] = time.time()
            if item['종류'] == '호위':
                try:
                    obj['체력'] = item.hp
                except:
                    obj['체력'] = item['체력']
            items.append(obj)

        o['아이템'] = items

        for memo in self.memo:
            o[memo] = self.memo[memo]
            
        try:
            f = open('data/user/' + self.get('이름'), 'w')
        except:
            return False
        save_script(f, o)
        f.close()
        return True

    def saveItems(self):
        return True

    def write(self, line):
        if self.channel == None:
            return
        self.channel.transport.write(line)

    def sendLine(self, line):
        #self.channel.write(line + '\r\n')
        if self.channel == None:
            return
        self.channel.transport.write('%s\r\n' % line)
    
    def sendGroup(self, line, prompt = False, ex = None):
        if self['소속'] == '':
            return
        g = GUILD[self['소속']]
        if '%s명칭' % self['직위'] in g:
            buf = g['%s명칭' % self['직위']]
        else:
            buf = self['직위']
        for ply in self.channel.players:
            if ply.state == ACTIVE and ply['소속'] == self['소속'] and ply != ex and ply.checkConfig('방파말거부') == False:
                if ply != self:
                    ply.sendLine('')
                ply.sendLine('[1m《[36m%s[37mː[36m%s[37m》[0;37m ' % ( buf, self['이름'])+ line)
                if prompt and ply != self:
                    ply.lpPrompt()
                
    def sendFightScript(self, line):
        if self.checkConfig('수련모드') == False:
            self.channel.transport.write('%s\r\n' % line)

    def fightPrompt(self):
        if self.INTERACTIVE != 1:
            return
        line = '\r\n[0;37;40m[ ' + str(self.getHp()) + '/' + \
            str(self.getMaxHp()) + \
            ', ' + str(self.getMp()) + '/' + \
            str(self.getMaxMp()) + ' ] \r'
        self.write(line)
        
    def input_to(self, func, *args):
        self.process_input = func
        self.process_input_args = args

    def view(self, ob):
            ob.sendLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
            m = self.get('무림별호')
            if m == '':
                m = '무명객'
            c = self.get('성격')
            if c == '':
                c = '없음'
            s = '『%s』 %s' % (m, self.get('이름'))
            ob.sendLine('[0m[44m[1m[37m◆ 이  름 ▷ %-24s ◆ 성격 ▷ 『%s』   [0m[37m[40m' % (s, c))
            m = self.get('배우자')
            if m == '':
                m = '미혼'
            s = '『%s』' % m
            s1 = '%d살(%s)' %(self.get('나이'), self.get('성별'))
            ob.sendLine('[0m[44m[1m[37m◆ 배우자 ▷ %-24s ◆ 나이 ▷ %-9s  [0m[37m[40m' % (s, s1))
            m = self['소속']
            if m != '':
                s = '■ 소  속 ▷ 『%s』' % m
                ob.sendLine('[0m[44m[1m[37m%-60s[0m[37m[40m' % s)
                g = GUILD[self['소속']]
                if '%s명칭' % self['직위'] in g:
                    buf = g['%s명칭' % self['직위']]
                else:
                    buf = self['직위']
                r = self['방파별호']
                if r == '':
                    s = '■ 직  위 ▷ 『%s』' % buf
                else:
                    s = '■ 직  위 ▷ 『%s(%s)』' % (buf, r)
                ob.sendLine('[0m[44m[1m[37m%-60s[0m[37m[40m' % s)

            ob.sendLine('──────────────────────────────')
            c = 0
            item_str = ''
            for lv in ob.ItemLevelList:
                for item in self.objs:
                    if item.inUse and lv == item['계층']:
                        c += 1
                        item_str += '[' + ob.ItemUseLevel[item.get('계층')] + '] [36m' + item.get('이름') + '[37m\r\n'
            ob.write(item_str)
            if c == 0:
                ob.sendLine('[36m☞ 혈혈단신 맨몸으로 강호를 주유중입니다.[37m')
            ob.sendLine('──────────────────────────────')
            ob.sendLine('★ %s' % self.GetHPString())
            ob.sendLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
            
    def viewMapData(self):
        room = self.env
        if room == None:
            return

        # room Name
        
        msg = '\r\n[1;30m[[0;37m[[[1;37m[][1m %s [1;37m[][0;37m]][1;30m][0;37m' % room.get('이름')
        if getInt(self['관리자등급']) >= 1000:
            msg += ' (%s)' % (room.index)
        self.sendLine(msg)
        # room Desc
        if not self.checkConfig('간략설명'):
            self.sendLine ( '' )
            self.sendLine (room.get('설명'))

        # room Exit ↕↑↓
        if not self.checkConfig('나침반제거'):
            self.sendLine(room.longExitStr)
        else:
            self.sendLine(room.shortExitStr)
            self.sendLine ( '' )

        msg = '☞ '
        for obj in room.objs:
            if is_box(obj):
                msg += obj.viewShort() + '    '
        if len(msg) != 3:
            self.sendLine(msg)

        for obj in room.objs:
            if is_mob(obj):
                if obj.get('몹종류') == 7:
                    continue
                if obj.act == ACT_REGEN:
                    continue
                elif obj.act == ACT_REST:
                    self.sendLine(obj.han_iga() + ' 흐트러진 진기를 추스리고 있습니다.')
                if obj.act == ACT_STAND:
                    self.sendLine(obj.getDesc1())
                elif obj.act == ACT_FIGHT:

                    msg = ''
                    for s in obj.skills:
                        msg += s['방어상태머리말'] + ' '
                    self.sendLine('%s%s 목숨을 건 사투를 벌이고 있습니다.' % (msg, obj.han_iga()))
                elif obj.act == ACT_DEATH:
                    self.sendLine(obj.getNameA() + '의 싸늘한 시체가 있습니다.')
        nStr = {} # { [], [], ... }
        for obj in room.objs:
            if is_item(obj):
                c = 0
                try:
                    l = nStr[obj.get('이름')]
                except:
                    l = [0, obj.get('설명1')]
                    nStr[obj.get('이름')] = l
                l[0] = l[0] + 1

        for iName in nStr:
            l = nStr[iName]
            if l[0] == 1:
                self.sendLine( l[1].replace('$아이템$', '[36m' + iName + '[37m') )
            else:
                self.sendLine( l[1].replace('$아이템$', '[36m' + iName + '[37m %d개' % l[0]) )

        for obj in room.objs:
            if is_player(obj) and obj != self:
                if obj['투명상태'] == 1:
                    continue
                self.sendLine(obj.getDesc())

    def getDesc(self, myself = False):
        msg = ''
        if myself == False:
            s = self['방파별호']
            if s != '':
                msg = '[1m【%s】[0m' % s
            for s in self.skills:
                msg += s['방어상태머리말'] + ' '
        if self['머리말'] != '':
            msg += str(self['머리말']) + ' '
        if myself == True:
            msg += '당신이 '
        else:
            msg += self.han_iga() + ' '
        if self['꼬리말'] != '':
            msg += str(self['꼬리말']) + ' '
            
        # act 에 따라 설명을 달리해야함
        if self.act == ACT_STAND:
            msg += '서 있습니다.'
        elif self.act == ACT_REST:
            msg += '운기조식을 하고 있습니다.'
        elif self.act == ACT_FIGHT:
            msg += '목숨을 건 사투를 벌이고 있습니다.'
        elif self.act == ACT_DEATH:
            msg += '쓰러져 있습니다.'
            
        return msg
        
    def promptRoom(self):
        if self.env == None:
            return
        for obj in self.env.objs:
            if is_player(obj) and obj != self:
                obj.lpPrompt()
                    
    def writeRoom(self, line, ex = None, noPrompt = False):
        if self.env == None:
            return
        exList = []
        if ex != None and type(ex) != list:
            exList = [ ex ]
        for obj in self.env.objs:
            if is_player(obj) and obj != self  and obj not in exList:
                obj.sendLine(line)
                if noPrompt == False:
                    obj.lpPrompt()
                
    def sendRoom(self, line, ex = None, noPrompt = False):
        if self.env == None:
            return
        exList = []
        if ex != None:
            if type(ex) != list:
                exList = [ ex ]
            elif type(ex) == list:
                exList = ex
        for obj in self.env.objs:
            if is_player(obj) and obj != self and obj not in exList:
                obj.sendLine('\r\n' + line)
                if noPrompt == False:
                        obj.lpPrompt()
                        
    def sendFightScriptRoom(self, line, ex = None, noPrompt = False):
        if self.env == None:
            return
        exList = []
        if ex != None and type(ex) != list:
            exList = [ ex ]
        for obj in self.env.objs:
            if is_player(obj) and obj != self and obj not in exList and obj.checkConfig('타인전투출력거부') == False:
                obj.sendLine('\r\n' + line)
                if noPrompt == False:
                        obj.lpPrompt()
            
    def autoMove(self, line):
        if line[1] == self.env:
            self.do_command(line[0])
        else:
            idDelayedCall = 0

    def enterRoom(self, room, move = '', mode = ''):
        if self.isMovable() == False and  mode != '소환' and mode != '도망':
            self.sendLine('☞ 지금 이동하기에는 좋은 상황이 아니네요. ^_^')
            return False

        li = getInt(room['레벨상한'])
        if li > 0 and li < self['레벨']:
            self.sendLine('강한 무형의 기운이 당신을 압박합니다.')
            return False

        if getInt(room['레벨제한']) > self['레벨']:
            self.sendLine('강한 무형의 기운이 당신을 압박합니다.')
            return False

        li = getInt(room['힘상한제한'])
        if li > 0 and li < self['힘']:
            self.sendLine('강한 무형의 기운이 당신을 압박합니다.')
            return False

        li = getInt(room['민첩상한제한'])
        if li > 0 and li < self.getDex():
            self.sendLine('강한 무형의 기운이 당신을 압박합니다.')
            return False

        if room.checkLimitNum():
            self.sendLine('☞ 알 수 없는 무형의 기운이 당신을 가로막습니다. ^_^')
            return False
        if room.checkAttr('사파출입금지') and self['성격'] == '사파':
            self.sendLine('☞ 사파는 출입할 수 없는 곳이라네!')
            return False
        if room.checkAttr('정파출입금지') and self['성격'] == '정파':
            self.sendLine('☞ 정파는 출입할 수 없는 곳이라네!')
            return False
        if room['방파주인'] != '' and room['방파주인'] != self['소속']:
            self.sendLine('☞ 그곳은 타 방파의 지역이므로 출입하실 수 없습니다.')
            return False
        if self.act == ACT_FIGHT:
            self.clearTarget()
        prev = self.env
        self.exitRoom(move, mode)
        if room != None:
            room.update()
        #self.env = room
        room.insert(self)

        self.viewMapData()

        for mob in room.objs:
            if is_mob(mob) and mob.get('이벤트 $%입장이벤트%') != '':
                #mob.doEvent(player, '이벤트 $%입장이벤트%', [])
                self.doEvent(mob, '이벤트 $%입장이벤트%', [])

        if self['투명상태'] != 1:
            txt = self.env.get('진입스크립:' + move)
            if txt != '':
                # 무리 이동시 인원만큼 이동 후 프롬프트가 출력
                buf = txt.replace('[공]', self.getNameA())
                buf = postPosition1(buf)
                self.writeRoom('\r\n' + buf)
            else:
                if mode == '시작':
                    buf = ''
                    nick = self['무림별호']
                    if nick == '':
                        nick = '무명객'
                    char = self['성격']
                    if char == '선인':
                        buf = '☞ [[1m선인[0;37m] 『[1m%s[0;37m』' % nick
                    elif char == '기인':
                        buf = '☞ [[1;33m기인이사[0;37m] 『[1;33m%s[0;37m』' % nick
                    elif char == '정파':
                        buf = '☞ [[1;32m정파[0;37m] 『[1;32m%s[0;37m』' % nick
                    elif char == '사파':
                        buf = '☞ [[1;31m사파[0;37m] 『[1;31m%s[0;37m』' % nick
                    elif char == '은둔칩거':
                        buf = '☞ [[1;35m은둔칩거[0;37m] 『[0;37m%s[0;37m』' % nick
                    else:
                        buf = '☞ [[0;30;47m무명객[0;37;40m] '
                    msg = '%s %s [1;36m무림지존을 꿈꾸며 강호에 출두합니다.[0;37m' % (buf, self.han_iga())
                    self.channel.sendToAllInOut(msg, ex = self)
                if mode == '귀환':
                    self.writeRoom('\r\n%s 하늘에서 사뿐히 내려 앉습니다. \'척~~~\'' % self.han_iga())
                elif mode == '소환':
                    self.writeRoom('\r\n%s 알수 없는 기운에 감싸여 나타납니다. \'고오오오~~~\'' % self.han_iga())
                elif mode == '도망':
                    self.writeRoom('\r\n%s 신형을 비틀거리며 간신히 도망옵니다. \'헉헉~~\' '  % self.han_iga())
                elif mode == '사망':
                    self.sendRoom('%s 손수레에 실려옵니다.' % self.han_iga())
                else:
                    #기인/선인/정사파에 따라 다름
                    self.sendRoom('%s 왔습니다.'% self.han_iga())

        for attr in room.mapAttr:
            if attr.find('체력감소') == 0:
                dmg = attr.split(None, 2)[1]
                msg = attr.split(None, 2)[2]
                self.lpPrompt()
                buf = msg.replace('[공]', '당신')
                buf = postPosition1(buf)
                self.sendLine('\r\n' + buf)
                buf = msg.replace('[공]', self.getNameA())
                buf = postPosition1(buf)
                self.sendRoom(buf)
                if self.minusHP(getInt(dmg), False):
                    return True
                break
        c = 0
        #방에 있는 선공몹 처리
        if self['투명상태'] != 1:
            for obj in room.objs:
                if is_mob(obj) and obj not in self.target and obj.act == ACT_STAND:
                    if obj.get('전투종류') == 1:
                        self.lpPrompt()
                        self.setFight(obj, True)
                        c += 1
                        break;
        if c > 0:
            self.doSkill()
            #self.lpPrompt()

        auto = room.get('자동이동')
        if auto != '':
            self.idDelayedCall = reactor.callLater( 1, self.autoMove, [auto.split()[0], room] )
        
        for f in self.follower:
            if f.env == prev and mode == '이동':
                reactor.callLater(0, f.do_command, move)

        if auto == '' and len(self.target) == 0:
            reactor.callLater(0.1, self.moveNext)
            #self.moveNext()

        return True

    def exitRoom(self, move = '', mode = ''):
        if self.env != None  and self['투명상태'] != 1:
            txt = self.env.get('이동스크립:' + move)
            if txt != '':
                # 무리 이동시 인원만큼 이동 후 프롬프트가 출력
                buf = txt.replace('[공]', '당신')
                buf = postPosition1(buf)
                self.sendLine('\r\n' + buf)
                buf = txt.replace('[공]', self.getNameA())
                buf = postPosition1(buf)
                self.sendRoom('\r\n' + buf)

            else:
                if mode == '귀환':
                    self.sendLine('당신이 경공술을 펼치며 하늘로 치솟아 오릅니다. \'무영지신!!!\'')
                    self.writeRoom('\r\n%s 경공술을 펼치며 하늘로 치솟아 오릅니다. \'무영지신!!!\'' % self.han_iga())
                elif mode == '소환':
                    self.sendLine('당신이 알수 없는 기운에 휘말려 사라집니다. \'고오오오~~~\'')
                    self.writeRoom('\r\n%s 알수 없는 기운에 휘말려 사라집니다. \'고오오오~~~\'' % self.han_iga())
                elif mode == '도망':
                    self.sendLine('당신이 신형을 비틀거리며 간신히 도망갑니다. \'살리도~~\'')
                    self.writeRoom('\r\n%s 신형을 비틀거리며 간신히 도망갑니다. \'살리도~~\'' % self.han_iga())
                elif mode == '사망':
                    self.sendRoom('[1m장의사[0;37m가 %s 데려갑니다.' % self.han_obj())
                elif mode == '숨겨진맵이동':
                    self.sendRoom('%s 갑자기 어디론가 사라집니다.' % self.han_iga())
                else:
                    msg = '%s %s쪽으로 갔습니다.\r\n'% ( self.han_iga(), move)
                    self.sendRoom(msg[:-2] , ex = self.follower)
                    for f in self.follower:
                        if f.env == self.env and mode == '이동':
                            f.sendLine('\r\n' + msg + '당신이 %s쪽으로 %s 따라갑니다.' % (move, self.han_obj()))
            self.env.remove(self)
        if self.env != None  and self['투명상태'] == 1:
            self.env.remove(self)

    def welcome(self):
        from lib.io import cat
        cat(self, 'data/text/logoMurim.txt')
        self.sendLine(WHT+BBLK + '무림에서 불리우는 존함을 알려주세요. (처음 오시는 분은 [1m무명객[0;40m이라고 하세요)')
        self.write('무림존함ː')
        self.input_to(self.get_name)

    def lpPrompt(self, mode = False):
        if not self.checkConfig('엘피출력'):
            self.prompt(True)
            if mode:
                self.sendLine('')

    def prompt(self, mode = False):
        if self.INTERACTIVE != 1:
            return
        if mode:
            self.write('\r\n')
        line = '[0;37;40m[ %d/%d, %d/%d ] ' % (self.getHp(), self.getMaxHp(), self.getMp(), self.getMaxMp())
        self.write(line)

    def getDesc1(self):
        return self.get('설명1').replace('$아이템$', self.get('이름'))

    def die(self, mode = True):
        self.act = ACT_DEATH
        self._str = 0
        self._dex = 0
        self._arm = 0
        self.autoMoveList = []
        
        self.unwearAll()
        if mode:
            self.sendLine('\r\n[1;37m당신이 쓰러집니다. \'쿠웅~~ 철퍼덕~~\'[0;37m')
        self.dropAllItem()
        self.sendLine('당신은 정신이 혼미합니다.')
        self.lpPrompt()
        self.clearTarget()
        self.clearSkills()
        for s in self.skills:
            self._str += s._str
            self._dex += s._dex
            self._arm += s._arm
        self.input_to(self.coma)

    def coma(self, line, *args):
        if line != '':
            self.sendLine('\r\n당신은 정신이 혼미합니다.')

    def checkMobEvent(self, line):
        words = line.split()
        if len(words) < 2:
            return False
        if self.env == None:
            return False
        mob = self.env.findObjName(words[0])
        if mob != None and is_mob(mob):
            key = mob.checkEvent(words)
            if key != '':
                self.doEvent(mob, key, words)
                return True
        return False

    def checkEvent(self, e):
        return self.checkAttr('이벤트설정리스트', e)

    def setEvent(self, e):
        self.setAttr('이벤트설정리스트', e)

    def delEvent(self, e):
        self.delAttr('이벤트설정리스트', e)
        
    def checkArmed(self, level):
        for item in self.objs:
            if item.inUse and item.get('계층') == level:
                return True
        return False

    def checkItemIndex(self, index, cnt = 1):
        c = 0
        if index == '은전':
            m = self.get('은전')
            if cnt < 1:
                return False
            if m < cnt:
                return False
            return True

        if index == '금전':
            m = self.get('금전')
            if cnt < 1:
                return False
            if m < cnt:
                return False
            return True

        for item in self.objs:
            if item.index == index:
                c = c + 1
                if cnt == c:
                    return True
        return False

    def checkItemName(self, name, cnt = 1):
        c = 0
        if name == '은전':
            if cnt < 1:
                return False
            m = self.get('은전')
            if m < cnt:
                return False
            return True

        if name == '금전':
            if cnt < 1:
                return False
            m = self.get('금전')
            if m < cnt:
                return False
            return True

        for item in self.objs:
            if item.inUse:
                continue
            if stripANSI(item.get('이름')) == name:
                c = c + 1
                if cnt == c:
                    return True
        return False

    def getItemIndex(self, index, cnt = 1):
        c = 0
        for item in self.objs:
            if item.index == index:
                c = c + 1
                if cnt == c:
                    return item
        return None

    def getItemName(self, name, cnt = 1):
        c = 0
        for item in self.objs:
            if item.getStrip('이름') == name:
                c = c + 1
                if cnt == c:
                    return item
        return None

    def addItem(self, index, cnt = 1, gamble = 0):
        c = 0
        if index == '은전':
            m = self.get('은전')
            m = m + cnt
            self.set('은전', m)
            return

        if index == '금전':
            m = self.get('금전')
            m = m + cnt
            self.set('금전', m)
            return

        item = getItem(index)
        if item == None:
            return
        for i in range(cnt):
            obj = item.deepclone()
            if obj.isOneItem():
                ONEITEM.have(index, self['이름'])
            if cnt == 1:
                obj.applyMagic(self['레벨'], 0, 1)
                if gamble != 0:
                    obj.setAttr('아이템속성', '버리지못함')
                    obj.setAttr('아이템속성', '줄수없음')
            self.insert(obj)

    def delItem(self, index, cnt = 1):
        c = 0
        if index == '은전':
            m = self.get('은전')
            m -= cnt
            self.set('은전',m)
            return

        if index == '금전':
            m = self.get('금전')
            m -= cnt
            self.set('금전',m)
            return

        objs = copy.copy(self.objs)
        for item in objs:
            if item.index == index:
                if item.inUse:
                    self.armor -= getInt(item['방어력'])
                    self.attpower -= getInt(item['공격력'])
                    option = item.getOption()
                    if option != None:
                        for op in option:
                            if op == '힘':
                                self._str -= option[op]
                            elif op == '민첩성':
                                self._dex -= option[op]
                            elif op == '맷집':
                                self._arm -= option[op]
                            elif op == '체력':
                                self._maxhp -= option[op]
                            elif op == '내공':
                                self._maxmp -= option[op]
                            elif op == '필살':
                                self._critical -= option[op]
                            elif op == '운':
                                 self._criticalChance -= option[op]
                            elif op == '회피':
                                self._miss -= option[op]
                            elif op == '명중':
                                self._hit -= option[op]
                            elif op == '경험치':
                                self._exp -= option[op]
                            elif op == '마법발견':
                                self._magicChance -= option[op]
                            
                self.remove(item)
                c += 1
                if cnt == c:
                    break

    def getTendency(self, line):
        type = line.strip()
        p1 = self['0 성격플킬']
        p2 = self['1 성격플킬']
        p3 = self['2 성격플킬']
        
        if type == '완성':
            if self.get('무림별호') != '':
                return True
            return False
        elif type == '정파':
            if p1 + p2 + p3 < MAIN_CONFIG['무림별호이벤트킬수'] or p3 > p2:
                return False
            return True
        elif type == '사파':
            if p1 + p2 + p3 < MAIN_CONFIG['무림별호이벤트킬수'] or p2 > p3:
                return False
            return True

    def printScript(self, line):
        l1 = line.replace('[공]', '당신')
        l2 = postPosition1(l1)
        self.sendLine(l2)
        l1 = line.replace('[공]', self.getNameA())
        l2 = postPosition1(l1)
        self.sendRoom(l2)

    def addMugong(self, line):
        if line.strip() not in self.skillList:
            self.skillList.append(line.strip())


    def delMugong(self, line):
        m = line.strip()
        ms = self.get('무공이름').splitlines()
        if line.strip() in self.skillList:
            self.skillList.remove(line.strip())

    def checkMugong(self, line):
        if line.strip() in self.skillList:
            return True
        return False

    def checkMugongList(self, line):
        m = line.split()
        for n in m:
            if n not in self.skillList:
                return False
        return True

    def setEunDun(self):
        p1 = self.get('힘')
        p1 = p1 - 2000
        if p1 < 15:
            p1 = 15        
        self.set('힘', p1)
        self.set('레벨', 1)
        self.set('현재경험치', 0)
        self.set('힘경험치', 0)
        self.set('맷집경험치', 0)
        self.set('기존성격', self.get('성격'))
        self.set('성격', '은둔칩거')
        self.set('내공증진아이템리스트', '')
        self.set('이벤트설정리스트', '은둔칩거끝')

    def setSunIn(self):
        self.set('기존성격', self.get('성격'))
        self.set('성격', '선인')
        self.set('내공증진아이템리스트', '')
        self.set('이벤트설정리스트', '우화등선끝')

    def setGiIn(self):
        p1 = self.get('힘')
        p1 = p1 - 600
        if p1 < 15:
            p1 = 15
        self.set('힘', p1)
        self.set('맷집', 15)
        self.set('레벨', 1)
        self.set('현재경험치', 0)
        self.set('힘경험치', 0)
        self.set('맷집경험치', 0)
        self.set('기존성격', self.get('성격'))
        self.set('성격', '기인')
        self.set('내공증진아이템리스트', '')
        self.set('이벤트설정리스트', '소오강호끝')

    def get_name(self, name, *args):
        self.loginRetry += 1
        if self.loginRetry > 2:
            self.channel.transport.loseConnection()
            return
        #self.channel.transport.loseConnection()
        if len(name) == 0:
            self.write('\r\n무림존함ː')
            return
        if is_han(name) == False:
            self.write('한글 입력만 가능합니다.\r\n무림존함ː')
            return
        if name == '무명객':
            #if self.checkMulti():
            #    return
            self.input_to(self.doNothing)
            self.state = sDOUMI
            from objs.doumi import DOUMI, autoScript
            self.autoscript = autoScript()
            self.autoscript.start(DOUMI['초기도우미'].splitlines(), self)
            return
        if name == '나만바라바':
            #if self.checkMulti():
            #    return
            self.input_to(self.doNothing)
            from objs.doumi import DOUMI, autoScript
            self.autoscript = autoScript()
            self.autoscript.start(DOUMI['빠른도우미'].splitlines(), self)
            return

        from client import Client
        for p in Client.players:
            if p.get('이름') == name and p != self and p.state != INACTIVE:
                self.sendLine('☞ 이미 무림에서 활동중 입니다.\r\n')
                self.write('무림존함ː')
                return

        res = self.load(name)
        if res == False:
            self.write('그런 사용자는 없습니다.\r\n무림존함ː')
            return

        # ip 중복 검사/인증시 패스
        #if self.checkMulti():
        #    return

        curtime = time.time()
        c = getInt(self['강제종료'])
        if c != 0:
            if curtime - c < getInt(MAIN_CONFIG['재접속제한시간']):
                self.sendLine('\r\n%d 초 뒤에 재접속하십시오.\r\n' % (getInt(MAIN_CONFIG['재접속제한시간']) - (curtime - c)) )
                self.channel.transport.loseConnection()
                return
        
        #self.set('이름', name)
        self.write('존함암호ː')
        self.loginRetry = 0
        self.input_to(self.get_pass)

    def checkMulti(self):
        if getInt(self['관리자등급']) > 0:
            return False

        if self['멀티인증'] == 1:
            return False

        ip = self.channel.transport.getPeer().host
        cnt = 0
        for ply in self.channel.players:
            if ply.channel.transport.getPeer().host == ip:
                cnt += 1

        if cnt < 4:
            return False

        self.sendLine('\r\n중복 접속을 제한합니다.\r\n')
        self.channel.transport.loseConnection()
        return True

    def get_oldpass(self, line, *args):
        if line.strip() != str(self['암호']):
            self.sendLine('☞ 현재의 암호가 맞지 않아요. ^^')
            self.INTERACTIVE = 1
            self.input_to(self.parse_command)
            return
        self.write('☞ 변경 하실 암호를 입력해주세요. \r\n존함암호ː')
        self.input_to(self.change_password)
    
    def change_password(self, line, *args):
        self._pass = line
        self.write('☞ 한번 더 암호를 입력해주세요. \r\n암호확인ː')
        self.input_to(self.change_password1)
    
    def change_password1(self, line, *args):
        if line != self._pass:
            self.sendLine('☞ 이전 입력과 다릅니다. 암호변경을 취소합니다.')
            self.INTERACTIVE = 1
            self.input_to(self.parse_command)
            return
        self['암호'] = line
        self.write('☞ 암호가 변경되었습니다.')
        self.INTERACTIVE = 1
        self.input_to(self.parse_command)
        
    def get_pass(self, line, *args):
        self.loginRetry += 1
        if len(line) == 0 or str(self.get('암호')) != line:
            if self.loginRetry >= 3:
                self.write('\r\n')
                self.channel.transport.loseConnection()
                return
            self.write('잘못된 암호 입니다.\r\n존함암호ː')
            return
        del self.loginRetry

        from client import Client
        for p in Client.players:
            if p['이름'] == self['이름'] and p != self and p.state != INACTIVE:
                self.sendLine('☞ 이미 무림에서 활동중 입니다.\r\n')
                self.channel.transport.loseConnection()
                return
        #self.channel.players.append(self)
        self.showNotice()

    def doNothing(self, line, *args):
        return

    def NextPage(self, line, *args):
        from twisted.internet import reactor
        self.write('[2J') # CLEAR SCREEN
        self.input_to(self.doNothing)
        reactor.callLater(3, self.newbie_msg, '')
        return

    def getNewname(self, name, *args):
        if len(name) == 0:
            self.write('☞ 한글자 이상 입력하세요.\r\n무림존함ː')
            return
        if len(name) > 10:
            self.write('☞ 사용하시려는 존함이 너무 길어요.\r\n무림존함ː')
            return
        if is_han(name) == False:
            self.write('☞ 한글 입력만 가능합니다.\r\n무림존함ː')
            return
        if name == '무명객':
            self.write('☞ 사용할 수 없는 존함입니다. 한글로 입력해주세요.\r\n무림존함ː')
            return
        import os
        if os.path.exists(USER_PATH + name) == True:
            self.write('☞ 이미 무림에서 활동중 입니다.\r\n무림존함ː')
            return
        for ply in self.channel.players:
            if ply['이름'] == name:
                self.write('☞ 이미 무림에서 활동중 입니다.\r\n무림존함ː')
                return
        self.set('이름', name)
        self.init_body()
        item = getItem('368').deepclone()
        self.insert(item)
        #self.channel.players.append(self)
        self.input_to(self.doNothing)
        self.autoscript.run()
        #self.write('\r\n왕대협이 말합니다. "%s라고 합니다."' % name + '\r\n노인이 말합니다. "음! 좋은 이름이군 그렇다면 암호는??"\r\n존함암호ː')
        #self.input_to(self.getNewpass)

    def getNewpass(self, line, *args):
        if len(line) < 3:
            self.write('\r\n☞ 3자 이상 입력하세요.\r\n존함암호ː')
            return
        self.set('암호', line)
        self.write('\r\n암호확인ː')
        self.input_to(self.getNewpass2)

    def getNewpass2(self, line, *args):
        if line != self.get('암호'):
            self.write('\r\n☞ 존함의 암호가 일치하지 않는군요.\r\n존함암호ː')
            self.input_to(self.getNewpass)
            return
        self.input_to(self.doNothing)
        self.autoscript.run()
        #self.write('\r\n노인이 말합니다. "그런데 그아이는 남자인가? 여자인가?"\r\n성별(남/여)ː')
        #self.input_to(self.getSex)

    def getSex(self, line, *args):
        if line not in ['남', '여']:
            self.write('\r\n☞ [남], [여]로 말해주세요.\r\n성별(남/여)ː')
            return
        self.set('성별', line)
        self.input_to(self.doNothing)
        self.autoscript.run()
        
    def showNotice(self):
        self.write('[0m[37m[40m[H[2J')
        from lib.io import cat
        cat(self, 'data/text/notice.txt')
        self.write('[엔터키를 누르세요]')
        self.state = NOTICE
        self.input_to(self.getStart)
        
    def write_edit(self, line, *args):
        if line == '.':
            try:
                f = open('data/' + self._lineDataTarget, 'w')
            except:
                return False
            f.write(self._lineData)
            f.close()
            self.sendLine('작성을 마칩니다.')
            del self._lineDataTarget
            del self._lineData
            self.INTERACTIVE = 1
            self.input_to(self.parse_command)
            return

        if self._lineData == '':
            self._lineData = line
        else:
            self._lineData = self._lineData + '\n' + line
        self.sendLine(line)
        self.write(':')

    def write_lines(self, line, *args):
        if line == '.':
            self._lineDataTarget[self._lineDataValue] = self._lineData
            self._lineDataTarget.save()
            self.sendLine('작성을 마칩니다.')
            del self._lineDataTarget
            del self._lineDataValue
            del self._lineData
            self.INTERACTIVE = 1
            self.input_to(self.parse_command)
            return
        if line == '':
            line = ' '
        if self._lineData == '':
            self._lineData = line
        else:
            self._lineData = self._lineData + '\r\n' + line
        self.sendLine(line)
        self.write(':')

    def write_memo(self, line, *args):
        l = len(self._memoBody.splitlines())
        if line == '.' or l >= 10:
            msg = ''
            found = False
            for ply in self.channel.players:
                if ply['이름'] == self._memoWho['이름']:
                    found = True
                    break
            if found:
                self.sendLine('사용자가 접속하였으므로 작성을 마칩니다.')
            else:
                if l >= 10:
                    msg += '제한용량을 초과하였습니다.\r\n'
                msg += '쪽지 작성을 마칩니다.'
                self._memo['내용'] = self._memoBody
                self._memoWho.memo['메모:%s' % self['이름']] = self._memo
                self._memoWho.save(False)
                self.sendLine(msg)
            del self._memo
            self._memo = {}
            del self._memoWho
            self._memoWho = None
            self.INTERACTIVE = 1
            self.input_to(self.parse_command)
            return
        if line == '':
            line = ' '
        if self._memoBody == '':
            self._memoBody = line
        else:
            self._memoBody = self._memoBody + '\r\n' + line
        self.write(':')
            
    def getStart(self, line, *args):
        self['_runaway'] = 0
        self.state = ACTIVE
        self.loadSkills()
        rName = self.get('귀환지맵')
        if rName == '':
            rName = '낙양성:42'
        room = getRoom(rName)
        last = self['마지막저장시간']
        if last != '':
            self.sendLine('마지막 접속 시간 : %s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last)))
        if room != None:
            self.enterRoom(room, '시작', '시작')
        else:
            self.sendLine('시작맵 없음!!!')
        
        l = len(self.memo)

        if l > 0:
            msg = '[1m★[0;37m 도착된 쪽지가 %d통 있습니다.\r\n   정보수집소에 가서 쪽지를 확인해보시기 바랍니다.' % l
            self.sendLine(msg)
        self.INTERACTIVE = 1

        v = self['특성치']
        if v == '':
            self['특성치'] = int(self['최고체력'] / 300)
            self.save()

        if self.checkConfig('자동채널입장'):
            buf = '\r\n[1;31m①⑨[0;37m ' + self.getNameA() + '님이 입장하셨습니다.'
            for ply in self.adultCH:
                ply.sendLine(buf)
                ply.lpPrompt()

            self.adultCH.append(self)
            self.sendLine('☞ 채널에 입장합니다.')
            
        self.input_to(self.parse_command)

    def do_command(self, line, noPrompt = False):
        self.parse_command(line)
        if noPrompt == False:
            self.lpPrompt()

    def parse_command(self, line, *args):
        if self.env == None:
            print self['이름']
            return

        if getInt(self['관리자등급']) < 2000:
            self.cmdCnt += 1
            if self.cmdCnt > MAIN_CONFIG['입력초과경고수']:
                self.sendLine('^^;')
                return
        line = stripANSI(line)
        if len(line) == 0:
            return
        
        if line == '!':
            line = self.prevCmd
        else:
            self.prevCmd = line
            
        if line[-1] in (' ', '.', '!', '?'):
            if self.env.noComm():
                self.sendLine('☞ 이지역에서는 어떠한 통신도 불가능합니다.')
                return
            Player.cmdList['말'].cmd(self, line)
            return

        cmds = line.split()
        if len(cmds) == 0:
            return
        cmd = cmds[-1]
        argc = len(cmds)
        param = line.rstrip(cmd)
        param = param.strip()

        if self.env != None and cmd in self.env.limitCmds:
            self.sendLine('이곳에서 그 명령을 사용할 수 없습니다.')
            return
            
        if cmd in self.alias:
            shortcut = self.alias[cmd]
            if argc > 1:
                sub = line.strip().rsplit(None, 1)[0]
                #shortcut = shortcut.replace('*', sub)
                wlist0 = shortcut.split(';')
                wlist = []
                for w in wlist0:
                    wlist.append(w.replace('*', sub)) 
            else:
                wlist = shortcut.split(';')
            
            line = wlist[0]
            cmds = line.split()
            if len(cmds) == 0:
                return
            cmd = cmds[-1]
            argc = len(cmds)
            param = line.rstrip(cmd)
            param = param.strip()
            
            msg = ''
            for w in wlist[1:]:
                #if w in s:
                #    self.sendLine('중첩된 줄임말은 사용할 수 없습니다.')
                #    return
                msg += w + '\r\n'
            self.channel._buffer = msg + self.channel._buffer

        try:
            if self.checkMobEvent(line) == True:
                return
        except :
            traceback.print_exc(file=sys.stderr)
            print 'Error in %s' % cmd
            return
            
        from objs.alias import alias
        if cmd in alias:
            cmd = alias[cmd]

        if self.env != None and argc == 1:
            if cmd in self.env.Exits:
                room = self.env.getExit(cmd)
                if room == None:
                    self.sendLine('Move where?')
                    return
                mode = '이동'
                if cmd + '$' in self.env.exitList:
                    mode = '숨겨진맵이동'
                self.enterRoom(room, cmd, mode)
                return
            else:
                if cmd in ['동', '서', '남', '북', '위', '아래', '북동', '북서', '남동', '남서']:
                    self.sendLine('☞ 그쪽 방향으로는 가실 수 없습니다.')
                    return
                for exitName in self.env.Exits:
                    if exitName.find(cmd) == 0:
                        room = self.env.getExit(exitName)
                        if room == None:
                            self.sendLine('Move where?')
                            return
                        mode = '이동'
                        if exitName + '$' in self.env.exitList:
                            mode = '숨겨진맵이동'
                        self.enterRoom(room, exitName, mode)
                        return

        if cmd in ('끝', '종료') and argc == 1:
            if self.isMovable() == False:
                self.sendLine('☞ 지금은 무림을 떠나기에 좋은 상황이 아니네요. ^_^')
                return
            self.INTERACTIVE = 2
            self.sendLine('\r\n다음에 또 만나요~!!!')
            #broadcast(self.get('이름') + '님이 나가셨습니다.', self)
            #self.save()
            #self.logout()

            self.channel.transport.loseConnection()
            return
        elif cmd in Player.cmdList:
            try:
                Player.cmdList[cmd].cmd(self, param)
            except :
                traceback.print_exc(file=sys.stderr)
                print 'Error in %s' % cmd
            return
        elif cmd in EMOTION.attr:
            if self.env.noComm():
                self.sendLine('☞ 이지역에서는 어떠한 통신도 불가능합니다.')
                return
            try:
                self.doEmotion(cmd, param)
                #Player.emotes[cmd].cmd(self, param)
            except :
                traceback.print_exc(file=sys.stderr)
                print 'Error in %s' % cmd
            return

        obj = ''
        if self.env != None:
            obj = self.env['오브젝트:'+cmd]
        if obj != '':
            self.sendLine(obj)
            return
        self.sendLine('☞ 무슨 말인지 모르겠어요. *^_^*')

    def checkInput(self, line, *args):
        if line == '네':
            self.autoscript.run()
            return
        if line == '취소':
            self.sendLine('☞ 취소합니다. *^_^*')
            self.stopAutoScript()
            return 
        self.sendLine('☞ 취소하시려면 『취소』를 입력 하세요. *^_^*')
        return 

    def getLines(self, line, *args):
        limit = 5
        if len(args) != 0:
            limit = int(args[0])
        line = line.strip()
        if line == '':
            self.sendLine('☞ 취소하시려면 『취소』를 입력 하세요. *^_^*')
            return 
        if line == '.':
            if len(self.temp_input) == 0:
                self.sendLine('☞ 한줄 이상 입력하세요. *^_^*')
                return 
            self.autoscript.run()
            return 
        if len(line) > 42:
            self.sendLine('☞ 너무길어요. *^_^*')
            return
        if line == '취소':
            self.sendLine('☞ 취소합니다. *^_^*')
            self.stopAutoScript()
            return 
        self.temp_input.append(line)
        if len(self.temp_input) >= limit:
            self.sendLine('☞ 입력을 마칩니다. *^_^*')
            self.autoscript.run()
            return

    def getLine(self, line, *args):
        limit = 70
        line = line.strip()
        if line == '':
            self.sendLine('☞ 취소하시려면 『취소』를 입력 하세요. *^_^*')
            return 
        if line == '취소':
            self.sendLine('☞ 취소합니다. *^_^*')
            self.stopAutoScript()
            return 
        if len(stripANSI(line)) > limit:
            self.sendLine('☞ 너무길어요. *^_^*')
            return
        self.temp_input = line
        self.autoscript.run()

    def getWord(self, line, *args):
        limit = args[0]
        keywords = args[1]
        line = line.strip()
        if line == '':
            self.sendLine('☞ 취소하시려면 『취소』를 입력 하세요. *^_^*')
            return 
        if ' ' in line:
            self.sendLine('☞ 공백이 포함되어 있습니다. 다시 입력하세요. *^_^*')
            return 
        if line == '취소':
            self.sendLine('☞ 취소합니다. *^_^*')
            self.stopAutoScript()
            return 
        if len(stripANSI(line)) > limit:
            self.sendLine('☞ 너무길어요. *^_^*')
            return
        if line not in keywords and len(keywords) > 0:
            self.sendLine('☞ 잘못 입력하셨어요. *^_^*')
            return
        self.temp_input = line
        self.autoscript.run()

    def stopAutoScript(self):
        self.INTERACTIVE = 1
        self.autoscript.player = None
        del self.autoscript
        self.autoscript = None
        self.input_to(self.parse_command)
        self.lpPrompt()

    def pressEnter1(self, line, *args):
        self.input_to(self.doNothing)
        self.autoscript.run()
        
    def getKeyInput(self, line, *args):
        if line == args[0]:
            self.input_to(self.doNothing)
            self.autoscript.run()
        else:
            self.sendLine('『%s』을 입력 하세요\r\n>' % args)
            
    def pressEnter(self, line, *args):
        self.INTERACTIVE = 1
        self.input_to(self.parse_command)

    def getFightStartStr(self):
        w = self.getWeapon()
        if w == None:
            buf1 = '당신이 주먹을 쥐며 공격 합니다.'
            buf2 = '%s 주먹을 쥐며 공격 합니다.' % self.han_iga()
        else:
            buf1 = '당신이 %s' % w['전투시작']
            buf2 = '%s %s' % (self.han_iga(), w['전투시작'])
        return buf1, buf2

    def setFight(self, mob, mode = False):
        if self.act == ACT_DEATH:
            return
        self.fightMode = mode
        self.dex = 0
        if mode == True:
            if mob.act == ACT_STAND:
                buf1, buf2 =  mob.getFightStartStr()
                self.sendLine('\r\n' + buf1)
                self.writeRoom('\r\n' + buf1, noPrompt = True)
            if self.act == ACT_STAND:
                buf1, buf2 = self.getFightStartStr()
                self.sendLine(buf1)
                self.writeRoom(buf2, noPrompt = True)
        else:
            self.target.append(mob)
            mob.target.append(self)
            
            if self.doSkill():
                self.sendLine('')
                self.writeRoom('', noPrompt = True)
            if self.act == ACT_STAND:
                buf1, buf2 = self.getFightStartStr()
                self.sendLine(buf1)
                if self.skill == None:
                    buf2 = '\r\n' + buf2
                self.writeRoom(buf2, noPrompt = True)
            if mob.act == ACT_STAND:
                buf1, buf2 = mob.getFightStartStr()
                self.sendLine(buf1)
                self.writeRoom(buf1, noPrompt = True)
            self.promptRoom()
            
        self.act = ACT_FIGHT
        mob.act = ACT_FIGHT
        self.setTarget(mob)
        mob.setTarget(self)
        
        if is_mob(mob):
            mob.stopSkill()
            self.startMobSkill(mob)
        
        #방에 있는 합공몹 처리(덩달이)
        for obj in self.env.objs:
            if is_mob(obj) and obj not in self.target and obj.act == ACT_STAND:
                if obj.get('전투종류') == 1 or obj.get('전투종류') == 2:
                    self.setTarget(obj)
                    obj.setTarget(self)
                    buf1, buf2 = obj.getFightStartStr()
                    self.sendLine(buf1)
                    obj.stopSkill()
                    self.startMobSkill(obj)
        
    def startMobSkill(self, mob):
        if mob.setSkill() and self.checkConfig('수련모드') == False:
            buf1, buf2, buf3 = mob.makeFightScript(mob.skill['무공스크립'], self)
            self.sendLine(buf2)
            self.sendRoomFightScript(buf3)
            
    def update(self):
        self._advance = False

        if self.cmdCnt > MAIN_CONFIG['입력초과에러수']:
            self['강제종료'] = int(time.time())
            self.channel.transport.loseConnection()
            return
        self.cmdCnt = 0
        self.tick += 1
        self['나이오름틱'] += 1
        if self['나이오름틱'] >= MAIN_CONFIG['나이오름틱']: #24시간에 1살
            self['나이오름틱'] = 0
            self['나이'] += 1
            if self['나이'] % 60 == 0:
                self['최고내공'] += 60
            else:
                self['최고내공'] +=1
            self.sendRoom('[1m' + self['이름'] + '의 단전에 회오리가 몰아치며 몸주위에 하얀 진기가 맴돕니다.[0;37m')
            self.sendLine('\r\n[1m당신의 단전에 회오리가 몰아치며 몸주위에 하얀 진기가 맴돕니다.[0;37m')
            self.lpPrompt()
        if self.tick % 60 == 0:
            if self['무림별호'] == '' and self['0 성격플킬'] + self['1 성격플킬'] + self['2 성격플킬'] >= MAIN_CONFIG['무림별호이벤트킬수']:
                self.sendLine('\r\n' + MAIN_CONFIG['무림별호이벤트호출'])
                self.lpPrompt()
        if self.tick % 600 == 0:
            self.save()
        if self.act == ACT_FIGHT:
            #전투처리
            self.doFight()
            if len(self.target) == 0:
                self.doAfterFight()
        elif self.act == ACT_DEATH:
            #사망처리
            self.doDeath()
            return
        else:
            if self.skill != None:
                self.skill.stopSkill()
            if len(self.target) != 0:
                self.clearTarget()
        if self.tick % 30 == 0:
            self.recover()
            
       
        if self.act == ACT_STAND or self.act == ACT_FIGHT:
            self.autoHpEat()
            self.autoMpEat()

        self.checkDefenceSkill()

    def autoHpEat(self):
        h = 0
        if '체력' not in self.alias:
            return
        if '체력약' not in self.alias:
            return

        food = self.alias['체력약']
        if food == '':
            return

        h = getInt(self.alias['체력'])
        if h == 0:
            return

        if self.getHp() < h:
            self.do_command('%s 먹어' % food)

    def autoMpEat(self):
        m = 0
        if '내공' not in self.alias:
            return
        if '내공약' not in self.alias:
            return
        food = self.alias['내공약']
        if food == '':
            return

        m = getInt(self.alias['내공'])
        if m == 0:
            return

        if self.getMp() < m:
            self.do_command('%s 먹어' % food)

    def doAfterFight(self):
        self.moveNext()

    def moveNext(self):
        if self.act != ACT_STAND:
            return

        if len(self.autoMoveList) == 0:
            return
        att = ''
        if '공격' in self.alias:
            att = self.alias['공격']
          
        if att != '':
            self.do_command(att)
            if len(self.target) != 0:
                return
        
        next = self.autoMoveList.pop(0)
        self.do_command(next)
        if len(self.autoMoveList) == 0:
            self.sendLine('☞ 더 이상 이동 할 경로가 없습니다.')
            self.lpPrompt()

    def doSkill(self):
        #자동무공시전설정이 되어있는지도 체크필요
        if self.skill == None and self.checkConfig('자동무공시전'):
            sName = self['자동무공']
            if sName != '':
                self.getSkill(sName)
                s = self.skill
                if self.getMp() < s.mp:
                    self.sendLine('[1m당신이 내공진기를 끌어 모으지만 기가 흩어져 버립니다.[0;37m')
                    self.stopSkill()
                    return
                if  self.getHp() < (self.getMaxHp() * s.hp) / 100 or self.getHp() < (self.getMaxHp() * s.maxhp) / 100:
                    self.sendLine('[1m당신의 내공진기가 흩어지며 기의 순환이 멈추어 버립니다.[0;37m')
                    self.stopSkill()
                    return
                self['내공'] -= s.mp
                self['체력'] -= (self.getMaxHp() * s.hp) / 100
                self.skill.init()
                self.lpPrompt()
                
                #print self.skill.bonus
                self.addStr(self.skill.bonus, False)
                buf1, buf2, buf3 = self.makeFightScript(self.skill['무공스크립'], self.target[0])
                self.sendLine('\r\n' + buf1)
                self.sendRoomFightScript(buf3)
                if self.getDex() >= 4200:
                    self._advance = True
                    self.doFight(True)
                return True
        return False

    def fightMobNormal(self):
        tdmg = 0
        for mob in self.target:
            if len(mob.target) == 0 or mob.target[0] != self:
                continue
            if is_player(mob):
                continue
            type = ''
            more = False
            mob.dex += mob.getDex() +700
            if mob.skill != None:
                script, more, mob.dex = mob.skill.getScript(mob.dex)
                vCheck = False
                for s in script:
                    for r in s:
                        type = r
                        msg = s[r]
                        if type == '초식':
                            if self.checkConfig('수련모드') == False:
                                #print mob['이름']
                                buf1, buf2, buf3 = mob.makeFightScript(msg, self)
                                self.sendFightScript(buf2)
                        elif type == '공격':
                            chance = mob.getSkillChance(self)
                            if chance < randint(0, 100):
                                if self.checkConfig('수련모드') == False:
                                    buf1, buf2, buf3 = mob.makeFightScript(mob.skill['실패'], self)
                                    self.sendFightScript(buf2)
                            else:
                                if vCheck == False:
                                    self.checkVision(mob.skill)
                                    vCheck = True

                                dmg = mob.getSkillPoint(self)
                                vision = self['비전설정']
                                if vision != '':
                                    if mob.skill.name == vision.replace('비전', '') or \
                                        (mob.skill.name[:2] == '독' and mob.skill.name[2:].isdigit()):
                                        dmg = int(dmg/2)
                                   
                                tdmg += dmg
                                if self.checkConfig('수련모드') == False:
                                    buf1, buf2, buf3 = mob.makeFightScript(msg, self)
                                    self.sendFightScript(buf2 + ' [1;31m%d[0;37m' % dmg)
                                if self.minusHP(dmg):
                                    self.clearTarget()
                                    return -1
            if more == False and mob.skill != None:
                mob.stopSkill()
            if more == False or type == '대기':
                cnt = int(mob.dex / 700)
                mob.dex = mob.dex % 700
                for i in range(cnt):
                    chance = mob.getSkillChance(self)
                    if chance < randint(0, 100):
                        if self.checkConfig('수련모드') == False:
                            buf1, buf2, buf3 = mob.getAttackFailScript(self)
                            self.sendFightScript(buf2)
                    else:
                        dmg, c1, c2 = mob.getAttackPoint(self)
                        tdmg += dmg
                        
                        if self.checkConfig('수련모드') == False:
                            buf1, buf2, buf3 = mob.getAttackScript(self, dmg, c1, c2)
                            self.sendFightScript(buf2 +  ' [1;31m%d[0;37m' % dmg)
                        self.addAnger()
                        if self.minusHP(dmg):
                            self.clearTarget()
                            return -1
            self.startMobSkill(mob)
        return tdmg
        
    def fightNormal(self):
        pass
        
    def doFight(self, advance = False):
        if advance and self._advance:
            return
        #self.sendLine('%d' % self['힘경험치'])
        if len(self.target) == 0:
            self.act = ACT_STAND
            return
        c = 0
        tdmg = 0
        more = False
        if self.checkConfig('수련모드') == False:
            self.sendLine('')
        if advance == False:
            self.dex += self.getDex() + 700
        else:
            self.dex = self.getDex()
        
        # 혹시나 타겟이 다른룸에 있거나 활성화상태가 아닐때 타겟 정리
        target = copy.copy(self.target)
        for mob in target:
            if mob.env != self.env or mob.act > 1:
                self.clearTarget(mob)
        if len(self.target) == 0:
            self.act == ACT_STAND
            return
             
        target = copy.copy(self.target)
        mob = self.target[0]
        dmg = 1
        if target[0].get('전투종류') >= 1 or len(target) > 1 or self.fightMode == True:
            if advance == False:
                ret = self.fightMobNormal()
                if ret == -1:
                    return
                tdmg += ret
            type = ''
            if self.skill != None:
                script, more, self.dex = self.skill.getScript(self.dex)
                for s in script:
                    for r in s:
                        type = r
                        msg = s[r]
                        if type == '초식':
                            buf1, buf2, buf3 = self.makeFightScript(msg, mob)
                            self.sendFightScript(buf1)
                            self.checkItemSkill()
                        elif type == '공격':
                            target = copy.copy(self.target)
                            for mob in target:
                                chance = self.getSkillChance(mob)
                                if chance < randint(0, 100):
                                    if self.checkConfig('수련모드') == False:
                                        buf1, buf2, buf3 = self.makeFightScript(self.skill['실패'], mob)
                                        self.sendFightScript(buf1)
                                    self.checkItemSkill()
                                    #실패
                                    self.addDex(1)
                                    #무공 성 올림 체크해야함
                                    self.weaponSkillUp()
                                else:
                                    
                                    dmg = self.getSkillPoint(mob)
                                    if self.checkConfig('수련모드') == False:
                                        buf1, buf2, buf3 = self.makeFightScript(msg, mob)
                                        self.sendFightScript(buf1 + ' [1;36m%d[0;37m' % dmg)
                                    self.checkItemSkill()
                                    self.addStr(1)
                                    self.weaponSkillUp()
                                    if mob.minusHP(dmg, who = self['이름']):
                                        self.dex = 0
                                        #self.clearTarget(mob)
                                        if self.skill != None and self.skill.is_allAttack() == False:
                                            r = self.recoverDemage(tdmg)
                                            self['체력'] += r
                                            if len(self.target) != 0:
                                                self.stopSkill()
                                            self.lpPrompt()
                                            return
                                        if len(self.target) == 0:
                                            r = self.recoverDemage(tdmg)
                                            self['체력'] += r
                                            self.stopSkill()
                                            self.lpPrompt()
                                            return
                                        else:
                                            self.sendLine('')
                                if self.skill != None and self.skill.is_allAttack() == False:
                                    break
            if more == False and self.skill != None:
                self.skillUp()
                self.stopSkill()
            if more == False or type == '대기':
                cnt = int(self.dex / 700)
                self.dex = self.dex % 700
                for l in range(cnt):
                    chance = self.getAttackChance(mob)
                    if chance < randint(0, 100):
                        buf1, buf2, buf3 = self.getAttackFailScript(mob)
                        if self.checkConfig('수련모드') == False:
                            self.sendFightScript(buf1)
                        if is_player(mob) and mob.checkConfig('수련모드') == False:
                            mob.sendFightScript(buf2)
                        self.checkItemSkill()
                        self.addDex(1)
                        self.weaponSkillUp()
                    else:
                        
                        dmg, c1, c2 = self.getAttackPoint(mob)
                        buf1, buf2, buf3 = self.getAttackScript(mob, dmg, c1, c2)
                        if self.checkConfig('수련모드') == False:
                            self.sendFightScript(buf1 + ' [1;36m%d[0;37m' % dmg)
                        if is_player(mob) and mob.checkConfig('수련모드') == False:
                            mob.sendFightScript(buf2 + ' [1;31m%d[0;37m' % dmg)
                        self.checkItemSkill()
                        #self.sendLine('당신은 ' + target[0].getName() + han_obj(target[0].getName())+ ' 후려칩니다. %d' % dmg)
                        self.addStr(1)
                        self.weaponSkillUp()
                        if target[0].minusHP(dmg, who = self['이름']):
                            r = self.recoverDemage(tdmg)
                            self['체력'] += r
                            #self.clearTarget(target[0])
                            if len(self.target) != 0:
                                self.stopSkill()
                            self.lpPrompt()
                            return
        else:
            mob = self.target[0]
            type = ''
            if self.skill != None:
                script, more, self.dex = self.skill.getScript(self.dex)
                for s in script:
                    for r in s:
                        type = r
                        msg = s[r]
                        if type == '초식':
                            if self.checkConfig('수련모드') == False:
                                buf1, buf2, buf3 = self.makeFightScript(msg, mob)
                                self.sendFightScript(buf1)
                            self.checkItemSkill()
                        elif type == '공격':
                            chance = self.getSkillChance(mob)
                            if chance < randint(0, 100):
                                if self.checkConfig('수련모드') == False:
                                    buf1, buf2, buf3 = self.makeFightScript(self.skill['실패'], mob)
                                    self.sendFightScript(buf1)
                                self.checkItemSkill()
                                #실패
                                self.addDex(1)
                                #무공 성 올림 체크해야함
                                self.weaponSkillUp()
                            else:
                                dmg = self.getSkillPoint(mob)
                                if self.checkConfig('수련모드') == False:
                                    buf1, buf2, buf3 = self.makeFightScript(msg, mob)
                                    self.sendFightScript(buf1 + ' [1;36m%d[0;37m' % dmg)
                                self.checkItemSkill()
                                self.addStr(1)
                                self.weaponSkillUp()
                                if mob.minusHP(dmg, who = self['이름']):
                                    r = self.recoverDemage(tdmg)
                                    self['체력'] += r
                                    #self.clearTarget(mob)
                                    self.lpPrompt()
                                    return
            if more == False and self.skill != None:
                self.skillUp()
                self.stopSkill()
            if more == False or type == '대기':
                cnt = int(self.dex / 700)
                self.dex = self.dex % 700
                for l in range(cnt):
                    chance = self.getAttackChance(mob)
                    if chance < randint(0, 100):
                        if self.checkConfig('수련모드') == False:
                            buf1, buf2, buf3 = self.getAttackFailScript(mob)
                            self.sendFightScript(buf1)
                        if is_player(mob) and mob.checkConfig('수련모드') == False:
                            buf1, buf2, buf3 = self.getAttackFailScript(mob)
                            mob.sendFightScript(buf2)
                        self.checkItemSkill()
                        self.addDex(1)
                        self.weaponSkillUp()
                    else:
                        dmg, c1, c2 = self.getAttackPoint(mob)
                        if self.checkConfig('수련모드') == False:
                            buf1, buf2, buf3 = self.getAttackScript(mob, dmg, c1, c2)
                            self.sendFightScript(buf1 + ' [1;36m%d[0;37m' % dmg)
                        if is_player(mob) and mob.checkConfig('수련모드') == False:
                            buf1, buf2, buf3 = self.getAttackScript(mob, dmg, c1, c2)
                            mob.sendFightScript(buf2 + ' [1;31m%d[0;37m' % dmg)
                        self.checkItemSkill()
                        self.addStr(1)
                        self.weaponSkillUp()
                        if mob.minusHP(dmg, who = self['이름']):
                            r = self.recoverDemage(tdmg)
                            self['체력'] += r
                            #self.clearTarget(mob)
                            self.lpPrompt()
                            return
            if advance == False:
                ret = self.fightMobNormal()
                if ret == -1:
                    return
                tdmg += ret
        r = self.recoverDemage(tdmg)
        self['체력'] += r
        self.startSkill()
        if self.checkConfig('수련모드'):
            self.fightPrompt()
        else:
            self.lpPrompt()
        if len(self.target) != 0:
            mob = self.target[0]
            if is_player(mob) and mob.checkConfig('수련모드'):
                mob.fightPrompt()
            else:
                mob.lpPrompt()

    def startSkill(self):
        if self.skill != None:
            pass
        elif self.checkConfig('자동무공시전'):
            sName = self['자동무공']
            if sName != '':
                self.getSkill(sName)
                s = self.skill
                if self.getMp() < s.mp:
                    self.sendLine('[1m당신이 내공진기를 끌어 모으지만 기가 흩어져 버립니다.[0;37m')
                    self.stopSkill()
                    return
                if  self.getHp() < (self.getMaxHp() * s.hp) / 100 or self.getHp() < (self.getMaxHp() * s.maxhp) / 100:
                    self.sendLine('[1m당신의 내공진기가 흩어지며 기의 순환이 멈추어 버립니다.[0;37m')
                    self.stopSkill()
                    return
                self['내공'] -= s.mp
                self['체력'] -= (self.getMaxHp() * s.hp) / 100
                self.skill.init()
                #print self.skill.bonus
                self.addStr(self.skill.bonus)
                buf1, buf2, buf3 = self.makeFightScript(self.skill['무공스크립'], self.target[0])
                self.sendFightScript(buf1)
                #self.sendRoomFightScript(buf3)

    def doDeath(self):
        if self.stepDeath == 0:
            self.sendLine('\r\n기혈이 거꾸로 돌며 정신이 혼미해 집니다.')
            self.lpPrompt()
        elif self.stepDeath == 1:
            self.sendLine('\r\n누군가가 당신 주위를 어슬렁 거립니다.')
            self.lpPrompt()
        elif self.stepDeath == 2:
            self.sendLine('\r\n웅성 웅성 거리는 소리가 귓전에 맴돌며 점점 멀어져 갑니다.')
            self.lpPrompt()
        elif self.stepDeath == 3:
            room = getRoom('낙양성:7')
            self.enterRoom(room, '사망', '사망')
            self.lpPrompt()
        elif self.stepDeath == 4:
            self.sendLine('\r\n코끝을 찌르는 향냄새에 정신을 차려보니 장의사 내부다.')
            self.lpPrompt()
        elif self.stepDeath == 5:
            self.sendLine('\r\n장의사가 말합니다. "앗~~ 죽은줄 알았는데 다시 깨어나는군~"')
            self.lpPrompt()
        elif self.stepDeath == 6:
            self.sendLine('\r\n장의사가 말합니다. "하나뿐인 목숨 무모하게 행동하지 말고 조심해서 행동하게나."')
            self.lpPrompt()
        elif self.stepDeath == 7:
            self.sendLine('\r\n당신이 떠지지 않는 눈을 힘겹게 뜨며 주위를 살펴 봅니다.')
            self.lpPrompt()
        elif self.stepDeath == 8:
            # 보험가입 유무처리 필요
            if self.insure == 0:
                self.sendLine('\r\n장의사가 말합니다. "쯧쯧... 표국에서 보험을 들지 않았군..."')
                self.sendLine('                   "무리한 무공수련은 화를 자초한다네."')
            else:
                self.sendLine('\r\n장의사가 말합니다. \"자네가 가지고 다니던 물건은 표국에서 회수 해왔으니\"')
                self.sendLine('                   \"잃어버린 것이 없는지 확인해 보게나..\"')
                self.sendLine('                   \"표국무사가 그러는데 보험료가 나갔다더군...\"')
            self.lpPrompt()
        elif self.stepDeath == 9:
            self.sendLine('\r\n당신이 자세를 편안히 하며 운기조식에 들어갑니다.')
            self.sendLine(HIC + '당신의 기혈이 타동하기 시작합니다.' + '[0;37m')
            self.sendRoom('%s 자세를 편안히 하며 운기조식에 들어갑니다.' % self.han_iga())
            self.act = ACT_REST
            self.INTERACTIVE = 1
            self.input_to(self.parse_command)
            self.stepDeath = 0
            self.set('체력', int(self.get('최고체력') * 0.33))
            self.lpPrompt()
            return

        self.stepDeath += 1

    def recover(self):
        #체력회복
        hp = self.getHp()
        maxhp = self.getMaxHp()
        
        mp = self.getMp()
        maxmp = self.getMaxMp()
        
        if self.act == ACT_STAND:
            # 10% 회복
            r = 0.1
        elif self.act == ACT_REST:
            # 20% 회복
            r = 0.2
        elif self.act == ACT_FIGHT:
            # 5% 회복
            r = 0.05
        else:
            r = 0
        if hp < maxhp:
            hp += int (maxhp * r)
            if hp >= maxhp:
                hp = maxhp
            self.set('체력', hp)
        
        if mp < maxmp:
            mp += int (maxmp * r)
            if mp >= maxmp:
                mp = maxmp
            self.set('내공', mp)

    def doEmotion(self, cmd, line):
        kd = EMOTION[cmd].splitlines()
        sub = line
        if line == '':
            buf1, buf2, buf3 = EMOTION.makeScript(kd[0], self.getNameA(), None, line)
            self.sendLine(buf1)
            self.sendRoom(buf3)
            return
        l = line.split(None, 1)
        obj = self.env.findObjName(l[0])
        
        if obj == None or obj == self:
            buf1, buf2, buf3 = EMOTION.makeScript(kd[0], self.getNameA(), None, line)
            self.sendLine(buf1)
            self.sendRoom(buf3)
            return
        if is_mob(obj):
            sub = line[len(l[0]):].strip()
            buf1, buf2, buf3 = EMOTION.makeScript(kd[1], self.getNameA(), obj.getNameA(), sub)
            self.sendLine(buf1)
            self.sendRoom(buf3)
        elif is_player(obj):
            sub = line[len(l[0]):].strip()
            e = kd[1]
            if obj.checkConfig('접촉거부') and len(kd) == 3:
                e = kd[2]
            buf1, buf2, buf3 = EMOTION.makeScript(e, self.getNameA(), obj.getNameA(), sub)
            self.sendLine(buf1)
            self.sendRoom(buf3, ex = obj)
            obj.sendLine('\r\n' + buf2)
            obj.lpPrompt()
        else:
            buf1, buf2, buf3 = EMOTION.makeScript(kd[0], self.getNameA(), None, line)
            self.sendLine(buf1)
            self.sendRoom(buf3)
            
    def loadConfig(self):
        self.Configs = {}
        for cfg in self.CFG:
            self.Configs[cfg] = self._checkConfig(cfg)
    
    def checkConfig(self, cfg):
        if cfg not in self.Configs:
            return False
        return self.Configs[cfg]
        
    def _checkConfig(self, config):
        kl = self['설정상태'].splitlines()
        for k in kl:
            if k.find(config) == 0:
                if len(k.split()) > 1 and k.split()[1] == '1':
                    return True
                break
        return False
        
    def setConfig(self, config):
        c = ''
        find = False
        kl = self['설정상태'].splitlines()
        for k in kl:
            if k.find(config) == 0:
                find = True
                ks = k.split()
                if len(ks) > 1:
                    if ks[1] == '1':
                        c += ks[0] + ' 0\r\n'
                    else:
                        c += ks[0] + ' 1\r\n'
                continue
            c += k + '\r\n'
        if find == False:
            c += config + ' 1'
        self['설정상태'] = c
        
        self.loadConfig()
        
    def loadAlias(self):
        self.alias = {}
        s = self['줄임말리스트'].splitlines()
        for key in s:
            ss = key.split(None, 1)
            self.alias[ss[0]] = ss[1]
        
    def buildAlias(self):
        msg = ''
        for key in self.alias:
            msg += key + ' ' + self.alias[key] + '\r\n'
        self['줄임말리스트'] = msg
        
    def setAlias(self, key, data):
        if key in self.alias:
            self.sendLine('☞ 이미 설정되어 있는 줄임말입니다.')
            return False
        self.alias[key] = data
        self.buildAlias()
        return True
    
    def delAlias(self, key):
        if key not in self.alias:
            self.sendLine('☞ 줄임말이 설정되어 있지 않아요. ^^')
            return False
        self.alias.__delitem__(key)
        self.buildAlias()
        return True
    
    def sendRoomFightScript(self, line, noPrompt = False, ex = []):
        for obj in self.env.objs:
            if is_player(obj) and obj != self and obj not in ex and obj.checkConfig('타인전투출력거부') == False:
                obj.sendLine('\r\n' + line)
                if noPrompt == False:
                    obj.lpPrompt()
        
    def makeHome(self):
        room = Room()
        room.index = '사용자맵:%s' % self['이름']
        room.path = 'data/map/사용자맵/%s.map' % self['이름']
        room['이름'] = '%s의 방' % self['이름']
        room['존이름'] = '사용자맵'
        room['설명'] = '%s의 방이다.' % self['이름']
        room['출구'] = '낙양성 낙양성:1'
        room.setAttr('맵속성', '사용자전투금지')
        room['주인'] = self['이름']
        room.save()
        
def is_player(obj):
    return isinstance(obj, Player)


def init_commands():

    script = 'objs/event.py'
    l = {}
    g = {}
    try:
        execfile(script, g, l)
    except NameError:
        print 'error load event.py'
    from objs.player import Player

    Player.doEvent = l['doEvent']

    script = 'objs/magicitem.py'
    l = {}
    g = {}
    try:
        execfile(script, g, l)
    except NameError:
        print 'error load event.py'
    from objs.item import Item

    Item.MagicMap = l['MagicMap']
    Item.OptionName = l['OptionName']
    Item.applyMagic = l['applyMagic']

    script = 'objs/autoscript.py'
    l = {}
    g = {}
    try:
        #execfile(script, g, l)
        execfile(script)
    except NameError:
        print 'error load autoscript.py'

    #Player.autoScript = l['autoScript']
    Player.autoScript = locals()['autoScript']
    
    cmdList = Player.cmdList

    from glob import glob
    from os.path import split
    scripts = glob('cmds/' + '*.py')

    for script in scripts:
        try:
            execfile(script)
        except NameError:
            continue

        cmdClass = locals()['CmdObj']
        cmdName =  split(script)[-1][:-3]
        cmdList[cmdName] = cmdClass()

