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

        for ply in ob.channel.players:
            if ply['�̸�'] == line:
#mob = ob.env.findObjName(line)
#        if mob == None or is_player(mob) == False:
#            ob.sendLine('�׷� ���� �����!')
#            return
		        ply.env.objs.remove(ply)
       			ob.channel.players.remove(ply)
		        del ply
        		ob.sendLine('����ڸ��� ���ŵǾ����ϴ�.')
