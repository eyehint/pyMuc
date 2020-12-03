# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        from objs.rank import Rank, RANK
        if line == '':
            RANK.attr = {}
            RANK.save()
            ob.sendLine('* ��ü�� �ʱ�ȭ �Ǿ����ϴ�.')
            return
        
        if line not in RANK.attr:
            ob.sendLine('�� �׷� ������ �����ϴ�.')
            return
        RANK.attr[line] = []
        RANK.save()
        ob.sendLine('* �ʱ�ȭ �Ǿ����ϴ�.')
