# -*- coding: euc-kr -*-

from objs.cmd import Command
from include.ansi import *

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            ob.sendLine('�� ��� ���: [���] ��')
            return
        for ply in ob.channel.players:
            if ply['�̸�'] == line:
                if ob.env == ply.env:
                    ob.sendLine('�� ���� �ڸ�����.')
                    return
                if ob.enterRoom(ply.env, '��ȯ', '��ȯ') == False:
                    ob.sendLine('�� �����̵��� �����Ͽ����ϴ�.')
                ob.clearTarget()
                return
        ob.sendLine('�� Ȱ������ �׷� �������� �����. ^^')
        return
        
        

