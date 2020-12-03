# -*- coding: euc-kr -*-

from objs.object import Object

from lib.loader import load_script, save_script

class Script(Object):
    
    attr = {}
    
    def __init__(self):
        self.load()
        
    def load(self):
        self.attr = {}
        script = load_script('data/config/script.cfg')
        self.attr = script['메인설정']
        for attr in self.attr:
            self.attr[attr] = self.attr[attr].splitlines()

SCRIPT = Script()

        