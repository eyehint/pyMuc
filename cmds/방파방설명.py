# -*- coding: euc-kr -*-

from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):
    level=2000
    def cmd(self, ob, line):
        if ob['����'] != '����' and ob['����'] != '�ι���':
            ob.sendLine('�� ������ ���ָ��� �� �� �ֽ��ϴ�.')
            return
        if line == '':
            ob.sendLine('�� ����: [�̸�] ���Ĺ��̸�')
            return
        if ob.env['��������'] == '':
            ob.sendLine('�� �������� �ƹ������� �̸��� ������ �ʴ´ٳ�.')
            return
            
        if ob.env['��������'] != ob['�Ҽ�']:
            ob.sendLine('�� �������� �ƹ������� �̸��� ������ �ʴ´ٳ�.')
            return
        ob.write('�� ���� �ۼ��� ��ġ�÷��� \'.\' �� �Է��ϼ���.\r\n:')
        ob.INTERACTIVE = 0
        ob._lineData = ''
        ob._lineDataTarget = ob.env
        ob._lineDataValue = '����'
        ob.input_to(ob.write_lines)

