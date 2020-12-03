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
            ob.sendLine('�� ��� ���: [���̸�]|[������] ��ã��\r\n ex) ���� ��ã�� or 6 ��ã��')
            return
        c = 0
        
        t = getInt(line)

        for zoneName in Mob.Mobs:
            zone = Mob.Mobs[zoneName]
            for mobName in zone:
                mob = zone[mobName]
                if t != 0:
                    if mob['������'] == t:
                        c += 1
                        ob.sendLine('%s(%s) : %s'% (mob.getNameA(), mob.index, mob['��ġ']))
                else:
                    if mob['�̸�'].find(line) != -1:
                        c += 1
                        ob.sendLine('%s(%s) : %s'% (mob.getNameA(), mob.index, mob['��ġ']))
        if c == 0:
            ob.sendLine('�� ã���ô� ���� �����ϴ�.')
        

