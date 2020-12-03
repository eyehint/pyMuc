# -*- coding: euc-kr -*-

import os
import glob
import time
import copy

from random import randint
from twisted.internet import reactor
from include.define import *
from objs.body import Body
from objs.config import Config, MAIN_CONFIG
from objs.item import Item, is_item, getItem
from objs.script import Script, SCRIPT
from objs.oneitem import Oneitem, ONEITEM
from objs.skill import MUGONG

from lib.loader import load_script, save_script
from lib.func import *
from lib.hangul import *
from objs.droplist import DROPITEM

MAXPROCESSMOVING = 30
REGEN_MULTIPLY = 3

		  
class Mob(Body):

    Mobs = {}
    movingMobs = []
    numMovings = 0
    nMovingOrder = 0
    
    def __init__(self):
        self.bPlayer = 0
        self.origin = ''
        self.moveTime = 0
        self.timeofdeath = 0
        self.timeofregen = 0
        self.moveTick = 0
        self.talkTick = 0
        self.moveList = []
        self.skillList = []
        self.skill = None
        self.weapon = ''
        
        self.hp = 0
        self.mp = 0
        
        
        Body.__init__(self)
        
    def create(self, index):
        #print(path)
        self.index = index
        self.path = 'data/mob/' + index.replace(':', '/') + '.mob'
        scr = load_script(self.path)
        
        if scr == None:
            return False
        
        try:
            self.attr = scr['������']
        except:
            return False
            
        self.init()
        
    def init(self):
        self.corpse = getInt(self.get('��ü'))
        if self.corpse <= 0:
            self.corpse = 30
        else:
            self.corpse = self.corpse * MAIN_CONFIG['REGEN_MULTIPLY']
        self.regen = getInt(self.get('����'))
        if self.regen <= 0:
            self.regen = 60
        elif self.regen >= 360:
            self.regen = 360
        else:
            self.regen = self.regen * MAIN_CONFIG['REGEN_MULTIPLY']
            if self.regen >= 360:
                self.regen = 360
        self.setMove()
        
        l = self.get('��������').splitlines()
        for i in l:
            item = getItem(i.split()[0])
            if item == None:
                continue
            self.armor += getInt(item['����'])
            self.attpower += getInt(item['���ݷ�'])
            if item['����'] == '����':
                self.weapon = item['������ũ��']
                self.weaponItem = item
        
        l = self['����'].splitlines()
        for m in l:
            words = m.split()
            if len(words) != 3:
                continue
            s = MUGONG[words[0]]
            if s == None or s == '':
                continue
            self.skillList.append( ( s, int(words[1]), int(words[2]) ) )
            
    def reset(self):
        self.target = []
        self.skills = []
        self.dmgMap = {}
        self.dex = 0
        self._str = 0
        self._dex = 0
        self._arm = 0
        self._mp = 0
        self._maxmp = 0
        if self['ü��'] == '':
            self['ü��'] = 0
        if self['����'] == '':
            self['����'] = 0
        self.hp = getInt(self.get('ü��'))
        self.mp = getInt(self.get('����'))
        
    def place(self):
        from objs.room import Room, is_room, getRoom
        keydata = self.getString('��ġ')
        lines = keydata.splitlines()
        for line in lines:
            for loc in line.split():
                room = getRoom(self.get('���̸�') + ':' + loc)
                if room != None:
                    mob = self.clone()
                    mob.reset()
                    mob.origin = self.get('���̸�') + ':' + loc
                    room.insert(mob)
                    if len(mob.moveList) != 0:
                        self.movingMobs.append(mob)
    
    def getMp(self):
        if self._mp != 0:
            mp = self.mp + self.mp * self._mp / 100
            return mp
        return self.mp
        
    def getMaxMp(self):
        if getInt(self['����']) == 0:
	    return 0
        if self._maxmp != 0:
            mp = self['����'] + self['����'] * self._maxmp / 100
            return float(mp)
        return self['����']
                            
    def addItem(self):
        if len(self.objs) != 0:
            return
        d = self['���̵�']
        if d == '':
            d = 0

        iList = self['������'].splitlines()
        for i in iList:
            c = 1
            words = i.split()
            if len(words) < 3:
                continue
            if len(words) == 4:
                c = getInt(words[3])
            index = words[0]
            item = getItem(index)
            if item == None:
                continue
            if item.isOneItem() and item.isOneThere():
                continue
            count = getInt(words[1])
            chance = getInt(words[2])
            if d > 0:
               chance = int( chance * Body.difficulty[d-1][2] ) 
            for cnt in range(count):
                if chance >= randint(0, 100 * c):
                    obj = item.deepclone()
                    obj.applyMagic(self['����'], 0)
                    self.insert(obj)
                    
        iList = self['��������'].splitlines()
        for i in iList:
            c = 1
            words = i.split()
            if len(words) < 3:
                continue
            if len(words) == 4:
                c = getInt(words[3])
            index = words[0]
            item = getItem(index)
            if item == None:
                continue
            if item.isOneItem() and item.isOneThere():
                continue
            count = getInt(words[1])
            chance = getInt(words[2])
            for cnt in range(count):
                if chance >= randint(0, 100 * c):
                    obj = item.deepclone()
                    obj.applyMagic(self['����'], 0)
                    self.insert(obj)
        
    def viewItemList(self):
        if len(self.objs) == 0:
            return '[36m�� �ƹ��͵� �����ϴ�.[37m'
        msg = ''
        for obj in self.objs:
            msg += '[36m%s[37m\r\n' % obj['�̸�']
        return msg[:-2]
        
    def view(self, ob):
        if self.act == ACT_DEATH:
            ob.sendLine('������������������������������������������������������������')
            ob.sendLine('[0m[44m[1m[37m�� �̸� �� %-49s[0m[37m[40m' % (self.get('�̸�') + '�� ��ü'))
            ob.sendLine('������������������������������������������������������������')
            ob.sendLine(self.viewItemList())
            ob.sendLine('������������������������������������������������������������')
            return
            
        ob.sendLine('������������������������������������������������������������')
        ob.sendLine('[0m[44m[1m[37m�� �̸� �� %-49s[0m[37m[40m' % self.get('�̸�'))
        ob.sendLine('������������������������������������������������������������')
        ob.sendLine(self.get('����2'))
        ob.sendLine('������������������������������������������������������������')
        
        l = self.get('��������').splitlines()
        for lv in self.ItemLevelList:
            for i in l:
                item = getItem(i.split()[0])
                if lv == item['����']:
                    ob.sendLine('[%s] [36m%s[37m' % (self.ItemUseLevel[item.get('����')] , item.get('�̸�')))
        if len(l) != 0:
            ob.sendLine('������������������������������������������������������������')
        ob.sendLine('�� %s' % self.GetHPString())
        ob.sendLine('�� %s' % self.getHPbar())
        ob.sendLine('������������������������������������������������������������')
        
    def checkDieEvent(self):
        e1 = self.get('�̺�Ʈ $%�Ҹ��̺�Ʈ%')
        e2 = self.get('�̺�Ʈ: $%�Ҹ��̺�Ʈ%')
        
        if e1 != '':
            return '�̺�Ʈ $%�Ҹ��̺�Ʈ%'
        elif e2 != '':
            return '�̺�Ʈ: $%�Ҹ��̺�Ʈ%'
        
        return ''
            
    def setMove(self):
        rstr = str( self.get('�̵�') )
        
        if rstr == '':
            return
        self.moveTick = getInt(self.get('�̵�ƽ'))
        if self.moveTick == 0:
            self.moveTick = 30
        
        mr = rstr.split()
        for r in mr:
            if r.find('-') != -1:
                rs = r.split('-')
                if len(rs) != 2:
                    continue
                for n in range( int(rs[0]), int(rs[1]) ):
                    rName = self.get('���̸�') + ':' + str(n)
                    if rName not in self.moveList:
                        self.moveList.append(rName)
            else:
                rName = self.get('���̸�') + ':' + r
                if rName not in self.moveList:
                    self.moveList.append(rName)
        
    def updateMoving(self):
        if self.numMovings == 0:
            return
        #print 'updateMovings'
        for n in range(MAXPROCESSMOVING):
            if  self.nMovingOrder >= self.numMovings:
                self.nMovingOrder = 0
                break
            
            mob = self.movingMobs[self.nMovingOrder]
            if mob != None:
                mob.move()
                #print str(self.nMovingOrder) + ': ' + mob.get('�̸�')
            self.nMovingOrder += 1
            
        if self.nMovingOrder >= self.numMovings:
            self.nMovingOrder = 0
        
    def move(self):
        
        if self.env == None:
            return
        if self.act != ACT_STAND:
            return
            
        if self.moveTime == 0:
            self.moveTime = time.time()
        curTime = time.time()
        if curTime < self.moveTime + self.moveTick:
            return
        if randint(0, 2) != 0:
            return
        room, dir = self.env.getRandomExit()
        if dir not in ['��', '��', '��', '��', '��', '�Ʒ�', '�ϵ�', '�ϼ�', '����', '����']:
            return
        if room == None:
            return
            
        if room.index in self.moveList:
            #print str(self.nMovingOrder) + ': ' + self.get('�̸�') + ' ' + room.index
            self.enterRoom(room, dir)
    
    def enterRoom(self, room, dir):
        self.moveTime = time.time()
        #print self.get('�̸�') + ' ' + room.index + '/' + dir
        
        msg1 = self.get('������ũ��')
        if msg1 == '':
            msg1 = '$����$������ �����ϴ�.'
        msg1 = msg1.replace('$����$', dir)
        msg2 =  self.get('���Խ�ũ��')
        if msg2 == '':
            msg2 = '$����$�ʿ��� �Խ��ϴ�.'
        msg2 = msg2.replace('$����$', room.reverseDir[dir])
        self.env.sendRoom('\r\n[33m' + self.get('�̸�') + '[37m' + han_iga(self.get('�̸�')) + ' ' + msg1)
        self.env.remove(self)
        msg = '\r\n[33m' + self.get('�̸�') + '[37m' + han_iga(self.get('�̸�')) + ' ' + msg2
        say = self.getSayStr()
        if say != '' and randint(0,2) == 0:
            msg += '\r\n' + say
        room.sendRoom(msg)
        room.insert(self)
        
    def getNameA(self):
        return '[33m' + self.get('�̸�') + '[37m'
        
    def say(self):
        say = self.getSayStr()
        if say != '':
            self.env.writeRoom('\r\n' + say)
                    
    def update(self):
        self.tick += 1
        curTime = time.time()
        if self.tick % 60 == 0:
            self.recover()
        
        if self.act == ACT_STAND:
            if self.get('��ȭƽ') != '' and self.tick % self.get('��ȭƽ') == 0:
                if randint(0, 2) == 0:
                    self.say()
                    return True
        elif self.act == ACT_DEATH:
            if curTime - self.timeofdeath >= self.corpse + self.regen:
                self.doDeath(curTime - self.timeofdeath - self.corpse)
                self.doRegen()
                return True
            elif curTime - self.timeofdeath >= self.corpse:
                self.doDeath()
                return True
        elif self.act == ACT_REGEN:
            if curTime - self.timeofdeath >= self.corpse + self.regen:
                self.doRegen()
                return True
        elif self.act == ACT_REST:
            if curTime - self.timeofdeath >= self.regen:
                self.doRegen()
                return True
        if self['������'] == 6:
            r = self['�����۸���']
            if r < 180:
                r = 180
            if curTime - self.timeofregen >= r:
                self.timeofregen = curTime
                self.addItem()
        elif self['��������'] == 1 and self.act == ACT_STAND:
            from objs.player import Player, is_player
            for ply in self.env.objs:
                if is_player(ply) and ply['�������'] != 1:
                    ply.setFight(self, True)  
                    break
            
        if self.checkDefenceSkill(curTime):
            return True
        return False
        
    def recover(self):
        #ü��ȸ��
        hp = self.hp
        maxhp = self.get('ü��')
        
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
            return

        if hp < maxhp:
            hp += int (maxhp * r)
            if hp >= maxhp:
                hp = maxhp
            self.hp = hp
        
        if mp < maxmp:
            mp += int (maxmp * r)
            if mp >= maxmp:
                mp = maxmp
            self.mp = mp

    def checkDefenceSkill(self, curTime):
        skills = copy.copy(self.skills)
        msg = ''
        for s in skills:
            if s.end_time < curTime:
                self.skills.remove(s)
                buf1, buf2, buf3 = self.makeFightScript(s['����������ũ��'], None)
                self._str -= s._str
                self._dex -= s._dex
                self._arm -= s._arm
                self._mp -= s._mp
                self._maxmp -= s._maxmp
                msg += '\r\n' + buf3
                #print msg
                del s
        if len(msg) != 0:
            self.env.writeRoom(msg)
            return True
        return False
                
    def getExpGold(self, target):
        c1 = getInt(target['����'])
        c2 = getInt(self['����'])
        a=((c2*c2)/3)+30
    	b=(a * (c2-c1))/100
    	
    	c = a + b
    	#print c1, c2, a, b, c
    	if c < 1:
    	    c = 1;
    	if c > MAX_INT:
    	    c = MAX_INT
    	c2 = randint(0, 9)
    	if randint(0, 1) == 0:
    	    c += c2
    	else:
            c -= c2;
    	if c < 1:
    	    c = 1
    	if c > MAX_INT:
    	    c = MAX_INT
    	
        c1 = getInt(self['����']) + 14
        c2 = randint(0, 4)
        if randint(0, 1) == 0:
            c1 += c2;
        else:
            c1 -= c2;
        #print self['����']
        c1 += getInt(self['����'])
        if c1 < 1:
            c1 = 1
        if c1 > MAX_INT:
            c1 = MAX_INT
        
        return c, c1
	
    def addHerb(self):
        if len(self.target) == 0:
            return
        if self['����'] < self.target[0]['����']:
            return
        p1 = self['����'] - self.target[0]['����']
        p2 = p1 * 0.01 + 0.05
        try:
            d = float (self['���̵�']) 
            p2 += d
        except:
            pass
        p3 = randint(0, 99)
        
        if p2 > MAIN_CONFIG['���ʳ���Ȯ��']:
            p2 = MAIN_CONFIG['���ʳ���Ȯ��']
        if p2 < p3:
            return
        
        herbs = MAIN_CONFIG['���������۸���Ʈ'].splitlines()
        l = len(herbs)
        herb = getItem(herbs[randint(0, l - 1)]).clone()
        if len(self.target) != 0:
            self.target[0].insert(herb)
	    
    def die(self, killer):
        from objs.player import Player, is_player
        self._str = 0
        self._dex = 0
        self._arm = 0
        self.addItem()
        self.addHerb()
        msg = self.get('�Ҹ꽺ũ��')
        if msg == '':
            self.env.writeRoom('\r\n[1;37m' + self.getName() + han_iga(self.getName()) + ' �������ϴ�. \'���~~ ö�۴�~~\'[0;37m')
        else:
            self.env.writeRoom('\r\n[1;37m' + msg + '[0;37m')
        self.env.writeRoom('\r\n')
        #print len(self.target)
        c = 0

        for target in self.target:
            if self.env != target.env:
                continue
            who = target['�̸�']
            if who not in self.dmgMap:
                continue
            c += 1
            dmg = float(self.dmgMap[who])
            ratio = dmg / float(self['ü��'])
            if ratio > 1:
                ratio = 1
            #print dmg, self['ü��'], ratio
            exp, gold = self.getExpGold(target)
            exp = int( exp * ratio )
            gold = int ( gold * ratio )
            bonus_exp = 0
            bonus_gold = 0
            
            #if is_player(target) and target['����'] > self['����']:
            #    target.addStr(5);
            #    target.addDex(2);
            #    target.weaponSkillUp(3);
            try:
                d = int (self['���̵�'])
            except:
                d = 0
            if d != 0:
                bonus_exp = int( exp * Body.difficulty[d-1][2] ) 
                bonus_gold = int( gold * Body.difficulty[d-1][3] ) 
                target.sendLine('\r\n����� %d(+%d)�� ����ġ�� ����ϴ�.' % (exp, bonus_exp))
                target.sendLine('����� %s���� ���� %d(+%d)���� ȹ���մϴ�.' % (self.getNameA(), gold, bonus_gold))
            else:
                target.sendLine('\r\n����� %d�� ����ġ�� ����ϴ�.' % exp)
                target.sendLine('����� %s���� ���� %d���� ȹ���մϴ�.' % (self.getNameA(), gold))
            target['����'] += gold + bonus_gold
            target['%d ������ų' % getInt(self['����'])] += 1
            
            msg = '%s �ణ�� ����ġ�� ����ϴ�.\r\n' % target.han_iga()
            msg += '%s ��� ������ ȹ���մϴ�.' % target.han_iga()
            
            if c == 1 and target.checkConfig('�ڵ�����') == True:
                chance = randint(0, 99)
                if self['����'] >= 2000 and chance < 1:
                    dropitem = DROPITEM[randint(0, len(DROPITEM) - 1)]
                    item = getItem(dropitem)
                    if item != None:
                        if target.getItemCount() <= getInt(MAIN_CONFIG['����ھ����۰���']) and target.getItemWeight() + item['����'] < target.getStr() * 10:
                            obj = item.deepclone()
                            if randint(0, 99) < 30:
                                obj.applyMagic(self['����'], 0)
                            target.insert(obj)
                            target.sendLine('����� %s ����ǰ���� ȹ���մϴ�.' % item.han_obj())
                            msg += '\r\n%s %s ����ǰ���� ȹ���մϴ�.' % (target.han_iga(), item.han_obj())
                            
                objs = copy.copy(self.objs)
                for item in objs:
                    if target.getItemCount() > getInt(MAIN_CONFIG['����ھ����۰���']) or target.getItemWeight() + item['����'] > target.getStr() * 10:
                        break
                    self.remove(item)
                    target.insert(item)
                    if item.isOneItem():
                        ONEITEM.have(item.index,target['�̸�'])
                    target.sendLine('����� %s ����ǰ���� ȹ���մϴ�.' % item.han_obj())
                    msg += '\r\n%s %s ����ǰ���� ȹ���մϴ�.' % (target.han_iga(), item.han_obj())
            target.sendRoom(msg, noPrompt = True)
            
            target.addExp(exp + bonus_exp)
        
        dieEvent = self.checkDieEvent()
        if dieEvent != '':
            reactor.callLater(0, target.doEvent, self, dieEvent, '')
        if len(self.target) != 0:
            target.env.printPrompt(killer, False)
        self.act = ACT_DEATH
        self.clearTarget()
        self.clearSkills()
        self.timeofdeath = time.time()
        
    def minusHP(self, demage, mode = True, who = ''):
        if demage > self.hp:
            demage = self.hp
        if who not in self.dmgMap:
            self.dmgMap[who] = demage
        else:
            self.dmgMap[who] += demage
        self.hp -= demage
        if self.hp <= 0:
            self.die(who)
            return True
        return False
        
    def doDeath(self, sec = None):
        self.act = ACT_REGEN
        self.env.writeRoom('\r\n' + self.getNameA() + '�� ��ü�� ���������� �տ� �̲��� ������ ���� �ǳʰ��ϴ�.')
        if len(self.objs) > 0:
            objs = copy.copy(self.objs)
            msg = '\r\n'
            for obj in objs:
                msg += '%s�� ��ü�ӿ��� %s ����� �巯���ϴ�.\r\n' % (self.getNameA(), obj.han_iga())
                self.remove(obj)
                self.env.insert(obj)
                obj.drop(sec)
            self.env.writeRoom(msg[:-2])
        
    def doRegen(self):
        self._str = 0
        self._dex = 0
        self._arm = 0
        from objs.room import getRoom
        self.reset()
        self.act = ACT_STAND
        #���� index�� �����϶�!
        if self.origin != self.env.index:
            self.env.remove(self)
            room = getRoom(self.origin)
            room.insert(self)
        self.env.writeRoom('\r\n' + self.get('����3'))
        self.attack_player()
        
    def attack_player(self):
        from objs.player import Player, is_player
        # �������� ��� �÷��̾� ����
        if self.get('��������') == 1:
            #print '����������2!!'
            for p in self.env.objs:
                if is_player(p) and p['�������'] != 1:
                    #print '����������3!!'
                    p.setFight(self, True)
                    break
        
    def getSayStr(self):
        lines = self.get('�ڵ���ũ��').splitlines()
        if len(lines) == 0:
            return ''
        return lines[randint(0, len(lines) - 1)]
        
    def getDesc1(self):
        msg = ''
        for s in self.skills:
            msg += s['�����¸Ӹ���'] + ' '
        return msg + self.get('����1')
    
    def checkEvent(self, words):
        noissue = ''
        for key in self.attr:
            if key.find('�̺�Ʈ') == 0:
                keywords = key[7:].split()
                cmdList = []
                issueList = []
                for keyword in keywords:
                    if keyword[0] == '$':
                        cmdList.append(keyword[1:])
                    else:
                        issueList.append(keyword)
                    
                if words[-1] in cmdList:
                    #print self.attr[key]
                    if len(issueList) == 0:
                        noissue = key
                    if len(words) > 2 and words[-2] not in issueList:
                        continue
                    elif len(words) == 2 and len(issueList) != 0:
                        continue
                    #self.doEvent(player, key, words)
                    return key
        if noissue != '':
            #self.doEvent(player, noissue, words)
            return noissue
        return ''
    
    def getFightStartStr(self):
        return '[33m' + self.get('�̸�') + '[37m' + han_iga(self.get('�̸�')) + ' ' + self.get('��������'), ''
        
    def getHPbar(self):
        maxhp = self.get('ü��')
        hcnt = 10*self.hp/maxhp
        return self.strBar[hcnt] + ' (%d)' % (100 * self.hp / maxhp)
        
    def get_hp_script(self):
        maxhp = self.get('ü��')
        cnt = len(self.hp_script)
        s = self.hp_script[(cnt - 1) - ((cnt - 1) * self.hp / maxhp)]
        s = self['�̸�'] + postPosition(s, self['�̸�'])
        return s
        
    def GetHPString(self):
        mode = self['ü�½�ũ��']
        if mode == '':
            mode == '���'
        mode += '��ũ��'
        scripts = SCRIPT[mode]
        cnt = len(scripts)
        if cnt == 0:
            return ''
        ix = (cnt - 1) - ((cnt - 1) * self.hp / self['ü��'] )
        if ix < 0:
            ix = 0
        if ix >= cnt:
            ix = cnt - 1
        s = scripts[ix]
        s = self['�̸�'] + postPosition(s, self['�̸�'])
        return s

    def getWeapon(self):
        if self.weaponItem != None:
            return self.weaponItem
        return getItem('�ָ�')
        
    def getAttackFailScript(self, mob):
        if self.weapon == '':
            buf = self['������ũ��']
        else:
            buf = self.weapon
            
        s = SCRIPT[buf + '�������н�ũ��']
        s = s[randint(0, len(s) - 1)]
        
        
        return self.makeFightScript(s, mob)
        
    def getAttackScript(self, mob, dmg, c1, c2):
        if self.weapon == '':
            buf = self['������ũ��']
        else:
            buf = self.weapon
        s = SCRIPT[buf + '������ũ��']
        c = ((dmg - c1) * (len(s) - 1))/(c2-c1)
        #print dmg, c1, c2, c, len(s)
        i = len(s) - 1 - c
        if i < 0 or i > len(s) - 1:
            print 'mob.getAttackScript'
            i = 0
        s = s[i]
        #s = s[randint(0, len(s) - 1)]

        return self.makeFightScript(s, mob)
        
    def getAct(self):
        if self.act == ACT_STAND:
            return '����'
        elif self.act == ACT_REST:
            return '��'
        elif self.act == ACT_FIGHT:
            return '����'
        elif self.act == ACT_DEATH:
            return '��ü'
        elif self.act == ACT_REGEN:
            return '����'
            
    def setAct(self, act):
        if act == '����':
            self.act = ACT_STAND
        elif act == '��':
            self.act = ACT_REST
        elif act == '����':
            self.act = ACT_FIGHT
        elif act == '��ü':
            self.act = ACT_DEATH
            self.timeofdeath = time.time()
        elif act == '����':
            self.doDeath()
        elif act == '�����Ļ���':
            self.doRegen()
            
    def setSkill(self):
        if self.skill != None:
            return False
        for skill in self.skillList:
            if skill[0]['����'] != '����':
                continue
            if self.hp > self['ü��'] * skill[1] / 100:
                continue
            if skill[2] < randint(0, 100):
                continue
            if skill[0].mp > self.getMp():
                continue
            if self.lastskill != None and self.lastskill.name == skill[0].name:
                self.skill = self.lastskill
            else:
                self.skill = copy.copy(skill[0])
            self.skill.init()
            self.mp -= self.skill.mp
            return True
        return False
            
    def getSkillChance(self, mob):
        l1 = self['����']
        l2 = mob['����']
        if self.skill != None:
            CHANCE = self.skill['Ȯ��']
        else:
            CHANCE = 100
        bonus = getInt(self['����']) * float(MAIN_CONFIG['����Ȯ��'])
        bonus -= getInt(mob['ȸ��']) * float(MAIN_CONFIG['ȸ��Ȯ��'])
        return CHANCE - (((l2-l1)+90)/3) + bonus

    def setDifficulty(self):
        maxlv = 15500
        try:
            d = int(self['���̵�'])
        except:
            d = 0
        if d == 0:
            return
        d -= 1
        l = self['����'] + 2000 * (d + 1) - 500
        self['����'] = l
        #self['ü��'] = int( self['ü��'] * self.difficulty[d][0] + 200000 * d)
        hp = int( 0.0529 * l * l - 8.7552 * l + 2448.9 )
        self['ü��'] = int( hp * self.difficulty[d][2])
        #self['��'] = int( self['��'] * self.difficulty[d][1] + 5500 * d )
        self['��'] = int( l * (3.0 + l / 20000)  * 1.3 )
        dex = l
        if dex < 1400:
            dex = 1400
        if dex > 2800:
           dex = 2800
        self['��ø��'] = dex
        self['����'] = l * 3
        m = 4000 + int( l / 2 )
        if self['����'] < m:
            self['����'] = m
        if self['����'] == '':
            h1 = 80
            c1 = 70
            h = h1 + self['����'] * (100-h1) / maxlv
            if h > 100:
                h = 100
            c = c1 + self['����'] * (100-c1) / maxlv
            if c > 100:
                c = 100
            s = MUGONG['��%d' % (d + 1)]
            self.skillList.append( ( s, h, c ) )

        self['����'] = int( self['����'] * 300 / maxlv )
        self['ȸ��'] = int( self['����'] * 200 / maxlv )
        self['�ʻ�'] = int( self['����'] * 200 / maxlv )
        self['��'] = int( self['����'] * 200 / maxlv )

        self.hp = self['ü��']
        self.mp = self['����']
        self['���ʽ�'] = self.difficulty[d][2]

    
