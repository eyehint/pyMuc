# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        ONEITEM.clear()
        ob.sendLine('* �⿬������ ����� �ʱ�ȭ�Ǿ����ϴ�.')
