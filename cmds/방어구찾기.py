# -*- coding: euc-kr -*-

from objs.cmd import Command
from include.ansi import *

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        c = 0
        for index in Item.Items:
            item = Item.Items[index]
            if item['����'] == '��':
                c += 1
                ob.sendLine('%s : %s'% (item.getNameA(), item.index))
        if c == 0:
            ob.sendLine('�� ã���ô� �������� �����ϴ�.')
        

