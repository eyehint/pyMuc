from twisted.internet import reactor

from lib.func import getInt
from lib.hangul import postPosition1
from lib.loader import load_script
from objs.object import Object


class Doumi(Object):
    attr = {}

    def __init__(self):
        self.load()

    def load(self):
        self.attr = {}
        s = load_script('data/config/doumi.cfg')
        self.attr = s['도우미메인설정']
    
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
        print_line = False
        while True:
            if self.lineNum >= self.lastNum:
                self.player.save()
                self.player.showNotice()
                return
            line = self.script[self.lineNum]
            if line == '':
                self.player.sendLine('')
            elif line[0] == '$':
                l = line.strip()
                if l == '$출력시작':
                    print_line = True
                elif l == '$출력끝':
                    print_line = False
                    self.lineNum += 1
                    continue
                elif l[:2] == '$틱':
                    tick = getInt(l[2:])
                    if tick != 0:
                        self.tick = tick * 0.1 * 1.5
                    self.lineNum += 1
                    continue
                elif l[:4] == '$키입력':
                    key = l.find(':')
                    if key == -1:
                        self.player.input_to(self.player.pressEnter1)
                    else:
                        self.player.input_to(self.player.getKeyInput, l[key + 1:])
                    self.lineNum += 1
                    return
                elif l[:5] == '$이름획득':
                    self.lineNum += 1
                    self.player.write('무림존함ː')
                    self.player.input_to(self.player.getNewname)
                    return
                elif l[:5] == '$암호획득':
                    self.lineNum += 1
                    self.player.write('존함암호ː')
                    self.player.input_to(self.player.getNewpass)
                    return
                elif l[:5] == '$성별획득':
                    self.lineNum += 1
                    self.player.write('성별(남/여)ː')
                    self.player.input_to(self.player.getSex)
                    return
            else:
                msg = line.replace('[공]', self.player['이름'])
                self.player.sendLine(postPosition1(msg))
            self.lineNum += 1
            if print_line == True:
                continue
            reactor.callLater(self.tick, self.run)
            break

DOUMI = Doumi()

