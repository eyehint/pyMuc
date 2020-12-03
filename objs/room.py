# -*- coding: euc-kr -*-

import os
import glob
import random
import copy
import time

from include.define import *

from objs.object import Object
from objs.mob import Mob, is_mob
from objs.item import Item, is_item
from objs.box import Box, is_box

from lib.loader import load_script, save_script
from lib.func import *

class Room(Object): 

    Zones = {}
    reverseDir = { '��': '��',
                   '��': '��',
                   '��': '��',
                   '��': '��',
                   '�ϵ�': '����',
                   '�ϼ�': '����',
                   '����': '�ϼ�',
                   '����': '�ϵ�',
                   '��': '�Ʒ�',
                   '�Ʒ�': '��', 
                 }
    def __init__(self):
        Object.__init__(self)
        self.lastup_time = 0
        self.limitNum = 0
        self.limitCmds = []
        
    def create(self, index):
        self.index = index
        self.zone = index[:index.find(':')]
        self.path = 'data/map/' + index.replace(':', '/') + '.map'
        #print(path)
        scr = load_script(self.path)
        if scr == None:
            return False
        try:
            self.attr = scr['������']
        except:
            return False 

        for boxName in self['��ġ����Ʈ'].splitlines():
            box = Box()
            if self['��������'] != '':
                box.create('%s_%s' % (self['��������'], boxName))
            else:
                box.create('%s_%s' % (self['����'], boxName))
            self.insert(box)
        self.init()
        
    def init(self):
        self.loadAttr()
        self.initExit()
        self.setHiddenExit()
        
    def save(self, path = None):
        if path == None:
            path = self.path
        o = {}
        o['������'] = self.attr
        try:
            f = open(path, 'w')
        except:
            return False
        save_script(f, o)
        f.close()
        return True
        
    def setHiddenExit(self):
        Exits = copy.copy(self.Exits)
        for exitName in Exits:
            if exitName[-1] == '$':
                exit = self.Exits[exitName]
                self.Exits.__delitem__(exitName)
                self.Exits[exitName[:-1]] = exit
                
    def initExit(self):
       
        self.Exits = {}
        self.exitList = []
        self.shortExitStr = ''
        self.longExitStr = ''
        
        exits = self.get('�ⱸ')
        lines = exits.splitlines()
        for line in lines:
            s = line.split()
            c = len(s)
            if c == 2:
                self.Exits[s[0]] = s[1]
            elif c > 2:
                self.Exits[s[0]] = s[1:]

        self.sortExit()
        
        str = ''

        c = 0
        for exitName in self.exitList:
            if exitName[-1] == '$':
                #print '������ �ⱸ!'
                continue
            c = c + 1
            str = str + exitName + ' '
        if c == 0:
            str = '����'
                
        self.shortExitStr = '\r\n[�ⱸ] : ' + str

        c = 0
        str1 = ''
        for exitName in self.exitList:
            if exitName[-1] == '$':
                #print '������ �ⱸ!'
                continue
            c = c + 1
            str1 = str1 + '[32m' + exitName +  '[37m��'
        str1 = str1[:-2]
        if c == 0:
            str = '\r\n  ��  ��� �����ε� �̵��� �� �����ϴ�.\r\n'
        else:
            if '�ϼ�' in self.exitList:
                str = '[32m��[37m'
            else:
                str = '  '
            if '��' in self.exitList:
                str = str + '[32m��[37m'
            else:
                str = str + '  '
            if '�ϵ�' in self.exitList:
                str = str + '[32m��[37m\r\n'
            else:
                str = str + '\r\n'
 
            if '��' in self.exitList:
                str = str + '[32m��[37m'
            else:
                str = str + '  '
            str = str + '��'
            if '��' in self.exitList:
                str = str + '[32m��[37m'
            else:
                str = str + '  '
            # print �ⱸ
            str += ' ��' + str1 + '�������� �̵��� �� �ֽ��ϴ�.\r\n'
                
            if '����' in self.exitList:
                str = str + '[32m��[37m'
            else:
                str = str + '  '
            if '��' in self.exitList:
                str = str + '[32m��[37m'
            else:
                str = str + '  '
            if '����' in self.exitList:
                str = str + '[32m��[37m'
            else:
                str = str + '  '
                
        self.longExitStr = str

    def getExit(self, exitName):
        if exitName not in self.Exits:
            return None
        e = self.Exits[exitName]
        if type(e) == list:
            c = len(e)
            num = random.randint(0, c - 1)
            fileName = e[num]
        else:
            fileName = e
        
        i = fileName.find(':')
        if i == -1:
            fileName = self.get('���̸�') + ':' + fileName
        else:
            diff = self['���̸�'][-1]
            if diff.isdigit():
                fileName = fileName[:i] + diff + fileName[i:]

        return getRoom(fileName)
    
    def getExit1(self, exitName):
        if exitName not in self.Exits:
            return None
        e = self.Exits[exitName]
        if type(e) == list:
            return None
            c = len(e)
            num = random.randint(0, c - 1)
            fileName = e[num]
        else:
            fileName = e
        
        i = fileName.find(':')
        if i == -1:
            fileName = self.get('���̸�') + ':' + fileName
        else:
            diff = self['���̸�'][-1]
            if diff.isdigit():
                fileName = fileName[:i] + diff + fileName[i:]

        return getRoom(fileName)

    def getRandomExit(self):
        c = len(self.exitList)
        if c != 0:
            exitName = self.exitList[random.randint(0, c - 1)]
            r = self.getExit(exitName)
            return r, exitName
        return None, None
    
    def sortExit(self):

        e1 = []
        for n in self.Exits:
            e1.append(n)
            
        if '��' in e1:
            self.exitList.append('��')
            e1.remove('��')
        if '��' in e1:
            self.exitList.append('��')
            e1.remove('��')
        if '��' in e1:
            self.exitList.append('��')
            e1.remove('��')
        if '��' in e1:
            self.exitList.append('��')
            e1.remove('��')
        if '��' in e1:
            self.exitList.append('��')
            e1.remove('��')
        if '�Ʒ�' in e1:
            self.exitList.append('�Ʒ�')
            e1.remove('�Ʒ�')
        if '����' in e1:
            self.exitList.append('����')
            e1.remove('����')
        if '����' in e1:
            self.exitList.append('����')
            e1.remove('����')
        if '�ϵ�' in e1:
            self.exitList.append('�ϵ�')
            e1.remove('�ϵ�')
        if '�ϼ�' in e1:
            self.exitList.append('�ϼ�')
            e1.remove('�ϼ�')
        
        for n1 in e1:
            self.exitList.append(n1)
    
    def getObjList(self):
        return self.objs
      
    def findMerchant(self):
        for obj in self.objs:
            if is_mob(obj) == False:
                continue
            if obj['�����Ǹ�'] != '' or obj['���Ǳ���'] != '':
                return obj
        return None
        
    def findObjName(self, name):
        if name == '':
            return None
        if name.strip() == '.':
            name = '1'
        t = name.split()
        if len(t) > 1:
            name = t[0]
        order = 0
        if name.isdigit():
            order = int(name)
        c = 0
        if order != 0:
            for obj in self.objs:
                if is_mob(obj) == False:
                    continue
                if obj.get('������') == 7:
                    continue
                if obj.act == ACT_DEATH or obj.act == ACT_REGEN:
                    continue
                c += 1
                if c == order:
                    return obj
            return None
            
        order = getInt(name)
        if order != 0:
            for i in range( len(name) ):
                if name[i].isdigit() == False:
                    name = name[i:]
                    break
        else:
            order = 1
        d = 0
        for obj in self.objs:
            if obj['�������'] == 1:
                continue
            if is_mob(obj) and name != '��ü' and (obj.act == ACT_DEATH or obj.act == ACT_REGEN):
                continue
            if name == '��ü' and is_item(obj) == False and is_box(obj) == False and obj.act == ACT_DEATH:
                c += 1
                if c == order:
                    return obj
            elif obj.get('�̸�') == name or name in obj.get('�����̸�').splitlines():
                c += 1
                if c == order:
                    return obj
            else:
                for alias in obj.get('�����̸�').splitlines():
                    if alias.find(name) == 0:
                        d += 1
                        if d == order:
                            return obj
        return None
        
    def sendRoom(self, line, prompt = True):
        from objs.player import is_player
        for obj in self.objs:
            if is_player(obj):
                obj.sendLine(line)
                if prompt:
                    obj.lpPrompt()
        
    def writeRoom(self, line):
        from objs.player import is_player
        for obj in self.objs:
            if is_player(obj):
                obj.write(line)
        
    def printPrompt(self, ex = None, newline = True):
        from objs.player import is_player
        for obj in self.objs:
            if is_player(obj) and ex != obj['�̸�']:
                if newline:
                    obj.sendLine('')
                obj.lpPrompt()
                    
    def update(self):
        updated = False
        current_time = time.time()
        if current_time - self.lastup_time < 1:
            return
        #print 'updateRoom()'
        self.lastup_time = current_time
        objs = copy.copy(self.objs)
        itemMap = {}
        for obj in objs:
            if is_item(obj):
                name = obj.han_iga()
                if obj.update():
                    if name not in itemMap:
                        itemMap[name] = 0
                    itemMap[name] += 1
            if is_mob(obj):
                if obj.update():
                    updated = True
        if len(itemMap) != 0:
            itemMsg = ''
            for item in itemMap:
                cnt = itemMap[item]
                if cnt == 1:
                    itemMsg += '%s ������ �Ǿ� ������ϴ�.\r\n' % item
                else:
                    itemMsg += '%s %d���� ������ �Ǿ� ������ϴ�.\r\n' % (item[:-2], cnt)
            self.writeRoom('\r\n' + itemMsg[:-2])
            updated = True 
        if updated:
            self.printPrompt()

    def checkLimitNum(self):
        if  self.limitNum == 0:
            return False
        num = 0
        from objs.player import is_player
        for obj in self.objs:
            if is_player(obj):
                num += 1
        if num >= self.limitNum:
            return True
        return False
        
    def loadAttr(self):
        self.mapAttr = []
        attrs = self['�ʼӼ�'].splitlines()
        for attr in attrs:
            self.mapAttr.append(attr)
            if attr.find('�ο�����') == 0:
                self.limitNum = getInt(attr[8:].strip())
                continue
            if attr.find('��ɱ���') == 0:
                self.limitCmds = attr[8:].split()
                continue
            
    def checkAttr(self, attr):
        if attr in self.mapAttr:
            return True
        return False
    
    def noComm(self):
        return self.checkAttr('�����ű���')
        
    def getItemCount(self):
        n = 0
        for item in self.objs:
            if is_item(item):
                n += 1
        return n

        
def getRoom(path):

    i = path.find(':')
    if i == -1:
        return None

    zoneName = path[:i]
    roomName = path[i+1:]

    try:
        zone = Room.Zones[zoneName]
    except KeyError:
        zone = {}
        Room.Zones[zoneName] = zone
        
    try:
        room = zone[roomName]
    except KeyError:
        room = Room()
        ret = room.create(path)
        if ret == False:
            return None
        room['���̸�'] = zoneName
        zone[roomName] = room

    return room
    
def loadAllMap():
    log('�� �ε���... ��ø� ��ٷ��ּ���.')
    pwd = os.getcwd()
    c = 0
    dirs = os.listdir('data/map')
    for dir in dirs:
        try:
            os.chdir('data/map/' + dir)
        except:
            os.chdir(pwd)
            continue
        files = glob.glob('*.map')
        os.chdir(pwd)
        for file in files:
            room = getRoom(dir + ':' + file[:-4])
            if room != None:
                c = c + 1
    log(str(c) + '���� ���� �ε��Ǿ����ϴ�.')

def is_room(obj):
    return isinstance(obj, Room)
