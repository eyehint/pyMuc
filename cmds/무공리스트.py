# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        msg = ''
        c = 0
        for m in MUGONG.attr:
            msg += '%14s,'% m
            c += 1
            if c % 5 == 0:
                msg += '\r\n'
        ob.sendLine(msg)
