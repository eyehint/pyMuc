# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
            
        from client import Client
        for ply in Client.players:
            if ply.state != ACTIVE:
                continue
            if ply.env == ob.env:
                ob.sendLine('�� ���� ���̿���. ^^')
                continue
            if ply.enterRoom(ob.env, '��ȯ', '��ȯ') == False:
                ob.sendLine('�� �����̵��� �����Ͽ����ϴ�.')
            ply.clearTarget()
            ply.lpPrompt()
