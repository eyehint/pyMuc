# -*- coding: euc-kr -*-

from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):
    def cmd(self, ob, line):
        words = line.split()
        if len(words) < 2:
            ob.sendLine('�� ����: [���̸�] [���̸�] ������')
            return
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^')
            return
        ob.write('�ۼ��� ��ġ�÷��� \'.\' �� �Է��ϼ���.\r\n:')
        ob.INTERACTIVE = 0
        ob._lineData = ''
        ob._lineDataTarget = 'mob/' + words[0] + '/'+ words[1] + '.mob'
        ob.input_to(ob.write_edit)

