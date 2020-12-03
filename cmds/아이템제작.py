# -*- coding: euc-kr -*-

from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):
    def cmd(self, ob, line):
        words = line.split()
        if len(words) < 1:
            ob.sendLine('�� ����: [���ϸ�] ����������')
            return
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^')
            return
        ob.write('�ۼ��� ��ġ�÷��� \'.\' �� �Է��ϼ���.\r\n:')
        ob.INTERACTIVE = 0
        ob._lineData = ''
        ob._lineDataTarget = 'item/' + words[0] + '.itm'
        ob.input_to(ob.write_edit)

