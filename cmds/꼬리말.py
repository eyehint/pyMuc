# -*- coding: euc-kr -*-

from objs.cmd import Command
from include.ansi import *

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('�� ����: [����] ������')
            return
        if len(line) > 20:
            ob.sendLine('�� �ʹ� ��ϴ�.')
            return
        ob['������'] = line
        ob.sendLine('�� �������� ���� �Ͽ����ϴ�.')
