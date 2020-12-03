# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if len(line) == 0:
            ob.sendLine('����: [����� �̸�] ����ڸ�����')
            return

        mob = ob.env.findObjName(line)
        if mob == None or is_player(mob) == False:
            ob.sendLine('�׷� ���� �����!')
            return
        ob.env.objs.remove(mob)
        ob.channel.players.remove(mob)
        del mob
        ob.sendLine('����ڸ��� ���ŵǾ����ϴ�.')
