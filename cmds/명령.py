# -*- coding: euc-kr -*-

from objs.cmd import Command
from include.ansi import *

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        words = line.split(None, 1)
        if line == '' or len(words) < 2:
            ob.sendLine('�� ��� ���: [���] [����] ���')
            return
        
        obj = ob.env.findObjName(words[0])
        if obj == None or is_player(obj) == False:
            ob.sendLine('�� �׷� ����� �����. *^_^*')
            return
        obj.sendLine('')
        obj.do_command(words[1])
        
        

