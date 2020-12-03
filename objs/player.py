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

    CFG = ['�ڵ�����', '�񱳰ź�', '���˰ź�', '����ź�', '�����ź�', 
    '��ħ�ź�', '���ĸ��ź�', '��������', '�������', '��ħ������',
    '��ھȽðź�', '����ھȽðź�', '�����Ը޼����ź�', 
    'Ÿ��������°ź�', '�ڵ���������', '�����ź�', '���ø��', '���ð�����',
    '�ڵ�ä������']
	
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
        #print 'Delete!!! ' + self.get('�̸�')

    def getNameA(self):
        return '[1m' + self.get('�̸�') + '[0;37m'

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
	    buf = '\r\n[1;31m���[0;37m ' + self.getNameA() + '���� �����ϼ̽��ϴ�.'
            for ply in self.adultCH:
                ply.sendLine(buf)
                ply.lpPrompt()

        if self._talker != None:
            self._talker._talker = None
        self._talker = None

        self.clearItems()
        if self['�������'] == 1:
            return

        buf = ''
        nick = self['������ȣ']
        if nick == '':
            nick = '����'
        char = self['����']
        if char == '����':
            buf = '�� [[1m����[0;37m] ��[1m%s[0;37m��' % nick
        elif char == '����':
            buf = '�� [[1;33m�����̻�[0;37m] ��[1;33m%s[0;37m��' % nick
        elif char == '����':
            buf = '�� [[1;32m����[0;37m] ��[1;32m%s[0;37m��' % nick
        elif char == '����':
            buf = '�� [[1;31m����[0;37m] ��[1;31m%s[0;37m��' % nick
        elif char == '����Ĩ��':
            buf = '�� [[1;35m����Ĩ��[0;37m] ��[0;37m%s[0;37m��' % nick
        else:
            buf = '�� [[0;30;47m����[0;37;40m] '
        msg = '%s %s ��ȣ�� ���� �ʿ��� ���� �մϴ�.' % (buf, self.han_iga())
        self.channel.sendToAllInOut(msg, ex = self)

    def load(self, path):

        scr = load_script('data/user/' + path)

        if scr == None:
            return False

        try:
            self.attr = scr['����ڿ�����Ʈ']
        except:
            return False
        
        self.loadConfig()
        self.loadAlias()
        self.loadSkillList()
        self.loadSkillUp()
        
        items = None
        if '������' not in scr:
            return True

        items = scr['������']
        
        if type(items) == dict:
            items = [items]
        
        for item in items:
            obj = getItem(str(item['�ε���']))
            if obj == None:
                print '����ھ����� �ε� ���� : %s' % str(item['�ε���'])
            if obj != None:
                obj = obj.deepclone()
                if '�̸�' in item:
                    obj['�̸�'] = item['�̸�']
                if '�����̸�' in item:
                    obj['�����̸�'] = item['�����̸�']
                if '���ݷ�' in item:
                    obj['���ݷ�'] = item['���ݷ�']
                if '����' in item:
                    obj['����'] = item['����']
                if '�ⷮ' in item:
                    obj['�ⷮ'] = item['�ⷮ']
                if '����' in item:
                    obj.inUse = True
                    self.armor += getInt(obj['����'])
                    self.attpower += getInt(obj['���ݷ�'])
                    if obj['����'] == '����':
                        self.weaponItem = obj
                if '�����ۼӼ�' in item:
                    obj.set('�����ۼӼ�', item['�����ۼӼ�'])
                if '�ɼ�' in item:
                    obj.set('�ɼ�', item['�ɼ�'])
                    if obj.inUse:
                        option = obj.getOption()
                        if option != None:
                            for op in option:
                                if op == '��':
                                    self._str += option[op]
                                elif op == '��ø��':
                                    self._dex += option[op]
                                elif op == '����':
                                    self._arm += option[op]
                                elif op == 'ü��':
                                    self._maxhp += option[op]
                                elif op == '����':
                                    self._maxmp += option[op]
                                elif op == '�ʻ�':
                                    self._critical += option[op]
                                elif op == '��':
                                     self._criticalChance += option[op]
                                elif op == 'ȸ��':
                                    self._miss += option[op]
                                elif op == '����':
                                    self._hit += option[op]
                                elif op == '����ġ':
                                    self._exp += option[op]
                                elif op == '�����߰�':
                                    self._magicChance += option[op]

                if 'Ȯ�� �̸�' in item:
                    obj.set('Ȯ�� �̸�', item['Ȯ�� �̸�'])
                if 'ü��' in item:
                    obj.hp = item['ü��']
                #if '�ð�' in item:
                #    obj.set('�ð�', item['�ð�'])
                self.insert(obj)
            
        for memo in scr:
            if memo.find('�޸�') == 0:
                self.memo[memo] = scr[memo]
        
        return True
        
    def save(self, mode = True):
        if mode == True:
            self['����������ð�'] = int(time.time())
        self.buildSkillList()
        self.buildSkillUp()
        self.buildSkills()
        
        o = {}
        o['����ڿ�����Ʈ'] = self.attr

        items = []
        for item in self.objs:
            obj = {}
            obj['�ε���'] = item.index
            obj['�̸�'] = item.get('�̸�')
            obj['�����̸�'] = item['�����̸�'].splitlines()
            if item.get('���ݷ�') != '':
                obj['���ݷ�'] = item.get('���ݷ�')
            if item.get('����') != '':
                obj['����'] = item.get('����')
            if item.get('�ⷮ') != '':
                obj['�ⷮ'] = item.get('�ⷮ')
            if item.inUse:
                obj['����'] = item.get('����')
            if item.get('�ɼ�') != '':
                obj['�ɼ�'] = item.get('�ɼ�').splitlines()
            if item.get('�����ۼӼ�') != '':
                obj['�����ۼӼ�'] = item.get('�����ۼӼ�').splitlines()
            if item.get('Ȯ�� �̸�') != '':
                obj['Ȯ�� �̸�'] = item.get('Ȯ�� �̸�')
            if item.isOneItem():
                obj['�ð�'] = time.time()
            if item['����'] == 'ȣ��':
                try:
                    obj['ü��'] = item.hp
                except:
                    obj['ü��'] = item['ü��']
            items.append(obj)

        o['������'] = items

        for memo in self.memo:
            o[memo] = self.memo[memo]
            
        try:
            f = open('data/user/' + self.get('�̸�'), 'w')
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
        if self['�Ҽ�'] == '':
            return
        g = GUILD[self['�Ҽ�']]
        if '%s��Ī' % self['����'] in g:
            buf = g['%s��Ī' % self['����']]
        else:
            buf = self['����']
        for ply in self.channel.players:
            if ply.state == ACTIVE and ply['�Ҽ�'] == self['�Ҽ�'] and ply != ex and ply.checkConfig('���ĸ��ź�') == False:
                if ply != self:
                    ply.sendLine('')
                ply.sendLine('[1m��[36m%s[37m��[36m%s[37m��[0;37m ' % ( buf, self['�̸�'])+ line)
                if prompt and ply != self:
                    ply.lpPrompt()
                
    def sendFightScript(self, line):
        if self.checkConfig('���ø��') == False:
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
            ob.sendLine('������������������������������������������������������������')
            m = self.get('������ȣ')
            if m == '':
                m = '����'
            c = self.get('����')
            if c == '':
                c = '����'
            s = '��%s�� %s' % (m, self.get('�̸�'))
            ob.sendLine('[0m[44m[1m[37m�� ��  �� �� %-24s �� ���� �� ��%s��   [0m[37m[40m' % (s, c))
            m = self.get('�����')
            if m == '':
                m = '��ȥ'
            s = '��%s��' % m
            s1 = '%d��(%s)' %(self.get('����'), self.get('����'))
            ob.sendLine('[0m[44m[1m[37m�� ����� �� %-24s �� ���� �� %-9s  [0m[37m[40m' % (s, s1))
            m = self['�Ҽ�']
            if m != '':
                s = '�� ��  �� �� ��%s��' % m
                ob.sendLine('[0m[44m[1m[37m%-60s[0m[37m[40m' % s)
                g = GUILD[self['�Ҽ�']]
                if '%s��Ī' % self['����'] in g:
                    buf = g['%s��Ī' % self['����']]
                else:
                    buf = self['����']
                r = self['���ĺ�ȣ']
                if r == '':
                    s = '�� ��  �� �� ��%s��' % buf
                else:
                    s = '�� ��  �� �� ��%s(%s)��' % (buf, r)
                ob.sendLine('[0m[44m[1m[37m%-60s[0m[37m[40m' % s)

            ob.sendLine('������������������������������������������������������������')
            c = 0
            item_str = ''
            for lv in ob.ItemLevelList:
                for item in self.objs:
                    if item.inUse and lv == item['����']:
                        c += 1
                        item_str += '[' + ob.ItemUseLevel[item.get('����')] + '] [36m' + item.get('�̸�') + '[37m\r\n'
            ob.write(item_str)
            if c == 0:
                ob.sendLine('[36m�� �����ܽ� �Ǹ����� ��ȣ�� �������Դϴ�.[37m')
            ob.sendLine('������������������������������������������������������������')
            ob.sendLine('�� %s' % self.GetHPString())
            ob.sendLine('������������������������������������������������������������')
            
    def viewMapData(self):
        room = self.env
        if room == None:
            return

        # room Name
        
        msg = '\r\n[1;30m[[0;37m[[[1;37m[][1m %s [1;37m[][0;37m]][1;30m][0;37m' % room.get('�̸�')
        if getInt(self['�����ڵ��']) >= 1000:
            msg += ' (%s)' % (room.index)
        self.sendLine(msg)
        # room Desc
        if not self.checkConfig('��������'):
            self.sendLine ( '' )
            self.sendLine (room.get('����'))

        # room Exit �ա��
        if not self.checkConfig('��ħ������'):
            self.sendLine(room.longExitStr)
        else:
            self.sendLine(room.shortExitStr)
            self.sendLine ( '' )

        msg = '�� '
        for obj in room.objs:
            if is_box(obj):
                msg += obj.viewShort() + '    '
        if len(msg) != 3:
            self.sendLine(msg)

        for obj in room.objs:
            if is_mob(obj):
                if obj.get('������') == 7:
                    continue
                if obj.act == ACT_REGEN:
                    continue
                elif obj.act == ACT_REST:
                    self.sendLine(obj.han_iga() + ' ��Ʈ���� ���⸦ �߽����� �ֽ��ϴ�.')
                if obj.act == ACT_STAND:
                    self.sendLine(obj.getDesc1())
                elif obj.act == ACT_FIGHT:

                    msg = ''
                    for s in obj.skills:
                        msg += s['�����¸Ӹ���'] + ' '
                    self.sendLine('%s%s ����� �� ������ ���̰� �ֽ��ϴ�.' % (msg, obj.han_iga()))
                elif obj.act == ACT_DEATH:
                    self.sendLine(obj.getNameA() + '�� �δ��� ��ü�� �ֽ��ϴ�.')
        nStr = {} # { [], [], ... }
        for obj in room.objs:
            if is_item(obj):
                c = 0
                try:
                    l = nStr[obj.get('�̸�')]
                except:
                    l = [0, obj.get('����1')]
                    nStr[obj.get('�̸�')] = l
                l[0] = l[0] + 1

        for iName in nStr:
            l = nStr[iName]
            if l[0] == 1:
                self.sendLine( l[1].replace('$������$', '[36m' + iName + '[37m') )
            else:
                self.sendLine( l[1].replace('$������$', '[36m' + iName + '[37m %d��' % l[0]) )

        for obj in room.objs:
            if is_player(obj) and obj != self:
                if obj['�������'] == 1:
                    continue
                self.sendLine(obj.getDesc())

    def getDesc(self, myself = False):
        msg = ''
        if myself == False:
            s = self['���ĺ�ȣ']
            if s != '':
                msg = '[1m��%s��[0m' % s
            for s in self.skills:
                msg += s['�����¸Ӹ���'] + ' '
        if self['�Ӹ���'] != '':
            msg += str(self['�Ӹ���']) + ' '
        if myself == True:
            msg += '����� '
        else:
            msg += self.han_iga() + ' '
        if self['������'] != '':
            msg += str(self['������']) + ' '
            
        # act �� ���� ������ �޸��ؾ���
        if self.act == ACT_STAND:
            msg += '�� �ֽ��ϴ�.'
        elif self.act == ACT_REST:
            msg += '��������� �ϰ� �ֽ��ϴ�.'
        elif self.act == ACT_FIGHT:
            msg += '����� �� ������ ���̰� �ֽ��ϴ�.'
        elif self.act == ACT_DEATH:
            msg += '������ �ֽ��ϴ�.'
            
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
            if is_player(obj) and obj != self and obj not in exList and obj.checkConfig('Ÿ��������°ź�') == False:
                obj.sendLine('\r\n' + line)
                if noPrompt == False:
                        obj.lpPrompt()
            
    def autoMove(self, line):
        if line[1] == self.env:
            self.do_command(line[0])
        else:
            idDelayedCall = 0

    def enterRoom(self, room, move = '', mode = ''):
        if self.isMovable() == False and  mode != '��ȯ' and mode != '����':
            self.sendLine('�� ���� �̵��ϱ⿡�� ���� ��Ȳ�� �ƴϳ׿�. ^_^')
            return False

        li = getInt(room['��������'])
        if li > 0 and li < self['����']:
            self.sendLine('���� ������ ����� ����� �й��մϴ�.')
            return False

        if getInt(room['��������']) > self['����']:
            self.sendLine('���� ������ ����� ����� �й��մϴ�.')
            return False

        li = getInt(room['����������'])
        if li > 0 and li < self['��']:
            self.sendLine('���� ������ ����� ����� �й��մϴ�.')
            return False

        li = getInt(room['��ø��������'])
        if li > 0 and li < self.getDex():
            self.sendLine('���� ������ ����� ����� �й��մϴ�.')
            return False

        if room.checkLimitNum():
            self.sendLine('�� �� �� ���� ������ ����� ����� ���θ����ϴ�. ^_^')
            return False
        if room.checkAttr('�������Ա���') and self['����'] == '����':
            self.sendLine('�� ���Ĵ� ������ �� ���� ���̶��!')
            return False
        if room.checkAttr('�������Ա���') and self['����'] == '����':
            self.sendLine('�� ���Ĵ� ������ �� ���� ���̶��!')
            return False
        if room['��������'] != '' and room['��������'] != self['�Ҽ�']:
            self.sendLine('�� �װ��� Ÿ ������ �����̹Ƿ� �����Ͻ� �� �����ϴ�.')
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
            if is_mob(mob) and mob.get('�̺�Ʈ $%�����̺�Ʈ%') != '':
                #mob.doEvent(player, '�̺�Ʈ $%�����̺�Ʈ%', [])
                self.doEvent(mob, '�̺�Ʈ $%�����̺�Ʈ%', [])

        if self['�������'] != 1:
            txt = self.env.get('���Խ�ũ��:' + move)
            if txt != '':
                # ���� �̵��� �ο���ŭ �̵� �� ������Ʈ�� ���
                buf = txt.replace('[��]', self.getNameA())
                buf = postPosition1(buf)
                self.writeRoom('\r\n' + buf)
            else:
                if mode == '����':
                    buf = ''
                    nick = self['������ȣ']
                    if nick == '':
                        nick = '����'
                    char = self['����']
                    if char == '����':
                        buf = '�� [[1m����[0;37m] ��[1m%s[0;37m��' % nick
                    elif char == '����':
                        buf = '�� [[1;33m�����̻�[0;37m] ��[1;33m%s[0;37m��' % nick
                    elif char == '����':
                        buf = '�� [[1;32m����[0;37m] ��[1;32m%s[0;37m��' % nick
                    elif char == '����':
                        buf = '�� [[1;31m����[0;37m] ��[1;31m%s[0;37m��' % nick
                    elif char == '����Ĩ��':
                        buf = '�� [[1;35m����Ĩ��[0;37m] ��[0;37m%s[0;37m��' % nick
                    else:
                        buf = '�� [[0;30;47m����[0;37;40m] '
                    msg = '%s %s [1;36m���������� �޲ٸ� ��ȣ�� ����մϴ�.[0;37m' % (buf, self.han_iga())
                    self.channel.sendToAllInOut(msg, ex = self)
                if mode == '��ȯ':
                    self.writeRoom('\r\n%s �ϴÿ��� ����� ���� �ɽ��ϴ�. \'ô~~~\'' % self.han_iga())
                elif mode == '��ȯ':
                    self.writeRoom('\r\n%s �˼� ���� �� ���ο� ��Ÿ���ϴ�. \'�������~~~\'' % self.han_iga())
                elif mode == '����':
                    self.writeRoom('\r\n%s ������ ��Ʋ�Ÿ��� ������ �����ɴϴ�. \'����~~\' '  % self.han_iga())
                elif mode == '���':
                    self.sendRoom('%s �ռ����� �Ƿ��ɴϴ�.' % self.han_iga())
                else:
                    #����/����/�����Ŀ� ���� �ٸ�
                    self.sendRoom('%s �Խ��ϴ�.'% self.han_iga())

        for attr in room.mapAttr:
            if attr.find('ü�°���') == 0:
                dmg = attr.split(None, 2)[1]
                msg = attr.split(None, 2)[2]
                self.lpPrompt()
                buf = msg.replace('[��]', '���')
                buf = postPosition1(buf)
                self.sendLine('\r\n' + buf)
                buf = msg.replace('[��]', self.getNameA())
                buf = postPosition1(buf)
                self.sendRoom(buf)
                if self.minusHP(getInt(dmg), False):
                    return True
                break
        c = 0
        #�濡 �ִ� ������ ó��
        if self['�������'] != 1:
            for obj in room.objs:
                if is_mob(obj) and obj not in self.target and obj.act == ACT_STAND:
                    if obj.get('��������') == 1:
                        self.lpPrompt()
                        self.setFight(obj, True)
                        c += 1
                        break;
        if c > 0:
            self.doSkill()
            #self.lpPrompt()

        auto = room.get('�ڵ��̵�')
        if auto != '':
            self.idDelayedCall = reactor.callLater( 1, self.autoMove, [auto.split()[0], room] )
        
        for f in self.follower:
            if f.env == prev and mode == '�̵�':
                reactor.callLater(0, f.do_command, move)

        if auto == '' and len(self.target) == 0:
            reactor.callLater(0.1, self.moveNext)
            #self.moveNext()

        return True

    def exitRoom(self, move = '', mode = ''):
        if self.env != None  and self['�������'] != 1:
            txt = self.env.get('�̵���ũ��:' + move)
            if txt != '':
                # ���� �̵��� �ο���ŭ �̵� �� ������Ʈ�� ���
                buf = txt.replace('[��]', '���')
                buf = postPosition1(buf)
                self.sendLine('\r\n' + buf)
                buf = txt.replace('[��]', self.getNameA())
                buf = postPosition1(buf)
                self.sendRoom('\r\n' + buf)

            else:
                if mode == '��ȯ':
                    self.sendLine('����� ������� ��ġ�� �ϴ÷� ġ�ھ� �����ϴ�. \'��������!!!\'')
                    self.writeRoom('\r\n%s ������� ��ġ�� �ϴ÷� ġ�ھ� �����ϴ�. \'��������!!!\'' % self.han_iga())
                elif mode == '��ȯ':
                    self.sendLine('����� �˼� ���� �� �ָ��� ������ϴ�. \'�������~~~\'')
                    self.writeRoom('\r\n%s �˼� ���� �� �ָ��� ������ϴ�. \'�������~~~\'' % self.han_iga())
                elif mode == '����':
                    self.sendLine('����� ������ ��Ʋ�Ÿ��� ������ �������ϴ�. \'�츮��~~\'')
                    self.writeRoom('\r\n%s ������ ��Ʋ�Ÿ��� ������ �������ϴ�. \'�츮��~~\'' % self.han_iga())
                elif mode == '���':
                    self.sendRoom('[1m���ǻ�[0;37m�� %s �������ϴ�.' % self.han_obj())
                elif mode == '���������̵�':
                    self.sendRoom('%s ���ڱ� ���а� ������ϴ�.' % self.han_iga())
                else:
                    msg = '%s %s������ �����ϴ�.\r\n'% ( self.han_iga(), move)
                    self.sendRoom(msg[:-2] , ex = self.follower)
                    for f in self.follower:
                        if f.env == self.env and mode == '�̵�':
                            f.sendLine('\r\n' + msg + '����� %s������ %s ���󰩴ϴ�.' % (move, self.han_obj()))
            self.env.remove(self)
        if self.env != None  and self['�������'] == 1:
            self.env.remove(self)

    def welcome(self):
        from lib.io import cat
        cat(self, 'data/text/logoMurim.txt')
        self.sendLine(WHT+BBLK + '�������� �Ҹ���� ������ �˷��ּ���. (ó�� ���ô� ���� [1m����[0;40m�̶�� �ϼ���)')
        self.write('�������Ԣ�')
        self.input_to(self.get_name)

    def lpPrompt(self, mode = False):
        if not self.checkConfig('�������'):
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
        return self.get('����1').replace('$������$', self.get('�̸�'))

    def die(self, mode = True):
        self.act = ACT_DEATH
        self._str = 0
        self._dex = 0
        self._arm = 0
        self.autoMoveList = []
        
        self.unwearAll()
        if mode:
            self.sendLine('\r\n[1;37m����� �������ϴ�. \'���~~ ö�۴�~~\'[0;37m')
        self.dropAllItem()
        self.sendLine('����� ������ ȥ���մϴ�.')
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
            self.sendLine('\r\n����� ������ ȥ���մϴ�.')

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
        return self.checkAttr('�̺�Ʈ��������Ʈ', e)

    def setEvent(self, e):
        self.setAttr('�̺�Ʈ��������Ʈ', e)

    def delEvent(self, e):
        self.delAttr('�̺�Ʈ��������Ʈ', e)
        
    def checkArmed(self, level):
        for item in self.objs:
            if item.inUse and item.get('����') == level:
                return True
        return False

    def checkItemIndex(self, index, cnt = 1):
        c = 0
        if index == '����':
            m = self.get('����')
            if cnt < 1:
                return False
            if m < cnt:
                return False
            return True

        if index == '����':
            m = self.get('����')
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
        if name == '����':
            if cnt < 1:
                return False
            m = self.get('����')
            if m < cnt:
                return False
            return True

        if name == '����':
            if cnt < 1:
                return False
            m = self.get('����')
            if m < cnt:
                return False
            return True

        for item in self.objs:
            if item.inUse:
                continue
            if stripANSI(item.get('�̸�')) == name:
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
            if item.getStrip('�̸�') == name:
                c = c + 1
                if cnt == c:
                    return item
        return None

    def addItem(self, index, cnt = 1, gamble = 0):
        c = 0
        if index == '����':
            m = self.get('����')
            m = m + cnt
            self.set('����', m)
            return

        if index == '����':
            m = self.get('����')
            m = m + cnt
            self.set('����', m)
            return

        item = getItem(index)
        if item == None:
            return
        for i in range(cnt):
            obj = item.deepclone()
            if obj.isOneItem():
                ONEITEM.have(index, self['�̸�'])
            if cnt == 1:
                obj.applyMagic(self['����'], 0, 1)
                if gamble != 0:
                    obj.setAttr('�����ۼӼ�', '����������')
                    obj.setAttr('�����ۼӼ�', '�ټ�����')
            self.insert(obj)

    def delItem(self, index, cnt = 1):
        c = 0
        if index == '����':
            m = self.get('����')
            m -= cnt
            self.set('����',m)
            return

        if index == '����':
            m = self.get('����')
            m -= cnt
            self.set('����',m)
            return

        objs = copy.copy(self.objs)
        for item in objs:
            if item.index == index:
                if item.inUse:
                    self.armor -= getInt(item['����'])
                    self.attpower -= getInt(item['���ݷ�'])
                    option = item.getOption()
                    if option != None:
                        for op in option:
                            if op == '��':
                                self._str -= option[op]
                            elif op == '��ø��':
                                self._dex -= option[op]
                            elif op == '����':
                                self._arm -= option[op]
                            elif op == 'ü��':
                                self._maxhp -= option[op]
                            elif op == '����':
                                self._maxmp -= option[op]
                            elif op == '�ʻ�':
                                self._critical -= option[op]
                            elif op == '��':
                                 self._criticalChance -= option[op]
                            elif op == 'ȸ��':
                                self._miss -= option[op]
                            elif op == '����':
                                self._hit -= option[op]
                            elif op == '����ġ':
                                self._exp -= option[op]
                            elif op == '�����߰�':
                                self._magicChance -= option[op]
                            
                self.remove(item)
                c += 1
                if cnt == c:
                    break

    def getTendency(self, line):
        type = line.strip()
        p1 = self['0 ������ų']
        p2 = self['1 ������ų']
        p3 = self['2 ������ų']
        
        if type == '�ϼ�':
            if self.get('������ȣ') != '':
                return True
            return False
        elif type == '����':
            if p1 + p2 + p3 < MAIN_CONFIG['������ȣ�̺�Ʈų��'] or p3 > p2:
                return False
            return True
        elif type == '����':
            if p1 + p2 + p3 < MAIN_CONFIG['������ȣ�̺�Ʈų��'] or p2 > p3:
                return False
            return True

    def printScript(self, line):
        l1 = line.replace('[��]', '���')
        l2 = postPosition1(l1)
        self.sendLine(l2)
        l1 = line.replace('[��]', self.getNameA())
        l2 = postPosition1(l1)
        self.sendRoom(l2)

    def addMugong(self, line):
        if line.strip() not in self.skillList:
            self.skillList.append(line.strip())


    def delMugong(self, line):
        m = line.strip()
        ms = self.get('�����̸�').splitlines()
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
        p1 = self.get('��')
        p1 = p1 - 2000
        if p1 < 15:
            p1 = 15        
        self.set('��', p1)
        self.set('����', 1)
        self.set('�������ġ', 0)
        self.set('������ġ', 0)
        self.set('��������ġ', 0)
        self.set('��������', self.get('����'))
        self.set('����', '����Ĩ��')
        self.set('�������������۸���Ʈ', '')
        self.set('�̺�Ʈ��������Ʈ', '����Ĩ�ų�')

    def setSunIn(self):
        self.set('��������', self.get('����'))
        self.set('����', '����')
        self.set('�������������۸���Ʈ', '')
        self.set('�̺�Ʈ��������Ʈ', '��ȭ���')

    def setGiIn(self):
        p1 = self.get('��')
        p1 = p1 - 600
        if p1 < 15:
            p1 = 15
        self.set('��', p1)
        self.set('����', 15)
        self.set('����', 1)
        self.set('�������ġ', 0)
        self.set('������ġ', 0)
        self.set('��������ġ', 0)
        self.set('��������', self.get('����'))
        self.set('����', '����')
        self.set('�������������۸���Ʈ', '')
        self.set('�̺�Ʈ��������Ʈ', '�ҿ���ȣ��')

    def get_name(self, name, *args):
        self.loginRetry += 1
        if self.loginRetry > 2:
            self.channel.transport.loseConnection()
            return
        #self.channel.transport.loseConnection()
        if len(name) == 0:
            self.write('\r\n�������Ԣ�')
            return
        if is_han(name) == False:
            self.write('�ѱ� �Է¸� �����մϴ�.\r\n�������Ԣ�')
            return
        if name == '����':
            #if self.checkMulti():
            #    return
            self.input_to(self.doNothing)
            self.state = sDOUMI
            from objs.doumi import DOUMI, autoScript
            self.autoscript = autoScript()
            self.autoscript.start(DOUMI['�ʱ⵵���'].splitlines(), self)
            return
        if name == '�����ٶ��':
            #if self.checkMulti():
            #    return
            self.input_to(self.doNothing)
            from objs.doumi import DOUMI, autoScript
            self.autoscript = autoScript()
            self.autoscript.start(DOUMI['���������'].splitlines(), self)
            return

        from client import Client
        for p in Client.players:
            if p.get('�̸�') == name and p != self and p.state != INACTIVE:
                self.sendLine('�� �̹� �������� Ȱ���� �Դϴ�.\r\n')
                self.write('�������Ԣ�')
                return

        res = self.load(name)
        if res == False:
            self.write('�׷� ����ڴ� �����ϴ�.\r\n�������Ԣ�')
            return

        # ip �ߺ� �˻�/������ �н�
        #if self.checkMulti():
        #    return

        curtime = time.time()
        c = getInt(self['��������'])
        if c != 0:
            if curtime - c < getInt(MAIN_CONFIG['���������ѽð�']):
                self.sendLine('\r\n%d �� �ڿ� �������Ͻʽÿ�.\r\n' % (getInt(MAIN_CONFIG['���������ѽð�']) - (curtime - c)) )
                self.channel.transport.loseConnection()
                return
        
        #self.set('�̸�', name)
        self.write('���Ծ�ȣ��')
        self.loginRetry = 0
        self.input_to(self.get_pass)

    def checkMulti(self):
        if getInt(self['�����ڵ��']) > 0:
            return False

        if self['��Ƽ����'] == 1:
            return False

        ip = self.channel.transport.getPeer().host
        cnt = 0
        for ply in self.channel.players:
            if ply.channel.transport.getPeer().host == ip:
                cnt += 1

        if cnt < 4:
            return False

        self.sendLine('\r\n�ߺ� ������ �����մϴ�.\r\n')
        self.channel.transport.loseConnection()
        return True

    def get_oldpass(self, line, *args):
        if line.strip() != str(self['��ȣ']):
            self.sendLine('�� ������ ��ȣ�� ���� �ʾƿ�. ^^')
            self.INTERACTIVE = 1
            self.input_to(self.parse_command)
            return
        self.write('�� ���� �Ͻ� ��ȣ�� �Է����ּ���. \r\n���Ծ�ȣ��')
        self.input_to(self.change_password)
    
    def change_password(self, line, *args):
        self._pass = line
        self.write('�� �ѹ� �� ��ȣ�� �Է����ּ���. \r\n��ȣȮ�΢�')
        self.input_to(self.change_password1)
    
    def change_password1(self, line, *args):
        if line != self._pass:
            self.sendLine('�� ���� �Է°� �ٸ��ϴ�. ��ȣ������ ����մϴ�.')
            self.INTERACTIVE = 1
            self.input_to(self.parse_command)
            return
        self['��ȣ'] = line
        self.write('�� ��ȣ�� ����Ǿ����ϴ�.')
        self.INTERACTIVE = 1
        self.input_to(self.parse_command)
        
    def get_pass(self, line, *args):
        self.loginRetry += 1
        if len(line) == 0 or str(self.get('��ȣ')) != line:
            if self.loginRetry >= 3:
                self.write('\r\n')
                self.channel.transport.loseConnection()
                return
            self.write('�߸��� ��ȣ �Դϴ�.\r\n���Ծ�ȣ��')
            return
        del self.loginRetry

        from client import Client
        for p in Client.players:
            if p['�̸�'] == self['�̸�'] and p != self and p.state != INACTIVE:
                self.sendLine('�� �̹� �������� Ȱ���� �Դϴ�.\r\n')
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
            self.write('�� �ѱ��� �̻� �Է��ϼ���.\r\n�������Ԣ�')
            return
        if len(name) > 10:
            self.write('�� ����Ͻ÷��� ������ �ʹ� ����.\r\n�������Ԣ�')
            return
        if is_han(name) == False:
            self.write('�� �ѱ� �Է¸� �����մϴ�.\r\n�������Ԣ�')
            return
        if name == '����':
            self.write('�� ����� �� ���� �����Դϴ�. �ѱ۷� �Է����ּ���.\r\n�������Ԣ�')
            return
        import os
        if os.path.exists(USER_PATH + name) == True:
            self.write('�� �̹� �������� Ȱ���� �Դϴ�.\r\n�������Ԣ�')
            return
        for ply in self.channel.players:
            if ply['�̸�'] == name:
                self.write('�� �̹� �������� Ȱ���� �Դϴ�.\r\n�������Ԣ�')
                return
        self.set('�̸�', name)
        self.init_body()
        item = getItem('368').deepclone()
        self.insert(item)
        #self.channel.players.append(self)
        self.input_to(self.doNothing)
        self.autoscript.run()
        #self.write('\r\n�մ����� ���մϴ�. "%s��� �մϴ�."' % name + '\r\n������ ���մϴ�. "��! ���� �̸��̱� �׷��ٸ� ��ȣ��??"\r\n���Ծ�ȣ��')
        #self.input_to(self.getNewpass)

    def getNewpass(self, line, *args):
        if len(line) < 3:
            self.write('\r\n�� 3�� �̻� �Է��ϼ���.\r\n���Ծ�ȣ��')
            return
        self.set('��ȣ', line)
        self.write('\r\n��ȣȮ�΢�')
        self.input_to(self.getNewpass2)

    def getNewpass2(self, line, *args):
        if line != self.get('��ȣ'):
            self.write('\r\n�� ������ ��ȣ�� ��ġ���� �ʴ±���.\r\n���Ծ�ȣ��')
            self.input_to(self.getNewpass)
            return
        self.input_to(self.doNothing)
        self.autoscript.run()
        #self.write('\r\n������ ���մϴ�. "�׷��� �׾��̴� �����ΰ�? �����ΰ�?"\r\n����(��/��)��')
        #self.input_to(self.getSex)

    def getSex(self, line, *args):
        if line not in ['��', '��']:
            self.write('\r\n�� [��], [��]�� �����ּ���.\r\n����(��/��)��')
            return
        self.set('����', line)
        self.input_to(self.doNothing)
        self.autoscript.run()
        
    def showNotice(self):
        self.write('[0m[37m[40m[H[2J')
        from lib.io import cat
        cat(self, 'data/text/notice.txt')
        self.write('[����Ű�� ��������]')
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
            self.sendLine('�ۼ��� ��Ĩ�ϴ�.')
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
            self.sendLine('�ۼ��� ��Ĩ�ϴ�.')
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
                if ply['�̸�'] == self._memoWho['�̸�']:
                    found = True
                    break
            if found:
                self.sendLine('����ڰ� �����Ͽ����Ƿ� �ۼ��� ��Ĩ�ϴ�.')
            else:
                if l >= 10:
                    msg += '���ѿ뷮�� �ʰ��Ͽ����ϴ�.\r\n'
                msg += '���� �ۼ��� ��Ĩ�ϴ�.'
                self._memo['����'] = self._memoBody
                self._memoWho.memo['�޸�:%s' % self['�̸�']] = self._memo
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
        rName = self.get('��ȯ����')
        if rName == '':
            rName = '���缺:42'
        room = getRoom(rName)
        last = self['����������ð�']
        if last != '':
            self.sendLine('������ ���� �ð� : %s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last)))
        if room != None:
            self.enterRoom(room, '����', '����')
        else:
            self.sendLine('���۸� ����!!!')
        
        l = len(self.memo)

        if l > 0:
            msg = '[1m��[0;37m ������ ������ %d�� �ֽ��ϴ�.\r\n   ���������ҿ� ���� ������ Ȯ���غ��ñ� �ٶ��ϴ�.' % l
            self.sendLine(msg)
        self.INTERACTIVE = 1

        v = self['Ư��ġ']
        if v == '':
            self['Ư��ġ'] = int(self['�ְ�ü��'] / 300)
            self.save()

        if self.checkConfig('�ڵ�ä������'):
            buf = '\r\n[1;31m���[0;37m ' + self.getNameA() + '���� �����ϼ̽��ϴ�.'
            for ply in self.adultCH:
                ply.sendLine(buf)
                ply.lpPrompt()

            self.adultCH.append(self)
            self.sendLine('�� ä�ο� �����մϴ�.')
            
        self.input_to(self.parse_command)

    def do_command(self, line, noPrompt = False):
        self.parse_command(line)
        if noPrompt == False:
            self.lpPrompt()

    def parse_command(self, line, *args):
        if self.env == None:
            print self['�̸�']
            return

        if getInt(self['�����ڵ��']) < 2000:
            self.cmdCnt += 1
            if self.cmdCnt > MAIN_CONFIG['�Է��ʰ�����']:
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
                self.sendLine('�� ������������ ��� ��ŵ� �Ұ����մϴ�.')
                return
            Player.cmdList['��'].cmd(self, line)
            return

        cmds = line.split()
        if len(cmds) == 0:
            return
        cmd = cmds[-1]
        argc = len(cmds)
        param = line.rstrip(cmd)
        param = param.strip()

        if self.env != None and cmd in self.env.limitCmds:
            self.sendLine('�̰����� �� ����� ����� �� �����ϴ�.')
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
                #    self.sendLine('��ø�� ���Ӹ��� ����� �� �����ϴ�.')
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
                mode = '�̵�'
                if cmd + '$' in self.env.exitList:
                    mode = '���������̵�'
                self.enterRoom(room, cmd, mode)
                return
            else:
                if cmd in ['��', '��', '��', '��', '��', '�Ʒ�', '�ϵ�', '�ϼ�', '����', '����']:
                    self.sendLine('�� ���� �������δ� ���� �� �����ϴ�.')
                    return
                for exitName in self.env.Exits:
                    if exitName.find(cmd) == 0:
                        room = self.env.getExit(exitName)
                        if room == None:
                            self.sendLine('Move where?')
                            return
                        mode = '�̵�'
                        if exitName + '$' in self.env.exitList:
                            mode = '���������̵�'
                        self.enterRoom(room, exitName, mode)
                        return

        if cmd in ('��', '����') and argc == 1:
            if self.isMovable() == False:
                self.sendLine('�� ������ ������ �����⿡ ���� ��Ȳ�� �ƴϳ׿�. ^_^')
                return
            self.INTERACTIVE = 2
            self.sendLine('\r\n������ �� ������~!!!')
            #broadcast(self.get('�̸�') + '���� �����̽��ϴ�.', self)
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
                self.sendLine('�� ������������ ��� ��ŵ� �Ұ����մϴ�.')
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
            obj = self.env['������Ʈ:'+cmd]
        if obj != '':
            self.sendLine(obj)
            return
        self.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')

    def checkInput(self, line, *args):
        if line == '��':
            self.autoscript.run()
            return
        if line == '���':
            self.sendLine('�� ����մϴ�. *^_^*')
            self.stopAutoScript()
            return 
        self.sendLine('�� ����Ͻ÷��� ����ҡ��� �Է� �ϼ���. *^_^*')
        return 

    def getLines(self, line, *args):
        limit = 5
        if len(args) != 0:
            limit = int(args[0])
        line = line.strip()
        if line == '':
            self.sendLine('�� ����Ͻ÷��� ����ҡ��� �Է� �ϼ���. *^_^*')
            return 
        if line == '.':
            if len(self.temp_input) == 0:
                self.sendLine('�� ���� �̻� �Է��ϼ���. *^_^*')
                return 
            self.autoscript.run()
            return 
        if len(line) > 42:
            self.sendLine('�� �ʹ�����. *^_^*')
            return
        if line == '���':
            self.sendLine('�� ����մϴ�. *^_^*')
            self.stopAutoScript()
            return 
        self.temp_input.append(line)
        if len(self.temp_input) >= limit:
            self.sendLine('�� �Է��� ��Ĩ�ϴ�. *^_^*')
            self.autoscript.run()
            return

    def getLine(self, line, *args):
        limit = 70
        line = line.strip()
        if line == '':
            self.sendLine('�� ����Ͻ÷��� ����ҡ��� �Է� �ϼ���. *^_^*')
            return 
        if line == '���':
            self.sendLine('�� ����մϴ�. *^_^*')
            self.stopAutoScript()
            return 
        if len(stripANSI(line)) > limit:
            self.sendLine('�� �ʹ�����. *^_^*')
            return
        self.temp_input = line
        self.autoscript.run()

    def getWord(self, line, *args):
        limit = args[0]
        keywords = args[1]
        line = line.strip()
        if line == '':
            self.sendLine('�� ����Ͻ÷��� ����ҡ��� �Է� �ϼ���. *^_^*')
            return 
        if ' ' in line:
            self.sendLine('�� ������ ���ԵǾ� �ֽ��ϴ�. �ٽ� �Է��ϼ���. *^_^*')
            return 
        if line == '���':
            self.sendLine('�� ����մϴ�. *^_^*')
            self.stopAutoScript()
            return 
        if len(stripANSI(line)) > limit:
            self.sendLine('�� �ʹ�����. *^_^*')
            return
        if line not in keywords and len(keywords) > 0:
            self.sendLine('�� �߸� �Է��ϼ̾��. *^_^*')
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
            self.sendLine('��%s���� �Է� �ϼ���\r\n>' % args)
            
    def pressEnter(self, line, *args):
        self.INTERACTIVE = 1
        self.input_to(self.parse_command)

    def getFightStartStr(self):
        w = self.getWeapon()
        if w == None:
            buf1 = '����� �ָ��� ��� ���� �մϴ�.'
            buf2 = '%s �ָ��� ��� ���� �մϴ�.' % self.han_iga()
        else:
            buf1 = '����� %s' % w['��������']
            buf2 = '%s %s' % (self.han_iga(), w['��������'])
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
        
        #�濡 �ִ� �հ��� ó��(������)
        for obj in self.env.objs:
            if is_mob(obj) and obj not in self.target and obj.act == ACT_STAND:
                if obj.get('��������') == 1 or obj.get('��������') == 2:
                    self.setTarget(obj)
                    obj.setTarget(self)
                    buf1, buf2 = obj.getFightStartStr()
                    self.sendLine(buf1)
                    obj.stopSkill()
                    self.startMobSkill(obj)
        
    def startMobSkill(self, mob):
        if mob.setSkill() and self.checkConfig('���ø��') == False:
            buf1, buf2, buf3 = mob.makeFightScript(mob.skill['������ũ��'], self)
            self.sendLine(buf2)
            self.sendRoomFightScript(buf3)
            
    def update(self):
        self._advance = False

        if self.cmdCnt > MAIN_CONFIG['�Է��ʰ�������']:
            self['��������'] = int(time.time())
            self.channel.transport.loseConnection()
            return
        self.cmdCnt = 0
        self.tick += 1
        self['���̿���ƽ'] += 1
        if self['���̿���ƽ'] >= MAIN_CONFIG['���̿���ƽ']: #24�ð��� 1��
            self['���̿���ƽ'] = 0
            self['����'] += 1
            if self['����'] % 60 == 0:
                self['�ְ���'] += 60
            else:
                self['�ְ���'] +=1
            self.sendRoom('[1m' + self['�̸�'] + '�� ������ ȸ������ ����ġ�� �������� �Ͼ� ���Ⱑ �ɵ��ϴ�.[0;37m')
            self.sendLine('\r\n[1m����� ������ ȸ������ ����ġ�� �������� �Ͼ� ���Ⱑ �ɵ��ϴ�.[0;37m')
            self.lpPrompt()
        if self.tick % 60 == 0:
            if self['������ȣ'] == '' and self['0 ������ų'] + self['1 ������ų'] + self['2 ������ų'] >= MAIN_CONFIG['������ȣ�̺�Ʈų��']:
                self.sendLine('\r\n' + MAIN_CONFIG['������ȣ�̺�Ʈȣ��'])
                self.lpPrompt()
        if self.tick % 600 == 0:
            self.save()
        if self.act == ACT_FIGHT:
            #����ó��
            self.doFight()
            if len(self.target) == 0:
                self.doAfterFight()
        elif self.act == ACT_DEATH:
            #���ó��
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
        if 'ü��' not in self.alias:
            return
        if 'ü�¾�' not in self.alias:
            return

        food = self.alias['ü�¾�']
        if food == '':
            return

        h = getInt(self.alias['ü��'])
        if h == 0:
            return

        if self.getHp() < h:
            self.do_command('%s �Ծ�' % food)

    def autoMpEat(self):
        m = 0
        if '����' not in self.alias:
            return
        if '������' not in self.alias:
            return
        food = self.alias['������']
        if food == '':
            return

        m = getInt(self.alias['����'])
        if m == 0:
            return

        if self.getMp() < m:
            self.do_command('%s �Ծ�' % food)

    def doAfterFight(self):
        self.moveNext()

    def moveNext(self):
        if self.act != ACT_STAND:
            return

        if len(self.autoMoveList) == 0:
            return
        att = ''
        if '����' in self.alias:
            att = self.alias['����']
          
        if att != '':
            self.do_command(att)
            if len(self.target) != 0:
                return
        
        next = self.autoMoveList.pop(0)
        self.do_command(next)
        if len(self.autoMoveList) == 0:
            self.sendLine('�� �� �̻� �̵� �� ��ΰ� �����ϴ�.')
            self.lpPrompt()

    def doSkill(self):
        #�ڵ��������������� �Ǿ��ִ����� üũ�ʿ�
        if self.skill == None and self.checkConfig('�ڵ���������'):
            sName = self['�ڵ�����']
            if sName != '':
                self.getSkill(sName)
                s = self.skill
                if self.getMp() < s.mp:
                    self.sendLine('[1m����� �������⸦ ���� �������� �Ⱑ ����� �����ϴ�.[0;37m')
                    self.stopSkill()
                    return
                if  self.getHp() < (self.getMaxHp() * s.hp) / 100 or self.getHp() < (self.getMaxHp() * s.maxhp) / 100:
                    self.sendLine('[1m����� �������Ⱑ ������� ���� ��ȯ�� ���߾� �����ϴ�.[0;37m')
                    self.stopSkill()
                    return
                self['����'] -= s.mp
                self['ü��'] -= (self.getMaxHp() * s.hp) / 100
                self.skill.init()
                self.lpPrompt()
                
                #print self.skill.bonus
                self.addStr(self.skill.bonus, False)
                buf1, buf2, buf3 = self.makeFightScript(self.skill['������ũ��'], self.target[0])
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
                        if type == '�ʽ�':
                            if self.checkConfig('���ø��') == False:
                                #print mob['�̸�']
                                buf1, buf2, buf3 = mob.makeFightScript(msg, self)
                                self.sendFightScript(buf2)
                        elif type == '����':
                            chance = mob.getSkillChance(self)
                            if chance < randint(0, 100):
                                if self.checkConfig('���ø��') == False:
                                    buf1, buf2, buf3 = mob.makeFightScript(mob.skill['����'], self)
                                    self.sendFightScript(buf2)
                            else:
                                if vCheck == False:
                                    self.checkVision(mob.skill)
                                    vCheck = True

                                dmg = mob.getSkillPoint(self)
                                vision = self['��������']
                                if vision != '':
                                    if mob.skill.name == vision.replace('����', '') or \
                                        (mob.skill.name[:2] == '��' and mob.skill.name[2:].isdigit()):
                                        dmg = int(dmg/2)
                                   
                                tdmg += dmg
                                if self.checkConfig('���ø��') == False:
                                    buf1, buf2, buf3 = mob.makeFightScript(msg, self)
                                    self.sendFightScript(buf2 + ' [1;31m%d[0;37m' % dmg)
                                if self.minusHP(dmg):
                                    self.clearTarget()
                                    return -1
            if more == False and mob.skill != None:
                mob.stopSkill()
            if more == False or type == '���':
                cnt = int(mob.dex / 700)
                mob.dex = mob.dex % 700
                for i in range(cnt):
                    chance = mob.getSkillChance(self)
                    if chance < randint(0, 100):
                        if self.checkConfig('���ø��') == False:
                            buf1, buf2, buf3 = mob.getAttackFailScript(self)
                            self.sendFightScript(buf2)
                    else:
                        dmg, c1, c2 = mob.getAttackPoint(self)
                        tdmg += dmg
                        
                        if self.checkConfig('���ø��') == False:
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
        #self.sendLine('%d' % self['������ġ'])
        if len(self.target) == 0:
            self.act = ACT_STAND
            return
        c = 0
        tdmg = 0
        more = False
        if self.checkConfig('���ø��') == False:
            self.sendLine('')
        if advance == False:
            self.dex += self.getDex() + 700
        else:
            self.dex = self.getDex()
        
        # Ȥ�ó� Ÿ���� �ٸ��뿡 �ְų� Ȱ��ȭ���°� �ƴҶ� Ÿ�� ����
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
        if target[0].get('��������') >= 1 or len(target) > 1 or self.fightMode == True:
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
                        if type == '�ʽ�':
                            buf1, buf2, buf3 = self.makeFightScript(msg, mob)
                            self.sendFightScript(buf1)
                            self.checkItemSkill()
                        elif type == '����':
                            target = copy.copy(self.target)
                            for mob in target:
                                chance = self.getSkillChance(mob)
                                if chance < randint(0, 100):
                                    if self.checkConfig('���ø��') == False:
                                        buf1, buf2, buf3 = self.makeFightScript(self.skill['����'], mob)
                                        self.sendFightScript(buf1)
                                    self.checkItemSkill()
                                    #����
                                    self.addDex(1)
                                    #���� �� �ø� üũ�ؾ���
                                    self.weaponSkillUp()
                                else:
                                    
                                    dmg = self.getSkillPoint(mob)
                                    if self.checkConfig('���ø��') == False:
                                        buf1, buf2, buf3 = self.makeFightScript(msg, mob)
                                        self.sendFightScript(buf1 + ' [1;36m%d[0;37m' % dmg)
                                    self.checkItemSkill()
                                    self.addStr(1)
                                    self.weaponSkillUp()
                                    if mob.minusHP(dmg, who = self['�̸�']):
                                        self.dex = 0
                                        #self.clearTarget(mob)
                                        if self.skill != None and self.skill.is_allAttack() == False:
                                            r = self.recoverDemage(tdmg)
                                            self['ü��'] += r
                                            if len(self.target) != 0:
                                                self.stopSkill()
                                            self.lpPrompt()
                                            return
                                        if len(self.target) == 0:
                                            r = self.recoverDemage(tdmg)
                                            self['ü��'] += r
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
            if more == False or type == '���':
                cnt = int(self.dex / 700)
                self.dex = self.dex % 700
                for l in range(cnt):
                    chance = self.getAttackChance(mob)
                    if chance < randint(0, 100):
                        buf1, buf2, buf3 = self.getAttackFailScript(mob)
                        if self.checkConfig('���ø��') == False:
                            self.sendFightScript(buf1)
                        if is_player(mob) and mob.checkConfig('���ø��') == False:
                            mob.sendFightScript(buf2)
                        self.checkItemSkill()
                        self.addDex(1)
                        self.weaponSkillUp()
                    else:
                        
                        dmg, c1, c2 = self.getAttackPoint(mob)
                        buf1, buf2, buf3 = self.getAttackScript(mob, dmg, c1, c2)
                        if self.checkConfig('���ø��') == False:
                            self.sendFightScript(buf1 + ' [1;36m%d[0;37m' % dmg)
                        if is_player(mob) and mob.checkConfig('���ø��') == False:
                            mob.sendFightScript(buf2 + ' [1;31m%d[0;37m' % dmg)
                        self.checkItemSkill()
                        #self.sendLine('����� ' + target[0].getName() + han_obj(target[0].getName())+ ' �ķ�Ĩ�ϴ�. %d' % dmg)
                        self.addStr(1)
                        self.weaponSkillUp()
                        if target[0].minusHP(dmg, who = self['�̸�']):
                            r = self.recoverDemage(tdmg)
                            self['ü��'] += r
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
                        if type == '�ʽ�':
                            if self.checkConfig('���ø��') == False:
                                buf1, buf2, buf3 = self.makeFightScript(msg, mob)
                                self.sendFightScript(buf1)
                            self.checkItemSkill()
                        elif type == '����':
                            chance = self.getSkillChance(mob)
                            if chance < randint(0, 100):
                                if self.checkConfig('���ø��') == False:
                                    buf1, buf2, buf3 = self.makeFightScript(self.skill['����'], mob)
                                    self.sendFightScript(buf1)
                                self.checkItemSkill()
                                #����
                                self.addDex(1)
                                #���� �� �ø� üũ�ؾ���
                                self.weaponSkillUp()
                            else:
                                dmg = self.getSkillPoint(mob)
                                if self.checkConfig('���ø��') == False:
                                    buf1, buf2, buf3 = self.makeFightScript(msg, mob)
                                    self.sendFightScript(buf1 + ' [1;36m%d[0;37m' % dmg)
                                self.checkItemSkill()
                                self.addStr(1)
                                self.weaponSkillUp()
                                if mob.minusHP(dmg, who = self['�̸�']):
                                    r = self.recoverDemage(tdmg)
                                    self['ü��'] += r
                                    #self.clearTarget(mob)
                                    self.lpPrompt()
                                    return
            if more == False and self.skill != None:
                self.skillUp()
                self.stopSkill()
            if more == False or type == '���':
                cnt = int(self.dex / 700)
                self.dex = self.dex % 700
                for l in range(cnt):
                    chance = self.getAttackChance(mob)
                    if chance < randint(0, 100):
                        if self.checkConfig('���ø��') == False:
                            buf1, buf2, buf3 = self.getAttackFailScript(mob)
                            self.sendFightScript(buf1)
                        if is_player(mob) and mob.checkConfig('���ø��') == False:
                            buf1, buf2, buf3 = self.getAttackFailScript(mob)
                            mob.sendFightScript(buf2)
                        self.checkItemSkill()
                        self.addDex(1)
                        self.weaponSkillUp()
                    else:
                        dmg, c1, c2 = self.getAttackPoint(mob)
                        if self.checkConfig('���ø��') == False:
                            buf1, buf2, buf3 = self.getAttackScript(mob, dmg, c1, c2)
                            self.sendFightScript(buf1 + ' [1;36m%d[0;37m' % dmg)
                        if is_player(mob) and mob.checkConfig('���ø��') == False:
                            buf1, buf2, buf3 = self.getAttackScript(mob, dmg, c1, c2)
                            mob.sendFightScript(buf2 + ' [1;31m%d[0;37m' % dmg)
                        self.checkItemSkill()
                        self.addStr(1)
                        self.weaponSkillUp()
                        if mob.minusHP(dmg, who = self['�̸�']):
                            r = self.recoverDemage(tdmg)
                            self['ü��'] += r
                            #self.clearTarget(mob)
                            self.lpPrompt()
                            return
            if advance == False:
                ret = self.fightMobNormal()
                if ret == -1:
                    return
                tdmg += ret
        r = self.recoverDemage(tdmg)
        self['ü��'] += r
        self.startSkill()
        if self.checkConfig('���ø��'):
            self.fightPrompt()
        else:
            self.lpPrompt()
        if len(self.target) != 0:
            mob = self.target[0]
            if is_player(mob) and mob.checkConfig('���ø��'):
                mob.fightPrompt()
            else:
                mob.lpPrompt()

    def startSkill(self):
        if self.skill != None:
            pass
        elif self.checkConfig('�ڵ���������'):
            sName = self['�ڵ�����']
            if sName != '':
                self.getSkill(sName)
                s = self.skill
                if self.getMp() < s.mp:
                    self.sendLine('[1m����� �������⸦ ���� �������� �Ⱑ ����� �����ϴ�.[0;37m')
                    self.stopSkill()
                    return
                if  self.getHp() < (self.getMaxHp() * s.hp) / 100 or self.getHp() < (self.getMaxHp() * s.maxhp) / 100:
                    self.sendLine('[1m����� �������Ⱑ ������� ���� ��ȯ�� ���߾� �����ϴ�.[0;37m')
                    self.stopSkill()
                    return
                self['����'] -= s.mp
                self['ü��'] -= (self.getMaxHp() * s.hp) / 100
                self.skill.init()
                #print self.skill.bonus
                self.addStr(self.skill.bonus)
                buf1, buf2, buf3 = self.makeFightScript(self.skill['������ũ��'], self.target[0])
                self.sendFightScript(buf1)
                #self.sendRoomFightScript(buf3)

    def doDeath(self):
        if self.stepDeath == 0:
            self.sendLine('\r\n������ �Ųٷ� ���� ������ ȥ���� ���ϴ�.')
            self.lpPrompt()
        elif self.stepDeath == 1:
            self.sendLine('\r\n�������� ��� ������ ��� �Ÿ��ϴ�.')
            self.lpPrompt()
        elif self.stepDeath == 2:
            self.sendLine('\r\n���� ���� �Ÿ��� �Ҹ��� ������ �ɵ��� ���� �־��� ���ϴ�.')
            self.lpPrompt()
        elif self.stepDeath == 3:
            room = getRoom('���缺:7')
            self.enterRoom(room, '���', '���')
            self.lpPrompt()
        elif self.stepDeath == 4:
            self.sendLine('\r\n�ڳ��� ��� �⳿���� ������ �������� ���ǻ� ���δ�.')
            self.lpPrompt()
        elif self.stepDeath == 5:
            self.sendLine('\r\n���ǻ簡 ���մϴ�. "��~~ ������ �˾Ҵµ� �ٽ� ����±�~"')
            self.lpPrompt()
        elif self.stepDeath == 6:
            self.sendLine('\r\n���ǻ簡 ���մϴ�. "�ϳ����� ��� �����ϰ� �ൿ���� ���� �����ؼ� �ൿ�ϰԳ�."')
            self.lpPrompt()
        elif self.stepDeath == 7:
            self.sendLine('\r\n����� ������ �ʴ� ���� ����� �߸� ������ ���� ���ϴ�.')
            self.lpPrompt()
        elif self.stepDeath == 8:
            # ���谡�� ����ó�� �ʿ�
            if self.insure == 0:
                self.sendLine('\r\n���ǻ簡 ���մϴ�. "����... ǥ������ ������ ���� �ʾұ�..."')
                self.sendLine('                   "������ ���������� ȭ�� �����Ѵٳ�."')
            else:
                self.sendLine('\r\n���ǻ簡 ���մϴ�. \"�ڳװ� ������ �ٴϴ� ������ ǥ������ ȸ�� �ؿ�����\"')
                self.sendLine('                   \"�Ҿ���� ���� ������ Ȯ���� ���Գ�..\"')
                self.sendLine('                   \"ǥ�����簡 �׷��µ� ����ᰡ �����ٴ���...\"')
            self.lpPrompt()
        elif self.stepDeath == 9:
            self.sendLine('\r\n����� �ڼ��� ����� �ϸ� ������Ŀ� ���ϴ�.')
            self.sendLine(HIC + '����� ������ Ÿ���ϱ� �����մϴ�.' + '[0;37m')
            self.sendRoom('%s �ڼ��� ����� �ϸ� ������Ŀ� ���ϴ�.' % self.han_iga())
            self.act = ACT_REST
            self.INTERACTIVE = 1
            self.input_to(self.parse_command)
            self.stepDeath = 0
            self.set('ü��', int(self.get('�ְ�ü��') * 0.33))
            self.lpPrompt()
            return

        self.stepDeath += 1

    def recover(self):
        #ü��ȸ��
        hp = self.getHp()
        maxhp = self.getMaxHp()
        
        mp = self.getMp()
        maxmp = self.getMaxMp()
        
        if self.act == ACT_STAND:
            # 10% ȸ��
            r = 0.1
        elif self.act == ACT_REST:
            # 20% ȸ��
            r = 0.2
        elif self.act == ACT_FIGHT:
            # 5% ȸ��
            r = 0.05
        else:
            r = 0
        if hp < maxhp:
            hp += int (maxhp * r)
            if hp >= maxhp:
                hp = maxhp
            self.set('ü��', hp)
        
        if mp < maxmp:
            mp += int (maxmp * r)
            if mp >= maxmp:
                mp = maxmp
            self.set('����', mp)

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
            if obj.checkConfig('���˰ź�') and len(kd) == 3:
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
        kl = self['��������'].splitlines()
        for k in kl:
            if k.find(config) == 0:
                if len(k.split()) > 1 and k.split()[1] == '1':
                    return True
                break
        return False
        
    def setConfig(self, config):
        c = ''
        find = False
        kl = self['��������'].splitlines()
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
        self['��������'] = c
        
        self.loadConfig()
        
    def loadAlias(self):
        self.alias = {}
        s = self['���Ӹ�����Ʈ'].splitlines()
        for key in s:
            ss = key.split(None, 1)
            self.alias[ss[0]] = ss[1]
        
    def buildAlias(self):
        msg = ''
        for key in self.alias:
            msg += key + ' ' + self.alias[key] + '\r\n'
        self['���Ӹ�����Ʈ'] = msg
        
    def setAlias(self, key, data):
        if key in self.alias:
            self.sendLine('�� �̹� �����Ǿ� �ִ� ���Ӹ��Դϴ�.')
            return False
        self.alias[key] = data
        self.buildAlias()
        return True
    
    def delAlias(self, key):
        if key not in self.alias:
            self.sendLine('�� ���Ӹ��� �����Ǿ� ���� �ʾƿ�. ^^')
            return False
        self.alias.__delitem__(key)
        self.buildAlias()
        return True
    
    def sendRoomFightScript(self, line, noPrompt = False, ex = []):
        for obj in self.env.objs:
            if is_player(obj) and obj != self and obj not in ex and obj.checkConfig('Ÿ��������°ź�') == False:
                obj.sendLine('\r\n' + line)
                if noPrompt == False:
                    obj.lpPrompt()
        
    def makeHome(self):
        room = Room()
        room.index = '����ڸ�:%s' % self['�̸�']
        room.path = 'data/map/����ڸ�/%s.map' % self['�̸�']
        room['�̸�'] = '%s�� ��' % self['�̸�']
        room['���̸�'] = '����ڸ�'
        room['����'] = '%s�� ���̴�.' % self['�̸�']
        room['�ⱸ'] = '���缺 ���缺:1'
        room.setAttr('�ʼӼ�', '�������������')
        room['����'] = self['�̸�']
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

