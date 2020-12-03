from include.define import *

from objs.object import Object

from lib.loader import load_script, save_script
from lib.func import *
from lib.hangul import *

class Skills(Object):
    attr = {}
    def __init__(self):
        self.load()
        
    def load(self):
        self.attr = {}
        skills = load_script('data/config/skill.cfg')
        
        for s in skills:
            skill = Skill()
            skill.attr = skills[s]
            skill.name = s
            self.attr[s] = skill
            skill.parse()
        
class Skill(Object):
    def __init__(self):
        Object.__init__(self)
        self.init()
        self.maxturn = 0
        self.bonus = 1
        self.hp = 0
        self.mp = 0
        self.maxhp = 0
        self.all = False
        self.deny = ''
        self._str = 0
        self._dex = 0
        self._arm = 0
        self._mp = 0
        self._maxmp = 0
    
    def init(self):
        self.start_time = 0
        self.step = 0
        self.end = 0
        self.curturn = 0
        
    def parse(self):
        self.getAttr()
        
        if self['종류'] != '전투':
            return
        #{1: [{'초식': '~~~~'}, {'초식': '!!!!!!!!'}], 2: [], 3:[], ...}
        self.pattern = {}
        for line in self['공격'].splitlines():
            words = line.split(None, 2)
            #print line
            turn = int(words[0])
            type = words[1]
            if type != '대기':
                msg = words[2]
            else:
                msg = ''
            if turn not in self.pattern:
                self.pattern[turn] = [{type:msg}]
            else:
                self.pattern[turn].append({type:msg})
        self.maxturn = len(self.pattern)
        
        
    def getAttr(self):
        for config in self['속성'].splitlines():
            if config.find('힘경험치증가') == 0:
                self.bonus = getInt(config.split()[1])
            elif config.find('내공소모') == 0:
                self.mp = getInt(config.split()[1])
            elif config.find('체력소모') == 0:
                self.hp = getInt(config.split()[1])
            elif config.find('체력요구') == 0:
                self.maxhp = getInt(config.split()[1])
            elif config.find('전체무공') == 0:
                self.all = True
            elif config.find('계열금지') == 0:
                self.deny = config.split()[1]
                #if len(attr) == 2:
                #    self.deny = attr[1]
        
        for config in self['방어능력'].splitlines():
            if config.find('힘') == 0:
                self._str = getInt(config.split()[1])
            elif config.find('민첩성') == 0:
                self._dex = getInt(config.split()[1])
            elif config.find('맷집') == 0:
                self._arm = getInt(config.split()[1])
            elif config.find('내공') == 0:
                a, self._mp = getNumberPercent(config.split()[1])
            elif config.find('최고내공') == 0:
                a, self._maxmp = getNumberPercent(config.split()[1])

    def getAntiType(self):
        return self.deny
        
    def is_allAttack(self):
        return self.all
        
    def getScript(self, dex):
        more = True
        start = self.end + 1
        self.curturn += 1
        self.step = int(dex / 700)
        if self.step > self.maxturn - start + 1:
            self.step = self.maxturn - start + 1
        if self.step > self.maxturn:
            dex -= 700 * self.maxturn
        else:
            dex -= 700 * self.step
        self.end = start + self.step - 1

        script = []
        #print self.curturn, self.step, dex, start, self.end
        for i in range(start, self.end + 1):
            if i > self.maxturn:
                print('break')
                break
            if i not in self.pattern:
                break
            r = self.pattern[i]
            for att in r:
                script.append(att)
        if self.end >= self.maxturn:
            self.end = 0
            more = False
        return script, more, dex

def getNumberPercent(buf):
    p = buf.find('%')
    if p != -1:
        return 0, int(buf[:p])
    else:
        return int(buf), 0
        
MUGONG = Skills()
    
