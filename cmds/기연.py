# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
            
        msg = ''
        for index in ONEITEM.attr:
            owner = ONEITEM.attr[index]
            name = ONEITEM.getName(index)
            msg += '%-16s (%-16s) : %s\r\n' % (name, index, owner)
        ob.sendLine(msg)
