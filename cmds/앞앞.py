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
            ob.sendLine('�� ��� ���: [���] ��')
            return
        for ply in ob.channel.players:
            if ply['�̸�'] == line:
                if ob.env == ply.env:
                    ob.sendLine('�� ���� �ڸ�����.')
                    return
                ob.clearTarget()
                ob.env.remove(ob)
                ob.env = ply.env
                ob.env.insert(ob)
                
                #if ob.enterRoom(ply.env, '��ȯ', '��ȯ') == False:
                #    ob.sendLine('�� �����̵��� �����Ͽ����ϴ�.')
                
                return
        ob.sendLine('�� Ȱ������ �׷� �������� �����. ^^')
        return
        
        

