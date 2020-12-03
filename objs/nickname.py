# -*- coding: euc-kr -*-

from objs.object import Object

from lib.loader import load_script, save_script

class Nickname(Object):
    
    attr = {}
    
    def __init__(self):
        self.load()
    
    def save(self):
        o = {}
        o['������ȣ'] = self.attr
        try:
            f = open('data/config/nickname.cfg', 'w')
        except:
            return False
        save_script(f, o)
        f.close()
        return True
        
    def load(self):
        script = load_script('data/config/nickname.cfg')
        self.attr = script['������ȣ']
        
NICKNAME = Nickname()
        