# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        ob['ü��'] = ob.getMaxHp()
        ob['����'] = ob.getMaxMp()
        ob.sendLine('* ȸ���Ǿ����ϴ�.')