def is_mob(obj):
    return isinstance(obj, Mob)

def getMob(path):

    i = path.find(':')
    if i == -1:
        return None

    zoneName = path[:i]
    mobName = path[i+1:]

    try:
        zone = Mob.Mobs[zoneName]
    except KeyError:
        zone = {}
        Mob.Mobs[zoneName] = zone
        
    try:
        mob = zone[mobName]
    except KeyError:
        mob = Mob()
        ret = mob.create(path)
        if ret == False:
            return None

        zone[mobName] = mob

    return mob

def loadAllMob():
    log('�� �ε���... ��ø� ��ٷ��ּ���.')
    pwd = os.getcwd()
    c = 0
    curTime = time.time()
    dirs = os.listdir('data/mob')
    for dir in dirs:
        try:
            os.chdir('data/mob/' + dir)
        except:
            continue
        files = glob.glob('*.mob')
        #print files
        os.chdir(pwd)
        for file in files:
            mob = getMob(dir + ':' + file[:-4])
            if mob != None:
                mob['���̸�'] = dir
                if dir[-1].isdigit():
                    mob['���̵�'] = int(dir[-1])
                mob.setDifficulty()
                c = c + 1
                mob.place()
                mob.timeofregen = curTime
    log(str(c) + '���� ���� �ε��Ǿ����ϴ�.')
    Mob.numMovings = len(Mob.movingMobs)
    log(str( Mob.numMovings ) + '���� Ȱ�� ���� �ε��Ǿ����ϴ�.')
    

