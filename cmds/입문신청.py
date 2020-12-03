# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob['�Ҽ�'] != '':
            ob.sendLine('�� ���Ŀ� �Թ� ��û�� �� �� �����ϴ�.')
            return
            
        if line == '':
            ob.sendLine('�� ���� : [�����̸�] �Թ���û')
            return

        obj = ob.env.findObjName(line)
        if obj == None  or is_player(obj) == False:
            ob.sendLine('�� �̰��� �׷� �������� �����ϴ�.')
            return
        if obj == ob:
            ob.sendLine('�� �ڱ� �ڽ��Դϴ�.')
            return
        if obj['����'] != '����' and obj['����'] != '�ι���':
            ob.sendLine('�� ������ ���ָ��� �� �� �ֽ��ϴ�.')
            return
        if obj['����'] == '����':
            if ob['����'] != '����' and ob['����'] != '����' and ob['����'] != obj['��������']:
                ob.sendLine('�� ���Ŀ� �Թ� ��û�� �� �� �����ϴ�.')
                return
        elif obj['����'] == '����' and ob['����'] == '':
            ob.sendLine('�� ���Ŀ� �Թ� ��û�� �� �� �����ϴ�.')
            return
        else:
             if ob['����'] != '����' and ob['����'] != '����' and obj['����'] != ob['����']:
                ob.sendLine('�� ���Ŀ� �Թ� ��û�� �� �� �����ϴ�.')
                return
        if obj.checkAttr('�Թ���û��', ob['�̸�']):
            ob.sendLine('�� �̹� �Թ� ��û�� �Ͽ����ϴ�.')
            return
        obj.setAttr('�Թ���û��', ob['�̸�'])
        ob.sendLine('����� %s�� ���Ŀ� �Թ��� ��û�մϴ�.' % obj.getNameA())
        obj.sendLine('\r\n%s ����� ���Ŀ� �Թ��� ��û�մϴ�.' % ob.han_iga())
        obj.lpPrompt()
