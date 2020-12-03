# -*- coding: euc-kr -*-
from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
            
        if line == '':
            ob.sendLine('���̸� ���̸� ����')
            return
        words = line.split()

        if len(words) < 2 :
            ob.sendLine('���̸� ���̸� ����')
            return

        try:
            zone = Room.Zones[words[1]]
        except KeyError:
            ob.sendLine('�׷� ���� �����!')
            return
        for room in zone:
            r = getRoom(words[1] + ':' + room)
            
            for obj in r.objs:
                if is_mob(obj):
                    if obj['�̸�'] == words[0]:
                        ob.sendLine(room)
                        return 
        ob.sendLine('��ã����')
    
    
    

