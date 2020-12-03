# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
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
        if len(line) > 20:
            ob.sendLine('�� �ʹ� ����.')
            return

        ob.env['�̸�'] = line
        ob.env.save()
        ob.sendLine('�̸��� ���� �Ǿ����ϴ�.')
        
