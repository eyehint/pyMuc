# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if len(line) == 0:
            ob.sendLine('����: [�� �̸�] ������')
            return

        mob = ob.env.findObjName(line)
        if mob == None or is_mob(mob) == False:
            ob.sendLine('�׷� ���� �����!')
            return
        ob.env.objs.remove(mob)
        del mob
        ob.sendLine('���� ���ŵǾ����ϴ�.')
