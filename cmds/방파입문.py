# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob['����'] != '����' and ob['����'] != '�ι���':
            ob.sendLine('�� ������ ���ָ��� �� �� �ֽ��ϴ�.')
            return
            
        if line == '':
            ob.sendLine('�� ���� : [���] �����Թ�')
            return

        obj = ob.env.findObjName(line)
        if obj == None or is_player(obj) == False:
            ob.sendLine('�� �̰��� �׷� �������� �����ϴ�.')
            return
        if obj == ob:
            ob.sendLine('�� �ڱ� �ڽ��Դϴ�.')
            return

        if ob.checkAttr('�Թ���û��', obj['�̸�']) == False:
            ob.sendLine('�� ���ĸ� ��û�� �׷� �������� �����ϴ�.')
            return
        ob.delAttr('�Թ���û��', obj['�̸�'])
        
        ob.sendLine('����� %s ���Ŀ� �Թ��������� �����մϴ�.' % obj.han_obj())
        obj.sendLine('\r\n%s ����� ���Ŀ� �Թ��������� �����մϴ�.' % ob.han_iga())
        obj.lpPrompt()
        obj['�Ҽ�'] = ob['�Ҽ�']
        obj['����'] = '������'
        g = GUILD[obj['�Ҽ�']]
        if '�����θ���Ʈ' not in g:
            g['�����θ���Ʈ'] = [obj['�̸�']]
        else:
            g['�����θ���Ʈ'].append(obj['�̸�'])
        g['���Ŀ���'] += 1
        GUILD.save()
        #���Ŀ��鿡�Ե� �˷�����!!
