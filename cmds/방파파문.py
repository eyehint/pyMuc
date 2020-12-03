# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob['����'] != '����':
            ob.sendLine('�� ������ ���ָ��� �� �� �ֽ��ϴ�.')
            return
        if line == '':
            ob.sendLine('�� ���� : [���] �����Ĺ�')
            return

        if line == ob['�̸�']:
            ob.sendLine('�� �ڱ� �ڽ��Դϴ�.')
            return
        found = False
        for obj in ob.channel.players:
            if obj['�̸�'] == line:
                found = True
                break
        if found == False:
            obj = Player()
            obj.load(line)
            if obj == None:
                ob.sendLine('�� �׷� �������� �ƾ� �������� �ʽ��ϴ�.')
                return
        
        if obj['�Ҽ�'] != ob['�Ҽ�']:
            ob.sendLine('�� ����� �Ҽ��� �ƴմϴ�.')
            return

        g = GUILD[ob['�Ҽ�']]
        g['%s����Ʈ' % obj['����']].remove(obj['�̸�'])
        obj.attr.__delitem__('�Ҽ�')
        obj.attr.__delitem__('����')
        if obj['���ĺ�ȣ'] != '':
            obj.attr.__delitem__('���ĺ�ȣ')
        obj.save(False)
        g['���Ŀ���'] -= 1
        GUILD.save()

        msg = '%s %s ���Ŀ��� �Ĺ���Ŵ�� �����մϴ�.' % (ob.han_iga(), obj.han_obj())
        obj.sendLine('\r\n����� �Ĺ��Ǿ����ϴ�.')
        obj.lpPrompt()
        ob.sendGroup(msg, prompt = True)
        
