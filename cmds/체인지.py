# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            ob.sendLine('�� ����: [���] ü����')
            return
        ply = ob.env.findObjName(line)
        if ply == None or is_player(ply) == False:
            ob.sendLine('���⿡ ��������^^')
            return
            
        c = ply.channel
        p = ply.channel.player
        
        ply.channel = ob.channel
        ply.channel.player = ob.channel.player
        
        ob.channel = c
        ob.channel.player = p
        
        ply.INTERACTIVE = 1
        ob.INTERACTIVE = 1
        
        ply.input_to(ob.parse_command)
        ob.input_to(ply.parse_command)
        
        ob.sendLine('\r\n%s%s ���� ��ȯ�մϴ�.' % (ply['�̸�'], han_wa(ply['�̸�'])))
        ply.sendLine('\r\n%s%s ���� ��ȯ�մϴ�.' % (ob['�̸�'], han_wa(ob['�̸�'])))
