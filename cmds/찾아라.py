# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        from objs.room import Room, getRoom
        for zoneName in Room.Zones:
            zone = Room.Zones[zoneName]
            for roomName in zone:
                room = zone[roomName]
                for obj in room.objs:
                    if obj['�̸�'] == line:
                        ob.sendLine(room['�̸�'])


