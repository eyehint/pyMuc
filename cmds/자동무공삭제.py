# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob['�ڵ�����'] == '':
            ob.sendLine('�� �ڵ����� : ����')
            return
        ob['�ڵ�����'] = ''
        ob.sendLine('�� �ڵ������� �����Ͽ����ϴ�.')
