# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob['����'] != '����':
            ob.sendLine('�� ������ ���ָ��� �� �� �ֽ��ϴ�.')
            return
        words = line.split()
        l = ['����', '�ι���', '���', '������']
        if line == '' or len(words) < 2 or words[0] not in l:
            ob.sendLine('�� ���� : [����|�ι���|���|������] [�̸�] ��Ī����')
            return

        GUILD[ob['�Ҽ�']]['%s��Ī' % words[0]] = words[1]
        GUILD.save()
        print GUILD[ob['�Ҽ�']]['%s��Ī' % words[0]]
        msg = '%s %s�� ��Ī�� [1m%s[0;37m%s �����Ͽ� �����մϴ�.' % (ob.han_iga(), words[0], words[1], han_uro(words[1]))
        ob.sendGroup(msg, prompt = True)
        
