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
    reverseDir = { '동': '서',
                   '서': '동',
                   '남': '북',
                   '북': '남',
                   '북동': '남서',
                   '북서': '남동',
                   '남동': '북서',
                   '남서': '북동',
                   '위': '아래',
                   '아래': '위', 
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
            self.attr = scr['맵정보']
        except:
            return False 

        for boxName in self['설치리스트'].splitlines():
            box = Box()
            if self['방파주인'] != '':
                box.create('%s_%s' % (self['방파주인'], boxName))
            else:
                box.create('%s_%s' % (self['주인'], boxName))
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
        o['맵정보'] = self.attr
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
        
        exits = self.get('출구')
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
                #print '숨겨진 출구!'
                continue
            c = c + 1
            str = str + exitName + ' '
        if c == 0:
            str = '없음'
                
        self.shortExitStr = '\r\n[출구] : ' + str

        c = 0
        str1 = ''
        for exitName in self.exitList:
            if exitName[-1] == '$':
                #print '숨겨진 출구!'
                continue
            c = c + 1
            str1 = str1 + '[32m' + exitName +  '[37mː'
        str1 = str1[:-2]
        if c == 0:
            str = '\r\n  ○  어느 쪽으로도 이동할 수 없습니다.\r\n'
        else:
            if '북서' in self.exitList:
                str = '[32m↖[37m'
            else:
                str = '  '
            if '북' in self.exitList:
                str = str + '[32m△[37m'
            else:
                str = str + '  '
            if '북동' in self.exitList:
                str = str + '[32m↗[37m\r\n'
            else:
                str = str + '\r\n'
 
            if '서' in self.exitList:
                str = str + '[32m◁[37m'
            else:
                str = str + '  '
            str = str + '○'
            if '동' in self.exitList:
                str = str + '[32m▷[37m'
            else:
                str = str + '  '
            # print 출구
            str += ' 〔' + str1 + '〕쪽으로 이동할 수 있습니다.\r\n'
                
            if '남서' in self.exitList:
                str = str + '[32m↙[37m'
            else:
                str = str + '  '
            if '남' in self.exitList:
                str = str + '[32m▽[37m'
            else:
                str = str + '  '
            if '남동' in self.exitList:
                str = str + '[32m↘[37m'
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
            fileName = self.get('존이름') + ':' + fileName
        else:
            diff = self['존이름'][-1]
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
            fileName = self.get('존이름') + ':' + fileName
        else:
            diff = self['존이름'][-1]
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
            
        if '동' in e1:
            self.exitList.append('동')
            e1.remove('동')
        if '서' in e1:
            self.exitList.append('서')
            e1.remove('서')
        if '남' in e1:
            self.exitList.append('남')
            e1.remove('남')
        if '북' in e1:
            self.exitList.append('북')
            e1.remove('북')
        if '위' in e1:
            self.exitList.append('위')
            e1.remove('위')
        if '아래' in e1:
            self.exitList.append('아래')
            e1.remove('아래')
        if '남동' in e1:
            self.exitList.append('남동')
            e1.remove('남동')
        if '남서' in e1:
            self.exitList.append('남서')
            e1.remove('남서')
        if '북동' in e1:
            self.exitList.append('북동')
            e1.remove('북동')
        if '북서' in e1:
            self.exitList.append('북서')
            e1.remove('북서')
        
        for n1 in e1:
            self.exitList.append(n1)
    
    def getObjList(self):
        return self.objs
      
    def findMerchant(self):
        for obj in self.objs:
            if is_mob(obj) == False:
                continue
            if obj['물건판매'] != '' or obj['물건구입'] != '':
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
                if obj.get('몹종류') == 7:
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
            if obj['투명상태'] == 1:
                continue
            if is_mob(obj) and name != '시체' and (obj.act == ACT_DEATH or obj.act == ACT_REGEN):
                continue
            if name == '시체' and is_item(obj) == False and is_box(obj) == False and obj.act == ACT_DEATH:
                c += 1
                if c == order:
                    return obj
            elif obj.get('이름') == name or name in obj.get('반응이름').splitlines():
                c += 1
                if c == order:
                    return obj
            else:
                for alias in obj.get('반응이름').splitlines():
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
            if is_player(obj) and ex != obj['이름']:
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
                    itemMsg += '%s 먼지가 되어 사라집니다.\r\n' % item
                else:
                    itemMsg += '%s %d개가 먼지가 되어 사라집니다.\r\n' % (item[:-2], cnt)
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
        attrs = self['맵속성'].splitlines()
        for attr in attrs:
            self.mapAttr.append(attr)
            if attr.find('인원제한') == 0:
                self.limitNum = getInt(attr[8:].strip())
                continue
            if attr.find('명령금지') == 0:
                self.limitCmds = attr[8:].split()
                continue
            
    def checkAttr(self, attr):
        if attr in self.mapAttr:
            return True
        return False
    
    def noComm(self):
        return self.checkAttr('모든통신금지')
        
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
        room['존이름'] = zoneName
        zone[roomName] = room

    return room
    
def loadAllMap():
    log('맵 로딩중... 잠시만 기다려주세요.')
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
    log(str(c) + '개의 맵이 로딩되었습니다.')

def is_room(obj):
    return isinstance(obj, Room)
