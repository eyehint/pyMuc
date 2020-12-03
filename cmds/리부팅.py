# -*- coding: euc-kr -*-

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        from twisted.internet import reactor
        self.updateZones()
        reactor.stop()

    def updateZones(self):
        for zoneName in Room.Zones:
            print "update zones..." + zoneName
            zone = Room.Zones[zoneName]
            for roomName in zone:
                room = zone[roomName]
                room.update()
