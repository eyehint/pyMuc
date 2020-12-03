# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cool(self, ob):
        ob['_runaway'] = 0

    def cmd(self, ob, line):
        if ob.act != ACT_FIGHT:
            ob.sendLine('�� �������� �ƹ����� �������°��� �ƴ϶��')
            return
        if ob.env.checkAttr('��������'):
            ob.sendLine('�� ���� ������ �������. \'����~~ T_T\'')
            return
        if ob['_runaway'] == None:
            ob['_runaway'] = 0
        if ob['_runaway'] == 1:
            ob.sendLine('�� ���� ������ �������. \'����~~ T_T\'')
            return
        ob['_runaway'] = 1
        from twisted.internet import reactor
        reactor.callLater(1, self.cool, ob)
        bonus = 0

        try:
            if ob.cooltime['���Ĺ̺�'] == 1:
                bonus = 40
        except:
            pass

        mob = ob.target[0]
        c1 = mob['����'] * (mob.getDex() + 1) - ob['����'] * (ob.getDex() + 1)
        if c1 < 1:
            c1 = 1
        c1 = 100 - c1
        if c1 < 10:
            c1 = 10
        c1 += bonus
        c2 = randint(0, 100)
        if c2 > c1:
            ob.sendLine('�� ���� ������ �������. \'����~~ T_T\'')
            return
        
        room, dir = ob.env.getRandomExit()
        if room == None or room == ob.env:
            ob.sendLine('�� ���� ������ �������. \'����~~ T_T\'')
            return
            
        if getInt(room['��������']) > ob['����']:
            ob.sendLine('�� ���� ������ �������. \'����~~ T_T\'')
            return
        if room.checkLimitNum():
            ob.sendLine('�� ���� ������ �������. \'����~~ T_T\'')
            return
        if room.checkAttr('�������Ա���') and ob['����'] == '����':
            ob.sendLine('�� ���� ������ �������. \'����~~ T_T\'')
            return
        if room.checkAttr('�������Ա���') and ob['����'] == '����':
            ob.sendLine('�� ���� ������ �������. \'����~~ T_T\'')
            return
        
        if ob.enterRoom(room, dir, '����') == False:
            ob.sendLine('�� ���� ������ �������. \'����~~ T_T\'')
            return

