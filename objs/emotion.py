# -*- coding: euc-kr -*-

from objs.object import Object

from lib.loader import load_script, save_script
from lib.hangul import postPosition1

class Emotion(Object):
    
    attr = {}
    
    def __init__(self):
        self.load()
        
    def load(self):
        self.attr = {}
        help = load_script('data/config/emotion.cfg')
        e = help['����ǥ��']
        for key in e:
            keys = key.split()
            for k in keys:
                self.attr[k] = e[key]
                
    def replace(self, line, sub):
        if sub == '':
            return line
        s = line.find('"')
        if s == -1:
            return line
        e = line.find('"', s + 1)
        if e == -1:
            return line
        return line[:s+1] + sub + line[e:]

    def makeScript(self, line, I, U, sub):
        line = self.replace(line, sub)
        if U == None:
            buf1 = line.replace('[��]', '���')
            buf1 = postPosition1(buf1)
            
            buf3 = line.replace('[��]', I)
            buf3 = postPosition1(buf3)
            return buf1, '', buf3
        else:
            
            buf1 = line.replace('[��]', '���')
            buf1 = buf1.replace('[��]', U)
            buf1 = buf1.replace('[�漺]', U)
            buf1 = postPosition1(buf1)
            buf1 = postPosition1(buf1)
            buf1 = postPosition1(buf1)
            
            buf2 = line.replace('[��]', I)
            buf2 = buf2.replace('[��]', '���')
            buf2 = buf2.replace('[�漺]', '���')
            buf2 = postPosition1(buf2)
            buf2 = postPosition1(buf2)
            buf2 = postPosition1(buf2)
            
            buf3 = line.replace('[��]', I)
            buf3 = buf3.replace('[��]', U)
            buf3 = buf3.replace('[�漺]', U)
            buf3 = postPosition1(buf3)
            buf3 = postPosition1(buf3)
            buf3 = postPosition1(buf3)
            return buf1, buf2, buf3

EMOTION = Emotion()
