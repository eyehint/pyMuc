# -*- coding: euc-kr -*-

from objs.cmd import Command
from include.ansi import *

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            ob.sendLine('�� ��� ���: [���] ��ȯ')
            return
        for ply in ob.channel.players:
            if ply['�̸�'] == line:
                if ply.env == ob.env:
                    ob.sendLine('�� ���� ���̿���. ^^')
                    return
                if ply.enterRoom(ob.env, '��ȯ', '��ȯ') == False:
                    ob.sendLine('�� �����̵��� �����Ͽ����ϴ�.')
                ply.clearTarget()
                ply.lpPrompt()
                return
        ob.sendLine('�� Ȱ������ �׷� �������� �����. ^^')
        return
        
        

