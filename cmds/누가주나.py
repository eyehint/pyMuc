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
            ob.sendLine('�� ��� ���: [�������ε���] �����ֳ�')
            return
        c = 0
        
        t = getInt(line)

        for zoneName in Mob.Mobs:
            zone = Mob.Mobs[zoneName]
            for mobName in zone:
                mob = zone[mobName]
                s = mob['������'] 
                if s != '':
                    s = s.splitlines()
                    for l in s:
                        if l.split(' ')[0] == line.strip() :
                            ob.sendLine(mob['�̸�'] + ' : ' + mob.index)
                s = mob['��������'] 
                if s != '':
                    s = s.splitlines()
                    for l in s:
                        if l.split(' ')[0] == line.strip() :
                            ob.sendLine(mob['�̸�'] + ' : ' + mob.index)

