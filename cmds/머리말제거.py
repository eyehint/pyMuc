# -*- coding: euc-kr -*-

from objs.cmd import Command
from include.ansi import *

class CmdObj(Command):

    def cmd(self, ob, line):
        ob['�Ӹ���'] = ''
        ob.sendLine('�� �Ӹ����� ���� �Ͽ����ϴ�.')
