# -*- coding: euc-kr -*-
from twisted.internet import reactor

from objs.object import Object

from lib.loader import load_script, save_script
from lib.func import getInt
from lib.hangul import postPosition1
from objs.skill import MUGONG

class Doumi(Object):
    
    attr = {}
    
    def __init__(self):
        self.load()
        
    def load(self):
        self.attr = {}
        s = load_script('data/config/doumi.cfg')
        self.attr = s['����̸��μ���']
    
class autoScript():
    def start(self, script, player):
        self.tick = 0.5
        self.lineNum = 0
        self.player = player
        self.script = script
        self.lastNum = len(self.script)
        self.run()
        self.name = ''
        
    def run(self):
        if self.player == None:
            return
        from objs.player import Player
        printLine = False
        while(True):
            if self.lineNum >= self.lastNum:
                self.player.save()
                self.player.showNotice()
                return
            line = self.script[self.lineNum]
            if line == '':
                self.player.sendLine('')
            elif line[0] == '$':
                l = line.strip()
                if  l == '$��½���':
                    printLine = True
                elif l == '$��³�':
                    printLine = False
                    self.lineNum += 1
                    continue
                elif l[:3] == '$ƽ':
                    tick = getInt(l[4:])
                    if tick != 0:
                        self.tick = tick * 0.1 * 1.5
                    self.lineNum += 1
                    continue
                elif l[:7] == '$Ű�Է�':
                    key = l.find(':')
                    if key == -1:
                        self.player.input_to(self.player.pressEnter1)
                    else:
                        self.player.input_to(self.player.getKeyInput, l[key + 1:])
                    self.lineNum += 1
                    return
                elif l[:9] == '$�̸�ȹ��':
                    self.lineNum += 1
                    self.player.write('�������Ԣ�')
                    self.player.input_to(self.player.getNewname)
                    return
                elif l[:9] == '$��ȣȹ��':
                    self.lineNum += 1
                    self.player.write('���Ծ�ȣ��')
                    self.player.input_to(self.player.getNewpass)
                    return
                elif l[:9] == '$����ȹ��':
                    self.lineNum += 1
                    self.player.write('����(��/��)��')
                    self.player.input_to(self.player.getSex)
                    return
            else:
                msg = line.replace('[��]', self.player['�̸�'])
                self.player.sendLine(postPosition1(msg))
            self.lineNum += 1
            if printLine == True:
                continue
            reactor.callLater(self.tick, self.run)
            break

DOUMI = Doumi()

        
