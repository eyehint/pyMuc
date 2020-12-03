# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob['����'] != '����':
            ob.sendLine('�� ������ ���ָ��� �� �� �ֽ��ϴ�.')
            return
        if line == '':
            ob.sendLine('�� ���� : [���] ���ֱ��Ѿ絵')
            return

        obj = ob.env.findObjName(line)
        if obj == None or is_player(obj) == False:
            ob.sendLine('�� �̰��� �׷� �������� �����ϴ�.')
            return
        if obj == ob:
            ob.sendLine('�� �̹� ����� ���� �Դϴ�.')
            return
        if obj['�Ҽ�'] != ob['�Ҽ�']:
            ob.sendLine('�� ����� �Ҽ��� �ƴմϴ�.')
            return
        if obj['����'] != '�ι���':
            ob.sendLine('�� ���ֱ����� �ι��ֿ��Ը� �絵�� �� �ֽ��ϴ�.')
            return
        if MAIN_CONFIG['�ι��־絵����'] > obj['����']:
            ob.sendLine('�� ���ְ� �Ǳ⿡�� ������ �����մϴ�.')
            return
        
        obj['����'] = '����'
        ob['����'] = '�ι���'
        g = GUILD[ob['�Ҽ�']]
        g['�ι��ָ���Ʈ'].append(ob['�̸�'])
        g['�ι��ָ���Ʈ'].remove(obj['�̸�'])
        g['�����̸�'] = obj['�̸�']
        GUILD.save()

        msg = '%s %s ���ַ� �����̾��� �����մϴ�.' % (ob.han_iga(), obj.han_obj())
#obj.sendLine('\r\n����� �Ĺ��Ǿ����ϴ�.')
        obj.lpPrompt()
        ob.sendGroup(msg, prompt = True)
        
