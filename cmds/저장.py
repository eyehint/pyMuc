# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        res = ob.save()
        if res == True:
            ob.sendLine('* ���� �Ǿ����ϴ�.')
        else:
            ob.sendLine('* ���� ����!!!')
