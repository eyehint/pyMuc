# -*- coding: euc-kr -*-

from objs.object import Object

from lib.loader import load_script, save_script

class Help(Object):
    
    attr = {}
    
    def __init__(self):
        self.load()
        
    def load(self):
        help = load_script('data/config/help.cfg')
        self.attr = help['����']

    def save(self):
        o = {}
        o['����'] = self.attr
        try:
            f = open('data/config/help.cfg', 'w')
        except:
            return False
        save_script(f, o)
        f.close()
        return True
        
HELP = Help()
        