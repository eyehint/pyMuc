# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if len(line) == 0:
            ob.sendLine('����: [�� �ε���] ������')
            return

        ret = self.delMob(line)
        if ret == None:
            ob.sendLine('���������ʴ� ���Դϴ�.')
            return
        del ret
        ob.sendLine('���� �����Ǿ����ϴ�.')
        
    def delMob(self, path):
        i = path.find(':')
        if i == -1:
            return None
    
        zoneName = path[:i]
        mobName = path[i+1:]
    
        try:
            zone = Mob.Mobs[zoneName]
        except KeyError:
            return None
            
        try:
            mob = zone[mobName]
        except KeyError:
            return None
        
        zone[mobName] = None
        zone.__delitem__(mobName)
        return mob
        
