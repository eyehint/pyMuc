# -*- coding: euc-kr -*-

import sys, traceback
from lib.object import *
from lib.comm import broadcast

def parse_command(self, line, *args):
    if len(line) == 0:
        return
        
    from objs.player import Player
    if line[-1] in (' ', '.', '!', '?', ','):
        Player.cmdList['��'].cmd(self, line)
        return

    cmd = line.split(' ')[-1]
    param = line.rstrip(cmd)
    param = param.strip()

    s = self.get('���Ӹ�')
    if s != None and cmd in s:
        wlist = s[cmd].split(';')
        cmd = wlist[0]
        msg = ''
        for w in wlist[1:]:
            #if w in s:
            #    self.sendLine('��ø�� ���Ӹ��� ����� �� �����ϴ�.')
            #    return
            msg += w + '\r\n'
        self.channel.buffer = msg + self.channel.buffer

    from objs.alias import alias
    if cmd in alias:
        cmd = alias[cmd]
                
    if type(self.env.get('�ⱸ')) is dict and cmd in self.env.get('�ⱸ'):
        if self.is_attack():
            self.sendLine('���� �߿��� �̵� �� �� �����ϴ�.')
            return

        exit = self.env.get('�ⱸ')[cmd]
        if type(exit) is list:
            import random
            r = random.randint(0, len(exit)-1)
            exit = exit[r]
        room = get_room(exit)
      
        if room == None:
            self.sendLine('* �̵� ����!!!')
            return
        room.append(self, cmd)
        return
    elif cmd in ('��', '����'):
        if self.is_attack():
            self.sendLine('���� �߿��� ���� �� �� �����ϴ�.')
            return
        self.sendLine('������ �� ������~!!!')
        broadcast(self.get('�̸�') + '���� �����̽��ϴ�.', self)
        self.channel.transport.loseConnection()
        return
    elif cmd in Player.emotes:
        try:
            Player.emotes[cmd].cmd(self, param)
        except :
            traceback.print_exc(file=sys.stderr)
            print 'Error in %s' % cmd
        return
    elif cmd in Player.cmdList:
        try:
            Player.cmdList[cmd].cmd(self, param)
        except :
            traceback.print_exc(file=sys.stderr)
            print 'Error in %s' % cmd
        
        # ������� ����� ó���� �� ���� ��ũ
        for obj in self.env.objs:
            if is_mob(obj) and hasattr(obj, 'mob_hook'):
                obj.mob_hook(line)
        return


    # �� ������Ʈ�� �׼��� ó��
    if hasattr(self.env, 'actions'):
        if cmd in self.env.actions:
            self.env.actions[cmd](self, param)
            return

    # �뿡 �ִ� ������Ʈ���� �׼��� ó��
    for obj in self.env.objs:
        if hasattr(obj, 'actions'):
            if cmd in obj.actions:
                obj.actions[cmd](self, param)
                return
           
    self.sendLine('\r\n�� ���� ������ �𸣰ھ��. *^_^*')
    
def pressEnter(self, line, *args):
    self.INTERACTIVE = 1
    self.input_to(parse_command)
