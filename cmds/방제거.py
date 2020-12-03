# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            ob.sendLine('�� ����: [���ȣ] ������')
            return
        
        ret = self.delRoom(line)
        if ret == None:
            ob.sendLine('���������ʴ� ���Դϴ�.')
            return
        del ret
        ob.sendLine('���� ���ŵǾ����ϴ�.')
        
    def delRoom(self, path):
    
        i = path.find(':')
        if i == -1:
            return None
    
        zoneName = path[:i]
        roomName = path[i+1:]
    
        try:
            zone = Room.Zones[zoneName]
        except KeyError:
            return None
            
        try:
            room = zone[roomName]
        except KeyError:
            return None
        
        zone[roomName] = None
        zone.__delitem__(roomName)
        return room
