# -*- coding: euc-kr -*-

import copy
from random import randint
from objs.item import getItem
from objs.object import Object
from objs.skill import MUGONG
from objs.oneitem import Oneitem, ONEITEM
from objs.script import Script, SCRIPT
from objs.config import MAIN_CONFIG
from lib.hangul import *
from lib.func import *
from include.define import *
import math

class Body(Object):
    ItemUseLevel = \
    { '����':	'��    ��', '�հ�':	  '   ��   ', '�Ӹ�':	'��    ��',
	  '�Ͱ���':	'�� �� ��', '�����': '�� �� ��', '���':	'��    ��',
	  '����':	'��    ��', '����':   '��    ��', '��ű�':	'�� �� ��',
	  '����':	'��    ��', '�㸮':   '��    ��', '����':	'��    ��',
	  '�尩':	'��    ��', '����':	  '��    ��', '��ȣ':	'��    ȣ',
	  '�Ź�':	'��    ��', '����':	  '��    ��', '��Ÿ':	'��    Ÿ', }
    
    ItemLevelList = \
    [ '����', '�հ�', '�Ӹ�', '�Ͱ���', '�����', '���', '����', '����', '��ű�',
     '����', '�㸮', '����', '�尩', '����', '��ȣ', '�Ź�', '����', '��Ÿ']
    
    strBar = [\
    '[37m��������������������[37m',
    '[31m��[37m������������������[37m',
    '[31m����[37m����������������[37m',
    '[31m������[37m��������������[37m',
    '[33m��������[37m������������[37m',
    '[33m����������[37m����������[37m',
    '[33m������������[37m��������[37m',
    '[32m��������������[37m������[37m',
    '[32m����������������[37m����[37m',
    '[32m������������������[37m��[37m',
    '[32m��������������������[37m']

    difficulty = [
        [2, 1.3, 1.75, 1.75],
        [3.2, 1.88, 2, 2],
        [5.12, 2.7333, 3, 3],
        [8.19, 3.9632, 4, 4],
        [13.11, 5.7467, 5, 5],
        [20.97, 8.3327, 6.5, 6.5],
        [33.55, 12.0823, 9, 9],
        [53.69, 17.5194, 12.5, 12.5],
        [85.9, 25.4031, 16, 16],
    ]
    
    def __init__(self):
        Object.__init__(self)
        self.act = ACT_STAND
        self.tick = 0
        self.skill = None
        self.lastskill = None
        self.attpower = 0
        self.armor = 0
        self.dex = 0
        self._str = 0
        self._dex = 0
        self._arm = 0
        self._mp = 0
        self._maxmp = 0
        self._hp = 0
        self._maxhp = 0
        self._hit = 0
        self._miss = 0
        self._critical = 0
        self._criticalChance = 0
        self._magicChance = 0
        self._exp = 0
        self.weaponItem = None

    def getStr(self):
        if self._str + self['��'] < 0:
            return 0
        return self._str + self['��']
        
    def getDex(self):
        if self._dex + self['��ø��'] < 0:
            return 0
        return self._dex + self['��ø��']
        
    def getArm(self):
        if self._arm + self['����'] < 0:
            return 0
        alpha = 0
        if self['�������'] != '':
            alpha = 1000
        return self._arm + self['����'] + alpha
        
    def getMp(self):
        if self._mp != 0:
            mp = self['����'] + (self['����'] * self._mp) / 100
            return mp
        return self['����']
        
    def getMaxMp(self):
        if self._maxmp != 0:
            # mp = self['�ְ���'] + (self['�ְ���'] * self._maxmp) / 100
            # limit max 
            mp = self['�ְ���'] + self._maxmp
            return mp
        return self['�ְ���']
        
    def getHp(self):
        return self['ü��']
        
    def getMaxHp(self):
        #h = self['�ְ�ü��'] + (self.getArm() - (self['����'] + 14)) * 30
        h = self['�ְ�ü��'] + (self.getArm()) * 30
        if self._maxhp != 0:
            # return h + (h * self._maxhp) / 100
            # limit max 
            return h + self._maxhp
        return h

    def getHit(self):
        if self['����'] == '':
            self['����'] = 0
        if self._hit != 0:
            return self['����'] + self._hit
        return self['����']
        
    def getCritical(self):
        if self['�ʻ�'] == '':
            self['�ʻ�'] = 0
        if self._critical != 0:
            return self['�ʻ�'] + self._critical
        return self['�ʻ�']

    def getCriticalChance(self):
        if self['��'] == '':
            self['��'] = 0
        if self._criticalChance != 0:
            return self['��'] + self._criticalChance
        return self['��']
            
    def getMiss(self):
        if self['ȸ��'] == '':
            self['ȸ��'] = 0
        if self._miss != 0:
            return self['ȸ��'] + self._miss
        return self['ȸ��']
        
    def getBonusExp(self):
        return self._exp

    def getBonusMagicChance(self):
        return self._magicChance

    def setTarget(self, ob):
        self.act = ACT_FIGHT
        ob.act = ACT_FIGHT
        if ob not in self.target:
            self.target.append(ob)
        
    def clearTarget(self, ob = None):
        
        if ob != None:
            if ob in self.target:
                self.target.remove(ob)
            if self in ob.target:
                ob.target.remove(self)
            if self.act == ACT_FIGHT and len(self.target) == 0:
                self.act = ACT_STAND
                self.stopSkill()
            if ob.act == ACT_FIGHT and len(ob.target) == 0:
                ob.act = ACT_STAND
                ob.stopSkill()
            return
        target = copy.copy(self.target)
        for ob in target:
            self.clearTarget(ob)
        
    def getSkill(self, sName):
        if self.lastskill != None:
            if sName == self.lastskill.name:
                self.skill = self.lastskill
                return self.skill
            else:
                del self.lastskill
        self.skill = MUGONG[sName].clone()
        #self.lastskill = self.skill
        return self.skill
        
    def stopSkill(self):
        if self.skill != None:
            self.lastskill = self.skill
            self.skill = None
        
    def clearSkills(self):
        self.stopSkill()
        ss = copy.copy(self.skills)
        for s in ss:
            self.skills.remove(s)
        
    def isMovable(self):
        if self.act == ACT_FIGHT or self.act == ACT_REST:
            return False
        return True

    def init_body(self):
        self.set('����', 1)
        self.set('ü��', 450)
        self.set('�ְ�ü��', 450)
        self.set('��', 15)
        self.set('����', 15)
        self.set('��ø��', 0)
        self.set('����', 100000)
        self.set('����', 0)
        self.set('����', 18)
        self.set('�ְ���', 18)
        self.set('����', 18)
        self.set('���̿���ƽ', 0)
        self.set('�������ġ', 0)
        self.set('1 ���õ�', 0)
        self.set('2 ���õ�', 0)
        self.set('3 ���õ�', 0)
        self.set('4 ���õ�', 0)
        self.set('5 ���õ�', 0)
        self.set('1 ���õ�����ġ', 0)
        self.set('2 ���õ�����ġ', 0)
        self.set('3 ���õ�����ġ', 0)
        self.set('4 ���õ�����ġ', 0)
        self.set('5 ���õ�����ġ', 0)
        self.set('������ġ', 0)
        self.set('��ø������ġ', 0)
        self.set('0 ������ų', 0)
        self.set('1 ������ų', 0)
        self.set('2 ������ų', 0)
        self.set('�������õ�', '')
        self.set('�����̸�', '')
        self.set('�����', 0)
        
    def GetHPString(self):
        scripts = SCRIPT['����ڽ�ũ��']
        cnt = len(scripts)
        if cnt == 0:
            return ''
        s = scripts[(cnt - 1) - ((cnt - 1) * self.getHp()) / self.getMaxHp()]
        s = self['�̸�'] + postPosition(s, self['�̸�'])
        return s
        
    def getItemWeight(self):
        w = 0
        for obj in self.objs:
            if obj.checkAttr('�����ۼӼ�', '��¾���'):
                continue
            w += getInt(obj['����'])
        return w
        
    def getItemCount(self):
        c = 0
        for item in self.objs:
            if item.checkAttr('�����ۼӼ�', '��¾���'):
                continue
            c += 1
        return c
        
    def getInvenItemCount(self):
        c = 0
        for item in self.objs:
            if item.checkAttr('�����ۼӼ�', '��¾���') or item.inUse:
                continue
            c += 1
        return c
    
    def getTotalExp(self):
        cc = self['����']
        c =(((cc * cc) / 3) + 30) * (cc + 4)
        n = MAIN_CONFIG['�ְ����ġ']
