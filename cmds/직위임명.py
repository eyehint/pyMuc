# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob['����'] != '����':
            ob.sendLine('�� ������ ���ָ��� �� �� �ֽ��ϴ�.')
            return
        words = line.split()
        l = ['����', '�ι���', '���', '������']
        if line == '' or len(words) < 2 or words[1] not in l:
            ob.sendLine('�� ���� : [���] [����|�ι���|���|������] �����Ӹ�')
            return
        obj = ob.env.findObjName(words[0])
        if obj == None:
            ob.sendLine('�� �̰��� �׷� �������� �����ϴ�.')
            return
        if obj == ob:
            ob.sendLine('�� �ڱ� �ڽ��Դϴ�.')
            return
        if obj['�Ҽ�'] != ob['�Ҽ�']:
            ob.sendLine('�� ����� �Ҽ��� �ƴմϴ�.')
            return
        if obj['����'] == words[1]:
            ob.sendLine('�� ���� �����Դϴ�.')
            return
        g = GUILD[ob['�Ҽ�']]
        c = MAIN_CONFIG['���� %s �ο�' % words[1]]
        if '%s����Ʈ' % words[1] in g:
            l1 = g['%s����Ʈ' % words[1]]
        else:
            l1 = []
            g['%s����Ʈ' % words[1]] = l1
            
        if c <= len(l1):
            ob.sendLine('�� ���� ������ �ο��� �ʹ� �����ϴ�.')
            return
        g['%s����Ʈ' % obj['����']].remove(obj['�̸�'])
        g['%s����Ʈ' % words[1]].append(obj['�̸�'])
        obj['����'] = words[1]
        GUILD.save()

        msg = '%s %s [1m%s[0m%s ������ �Ӹ��մϴ�.' % (ob.han_iga(), obj.han_obj(), words[1], han_uro(words[1]))
        ob.sendGroup(msg, prompt = True)
        
