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
        for m in ob.cmdList:
            try:
                if ob.cmdList[m].level == 1000:
                    pass
            except:
                continue
            if ob.cmdList[m].level != 1000:
                continue
            msg += '%20s'% m
            c += 1
            if c % 3 == 0:
                msg += '\r\n'
        ob.sendLine(msg)