#        if cc >= 1800:
#            return cc * 200000 
#        if  n < 1: 
#            n = MAX_INT
        if c < 1:
            c = 1
#        if c > n:
#            c = n
        if c > n:
            N = 200
            if self['����'] >= 3000:
                N = int(self['����'] / 10)
            c1 = getInt(self['����'])
            c2 = c1 + 200

            a = ((c2 * c2) / 3) + 30
            b = (a * (c2 - c1)) / 100
            c = (a + b) * N
        return	c
        
    def addExp(self, exp):
        self['�������ġ'] += exp
        t_exp = self.getTotalExp()
        if self['�������ġ'] >= t_exp:
            #self['�������ġ'] -= t_exp
            self['�������ġ'] = 0
            self['����'] += 1
            self.levelUp()
        
    def addStr(self, str, check = True):
        self['������ġ'] += str
        c = (self['��'] - 10) * 20
        if check and self['������ġ'] >= c:
            self['������ġ'] = 0
            self['��'] += 1
            self.sendLine(MAIN_CONFIG['��������ũ��'])
    
    def addDex(self, dex):
        self['��ø������ġ'] += dex
        c = (self['��ø��'] + 4) * 8
        if self['��ø������ġ'] >= c:
            self['��ø������ġ'] = 0
            if self['��ø��'] < MAIN_CONFIG['��ø���ְ��ġ']:
                self['��ø��'] += 1
                self.sendLine(MAIN_CONFIG['��ø��������ũ��'])

    def addAnger(self):
        anger = getInt(self['�г�'])
        
        if anger >= 600:
            return
        anger += 1
        if anger == 100:
            self.sendFightScript('����� ���ڱ� [1;40;31m����[0;40;37m�� ������ [1;40;31m����[0;40;37m�� �θ��ϴ�. \'����������~~\'')
            self.sendFightScriptRoom('%s ���ڱ� [1;40;31m����[0;40;37m�� ������ [1;40;31m����[0;40;37m�� �θ��ϴ�. \'����������~~\'' % self.han_iga())
        self['�г�'] = anger
        
    def levelUp(self):
        self.sendLine(MAIN_CONFIG['����������ũ��'])
        hpUp = randint(0, 9) + 25;
        self['�ְ�ü��'] += hpUp
        self['����'] += 1
        self['ü��'] = self.getMaxHp()
        self['����'] = self.getMaxMp()
        self.sendLine('�� ü�� ��� �� %d��%d��, ���� ��� �� 1��%d��' % \
        ( hpUp, self['�ְ�ü��'], self['����']))
        if self['����'] >= 2000:
            self['Ư��ġ'] += 1
        else:
            if self['����'] % 10 == 0:
                self['Ư��ġ'] += 1

    def loadSkillUp(self):
        self.skillMap = {}
        lines = self['�������õ�'].splitlines()
        for line in lines:
            words = line.split()
            self.skillMap[words[0]] = (int(words[1]), int(words[2]))
            
    def buildSkillUp(self):
        msg = ''
        for sup in self.skillMap:
            msg += '%s %d %d\r' % (sup, self.skillMap[sup][0], self.skillMap[sup][1])
        self['�������õ�'] = msg
        
    def skillUp(self, s = None):
        if s == None:
            s = self.skill

        if s.name not in self.skillMap:
            self.skillMap[s.name] = (1, 0)
        
        s1 = self.skillMap[s.name][0]
        s2 = self.skillMap[s.name][1]
        s2 += 1
        if s2 >= s['Ȯ������']:
            s1 += 1
            s2 = 0
            if s1 > 10:
                return
            else:
                self.sendLine('[1m����� ������ ��ġ������ ���������� ������ ���°��� �����ϴ�.[0m[40m[37m')
        self.skillMap[s.name] = (s1, s2)
        
    def weaponSkillUp(self, n = 1):
        type = self.getWeaponType()
        buf1 = '%d ���õ�' % type
        buf2 = '%d ���õ�����ġ' % type
        c = getInt(self[buf1])
        cc = getInt(self[buf2])
        cc += n
        self[buf2] = cc
        c = (c + 5 ) * 7
        if cc >= c:
            self[buf1] += 1
            self[buf2] = 0
            self.sendLine(MAIN_CONFIG['���õ�������ũ��'])
            
    def getAttackFailScript(self, mob):
        s = SCRIPT[self.getWeaponFightType() + '�������н�ũ��']
        s = s[randint(0, len(s) - 1)]
        return self.makeFightScript(s, mob)
        
    def getAttackScript(self, mob, dmg, c1, c2):
        s = SCRIPT[self.getWeaponFightType() + '������ũ��']
        if len(s) == 0:
            return '���׹��׹��׹��׹��׹��׹��׹��׹��׹��׽Ű��ϼ��Ű��ϼ�'
        s = s[randint(0, len(s) - 1)]
        return self.makeFightScript(s, mob)
        
    def getSkillChance(self, mob):
        l1 = self['����']
        l2 = mob['����']
        
        # limit attack level
        if (l2 - l1) >= MAIN_CONFIG['�ִ��ɷ�������']:
            return -1        
        
        if self.skill != None:
            CHANCE = self.skill['Ȯ��']
            #�������õ� �߰��ʿ�
            if self.skill.name in self.skillMap:
                CHANCE += self.skillMap[self.skill.name][0] * MAIN_CONFIG['���Ȯ�����']
        else:
            CHANCE = 100
        bonus = self.getHit() * float(MAIN_CONFIG['����Ȯ��'])
        bonus -= mob.getMiss() * float(MAIN_CONFIG['ȸ��Ȯ��']) 
            
        return CHANCE - (((l2-l1)+90)/3) + bonus
        
    def getAttackChance(self, mob):
        l1 = self['����']
        l2 = mob['����']
        
        # limit attack level
        if (l2 - l1) >= MAIN_CONFIG['�ִ��ɷ�������']:
            return -1
        
        CHANCE = 100
        bonus = self.getHit() * float(MAIN_CONFIG['����Ȯ��'])
        bonus -= mob.getMiss() * float(MAIN_CONFIG['ȸ��Ȯ��']) 
        return CHANCE - (((l2-l1)+90)/3) + bonus
        
    def getAttackPoint(self, mob):
        item = self.getWeapon()
        s1 = 0
        from objs.player import is_player
        if is_player(self): 
            if item != getItem('�ָ�'):
                s1 = getInt(item['�ⷮ'])
        s2 = getInt(self['%d ���õ�' % self.getWeaponType()])
        if self['���õ����'] != '':
            s2 += 2000 
        ss = s1 - s2;
        if ss < 0:
            ss = 0
        c1 = self.getStr() * 2
        if is_player(self): 
            #c1 += math.sqrt( self.getStr() * self.getMaxMp() )
            c1 += self.getMaxMp() / 4
        c2 = self.getAttPower() - ss
        m1 = (c1 + c2) - (mob.getArm() + mob.getArmor())
        if m1 < 1:
            m1 = 1
        m = m1
        #print 's1=%d, s2=%d, ss=%d, c1=%d, c2=%d, m1=%d, m=%d' % (s1, s2, ss, c1, c2, m1, m)
        c1 = int(m * 0.80)
        c2 = int(m * 1.20)
        
        s1 = c2 - c1 + 1
        #print 's1=%d, c1=%d, c2=%d' % (s1, c1, c2)
        if s1 < 1:
            s1=1;
    
        m = randint(0, s1 - 1) + c1
        
        if m < 1:
            m = 1
        #print 'c1=%d, c2=%d, m=%d' % (c1, c2, m)
        return int(m), c1, c2
        
    def getArmor(self):
        return self.armor
        
    def getAttPower(self):
        return self.attpower
        
    def getSkillPoint(self, mob):
        m, c1, c2 = self.getAttackPoint(mob)
        f = float(self.skill['Ÿ�ݷ�'])
        
        if f <= 0:
            f = 0.1
        m += m * f
        m = int(m)
        chance = self.getCriticalChance() * float(MAIN_CONFIG['��Ȯ��'])
        bonus = 1
        if chance > randint(0, 100):
            bonus = self.getCritical() * float(MAIN_CONFIG['�ʻ���'])
            if bonus < 1:
                bonus = 1
        return int(m * bonus)
        
    def getWeaponType(self):
        return self.getWeapon()['��������']
        
    def getWeaponFightType(self):
        #���� Ÿ���� �ʿ���
        return self.getWeapon()['������ũ��']
        
    def getWeapon(self):
        if self.weaponItem != None:
            return self.weaponItem
        return getItem('�ָ�')
        
    def makeFightScript(self, line, mob, weapon = None):
        if mob == None:
            mName = ''
        else:
            mName = mob.getNameA()
            
        if weapon == None:
            m = self.getWeapon()
            if m == getItem('�ָ�'):
                mstr = '[36m�ָ�[37m'
            else:
                mstr = m.getNameA()
        else:
            mstr = weapon.getNameA()
            
        buf1 = line.replace('[��]', '���')
        buf1 = buf1.replace('[��]', mName)
        buf1 = buf1.replace('[��]', mstr)
        buf1 = postPosition1(buf1)
        buf1 = postPosition1(buf1)
        buf1 = postPosition1(buf1)
        
        buf2 = line.replace('[��]', self.getNameA())
        buf2 = buf2.replace('[��]', '���')
        buf2 = buf2.replace('[��]', mstr)
        buf2 = postPosition1(buf2)
        buf2 = postPosition1(buf2)
        buf2 = postPosition1(buf2)
        
        buf3 = line.replace('[��]', self.getNameA())
        buf3 = buf3.replace('[��]', mName)
        buf3 = buf3.replace('[��]', mstr)
        buf3 = postPosition1(buf3)
        buf3 = postPosition1(buf3)
        buf3 = postPosition1(buf3)
        
        return buf1, buf2, buf3
    
    def sendLine(self, line):
        return
    
    def sendRoom(self, line):
        return
        
    def writeRoom(self, line):
        return
        
    def sendRoomFightScript(self, line):
        return
        
    def lpPrompt(self):
        return
        
    def checkDefenceSkill(self):
        skills = copy.copy(self.skills)
        msg = '\r\n'
        autoSkill = []
        for s in skills:
            s.start_time -= 1
            if s.start_time < 0:
                self.skills.remove(s)
                self._str -= s._str
                self._dex -= s._dex
                self._arm -= s._arm
                self._mp -= s._mp
                self._maxmp -= s._maxmp
                buf1, buf2, buf3 = self.makeFightScript(s['����������ũ��'], None)
                msg += buf1 + '\r\n'
                autoSkill.append(s.name)
                del s
        if len(msg) != 2:
            self.write(msg)
            self.lpPrompt()
            self.sendFightScriptRoom(buf3)
            
        if len(autoSkill) != 0 and '�ڵ�����' in self.alias:
            a = self.alias['�ڵ�����']
            askill = a.split(';')
            for s in autoSkill:
                if s in askill:
                    self.do_command('%s ����' % s)

    def checkItemSkill(self):
        m = self.getWeapon()
        if m == getItem('�ָ�'):
            return
        mlist = m['�����̸�'].splitlines()
        if len(mlist) == 0:
            return
        mName = m['�̸�']
        if m['�̸�'] not in self.itemSkillMap:
            self.itemSkillMap[mName] = 1
        else:
            self.itemSkillMap[mName] += 1
        p = self.itemSkillMap[mName]
        for s in mlist:
            words = s.split()
            sName = words[0]
            if sName in self.skillList:
                continue
            type = words[1]
            if type != '����':
                if self['����'] != type and self['����'] != '����' and self['����'] != '����':
                    continue
            n1 = int(words[2])
            count = self.itemSkillMap[mName]
            if count < n1:
                continue
            n2 = int(words[3])
            if p % n2 != 0:
                continue
            n3 = int(words[4])
            
            r = randint(0, 99)
            #print n1, n2, n3, r
            if  count < 2500000 and r > n3:
                continue

            self.skillList.append(sName)
            self.itemSkillMap[mName] = 0
            self.sendLine('\r\n[1m[40m[37m����� ��[1m[40m[32m%s[1m[40m[37m���� ���� ������ ����ġ�� �����մϴ�. \'�ĥץΥ��~\'[0m[40m[37m\r\n' % sName)
            self.sendRoom('[1m[40m[37m%s ��[1m[40m[32m%s[1m[40m[37m���� ���� ������ ����ġ�� �����մϴ�. \'�ĥץΥ��~\'[0m[40m[37m' % (self.getNameA(), sName))
            attr = m['�����ۼӼ�'].splitlines()
            for at in attr:
                if at.find('��������ļҸ�') == 0:
                    m.inUse = False
                    self.armor -= getInt(m['����'])
                    self.attpower -= getInt(m['���ݷ�'])
                    m.env = None
                    self.weaponItem = None 
                    self.objs.remove(m) 
                    del m
                    break
            break
            
    def loadSkills(self):
        for line in self['��������'].splitlines():
            words = line.split()
            s = MUGONG[words[0]]
            s = copy.copy(s)
            self.skills.append(s)
            s.start_time = int(words[1])
            self._str += s._str
            self._dex += s._dex
            self._arm += s._arm
            self._mp += s._mp
            self._maxmp += s._maxmp
    
    def buildSkills(self):
        self['��������'] = ''
        for s in self.skills:
            buf = '%s %d' % (s.name, s.start_time)
            self.setAttr('��������', buf)
            
    def loadSkillList(self):
        self.skillList = self['�����̸�'].splitlines()
        lines = self['�����̸����ø���Ʈ'].splitlines()
        for line in lines:
            words = line.split()
            self.itemSkillMap[words[0]] = int(words[1])
        
    def buildSkillList(self):
        msg = ''
        for s in self.skillList:
            msg += s + '\r\n'
        self['�����̸�'] = msg
        
        msg = ''
        for s in self.itemSkillMap:
            msg += '%s %s\r\n' % (s, self.itemSkillMap[s])
        self['�����̸����ø���Ʈ'] = msg

    def unwearAll(self):
        self.attpower = 0
        self.armor = 0
        self._str = 0
        self._dex = 0
        self._arm = 0
        self._mp = 0
        self._maxmp = 0
        self._hp = 0
        self._maxhp = 0
        self._hit = 0
        self._miss = 0
        self._critical = 0
        self._criticalChance = 0
        self._magicChance = 0
        self._exp = 0
        for item in self.objs:
            if item.inUse == True:
                item.inUse = False
                if item['����'] == '����':
                        self.weaponItem = None

    def dropAllItem(self):
        p = self.getInsureCount()
        self.insure = 0
        nCnt = {}
        nFail = {}
        c = 0
        objs = copy.copy(self.objs)
        for item in objs:
            if p > 0 and item.checkAttr('�����ۼӼ�', '��������ȵ�') == False:
                self.insure += 1
                continue
            if item.checkAttr('�����ۼӼ�', '�ټ�����'):
                continue
            if item.checkAttr('�����ۼӼ�', '����������'):
                continue
            if item.checkAttr('�����ۼӼ�', '��¾���'):
                continue
            if item.checkAttr('�����ۼӼ�', '���Ͼ�����'):
                ONEITEM.drop2(item.index, self['�̸�'])
            item.inUse = False
            self.objs.remove(item)
            c += 1
            if self.env.getItemCount() < 50:
                self.env.insert(item)
                item.drop()
                nc = 0
                try:
                    nc = nCnt[item['�̸�']]
                except:
                    nCnt[item.get('�̸�')] = 0
                nCnt[item.get('�̸�')] = nc + 1
            else:
                nc = 0
                try:
                    nc = nFail[item.get('�̸�')]
                except:
                    nFail[item.get('�̸�')] = 0
                nFail[item.get('�̸�')] = nc + 1
                del item
        self.decInsureCount()
        if c == 0:
            return
            
        for name in nCnt:
            nc = nCnt[name]
            if nc == 1:
                self.sendLine('����� [36m' + name + '[37m' + han_obj(name) + ' ����߸��ϴ�.')
            else:
                self.sendLine('����� [36m' + name + '[37m %d���� ����߸��ϴ�..' % nc)
        for name in nFail:
            nc = nFail[name]
            if nc == 1:
                self.sendLine('����� [36m' + name + '[37m' + han_obj(name) + ' ����߸��� �ٷ� �μ����ϴ�.')
            else:
                self.sendLine('����� [36m' + name + '[37m %d���� ����߸��� �ٷ� �μ����ϴ�.' % nc)
        
        
    def decInsureCount(self):
        p = self['�����']
        c1 = self['����'] * MAIN_CONFIG['�����ܰ�']
        c2 = c1 * MAIN_CONFIG['���������'] / 100
        p -= c2
        if p < 0:
            p = 0
        self['�����'] = p
        
    def getInsureCount(self):
        return getInt(self['�����']) / (self['����'] * MAIN_CONFIG['�����ܰ�'])
        
    def addFollow(self, f):
        self.follow = f
        f.addFollower(self)
        self.sendLine('����� %s ����ٴϱ� �����մϴ�.' % f.han_obj())
        
    def delFollow(self, other = False):
        if self.follow != None:
            if other == True:
                self.sendLine('')
            self.sendLine('����� %s ����ٴϴ� ���� �׸��Ӵϴ�.' % self.follow.han_obj())
            if other == True:
                self.lpPrompt()
            self.follow.delFollower(self)
            self.follow = None
        
    def addFollower(self, f):
        if f not in self.follower:
            self.follower.append(f)
            self.sendLine('\r\n%s ����� ����ٴϱ� �����մϴ�.' % f.han_iga())
            self.lpPrompt()
            
    def delFollower(self, f = None, noPrompt = False):
        if f != None:
            if f in self.follower:
                self.follower.remove(f)
                self.sendLine('\r\n%s ��Ű� ����ٴϴ� ���� �׸��Ӵϴ�.' % f.han_iga())
                self.lpPrompt()
            return
        fs = copy.copy(self.follower)
        for f in fs:
            f.delFollow(True)
        self.follower = []
        
    def recoverDemage(self, dmg):
        t = 0
        if dmg == 0:
            return 0
        for s in self.skills:
            if s['�迭'] == '����ȸ��':
                p = int(s['ȸ���ɷ�'].split()[1])
                r = dmg * p / 100
                t += r
                if self.checkConfig('���ø��') == False:
                    buf1, buf2, buf3 = self.makeFightScript(s['ȸ����ũ��'], None)
                    self.sendLine(buf1 + ' ([1;32m+ %d[0;37m)' % r)
        return t
        
    def minusHP(self, demage, mode = True, who = None):
        cc = self.get('ü��')
        cc -= demage

        if cc <= 0:
            self.set('ü��', 0)
            self.die(mode)
            return True
        self.set('ü��', cc)
        return False

    def checkVision(self, skill):
        line = self['��������']
        if line == '':
            return
        if skill == None:
            return
        if skill.name not in line:
            return
        var = line.split()
        if len(var) == 1:
            p = 0
        else:
            p = int(var[1])
        n1 = 10
        n2 = 10
        
        n3 = 1
        if randint(0, 99) > 1:
            p += 1
            self['��������'] = '%s %d' % (var[0], p) 
            return
        self.attr.__delitem__('��������')
        if self['�����̸�'] == '':
            self['�����̸�'] = var[0]
        else:
            self['�����̸�'] += '\r\n' + var[0]
        self.sendLine('[1m����� ��[32m%s[37m���� ���� ������ ����ġ�� �����մϴ�. \'�ĥץΥ��~\'[0;37m\r\n' % var[0])
        self.sendRoom('[1m%s ��[32m%s[37m���� ���� ������ ����ġ�� �����մϴ�. \'�ĥץΥ��~\'[0;37m' % (self.han_iga(), var[0]))
