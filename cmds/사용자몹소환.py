# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            ob.sendLine('�� ����: [���] ����ڸ���ȯ')
            return
        ply = Player()
        if ply.load(line) == False:
            ob.sendLine('���������ʴ� ������Դϴ�.')
            return
        ply.state = ACTIVE
        ob.env.insert(ply)
        ob.channel.players.append(ply)
        ob.sendLine('%s ��ȯ�Ͽ����ϴ�.' % ply.han_obj())
