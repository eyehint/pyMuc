# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob['��������'] == '':
            ob.sendLine('�� ������ ������ �����ϴ�.')
            return
        ob['��������'] = ''
        ob.sendLine('�� ������ ������ �����մϴ�.')
