# -*- coding: euc-kr -*-

from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):

    def cmd(self, ob, line):

        if ob.act != ACT_FIGHT or len(ob.target) == 0:
            ob.sendLine('�� ������ [1m[31m���[0m[37m[40m�� ����Ű�⿡ �������� ��Ȳ �̶��')
            return
        if ob['�г�'] < 100:
            ob.sendLine('�� ����� ���� [1;40;31m�г�[0;40;37m�� ǥ���� �� �����ϴ�.')
            return
        n, guard = self.getGuardNum(ob)
        if n < 1:
            ob.sendLine('�� ����� [1;40;31m�г�[0;40;37m�� ������ �ٽ����ϴ�.')
            ob['�г�'] -= 100
            return
        mob = None
        if line != '':
            mob = ob.env.findObjName(line)
            if mob == None:
                ob.sendLine('�� ������ �׷� ����� �����ϴ�.')
                return
            if mob not in ob.target:
                ob.sendLine('�� ������ �񹫿� �Ű��� �����ϼ���. @_@')
                return
        ob['�г�'] -= 100
        if mob == None:
            for mob in ob.target:
                if mob.env != ob.env:
                    continue
                break
        if mob == None:
            ob.sendLine('�� ������ �׷� ����� �����ϴ�.')
            return
        msg = ''
        msg1 = guard[0]['��뽺ũ��']
        msg2 = guard[0]['���ݽ�ũ��']
        msg3 = guard[0]['���н�ũ��']
        buf1, buf2, buf3 = ob.makeFightScript(msg1, mob, guard[0])
        ob.sendLine(buf1 + '\r\n')
        msg += buf3 + '\r\n'
        for g in guard:
            c = 100 + g['���߷�'] - ( mob['����'] - ob['����'] + 90 ) / 3
            if g.hp < 1 or randint(0, 99) > c:
                buf1, buf2, buf3 = ob.makeFightScript(msg3, mob, g)
                ob.sendLine(buf1)
                msg += buf3 + '\r\n'
            else:
                if randint(0, 1) == 0:
                    dmg = (ob['��'] * g['���ݷ�']) / 100 + randint(0, 9)
                else:
                    dmg = (ob['��'] * g['���ݷ�']) / 100 - randint(0, 9)
                    
                if dmg < 1:
                    dmg = 1
                g.hp -= (dmg * g['ü�°���']) / 100
                if g.hp < 0:
                    g.hp = 0
                buf1, buf2, buf3 = ob.makeFightScript(msg2, mob, g)

                if mob.hp <= 1:
                    dmg = 0

                ob.sendLine(buf1 + ' [1;36m%d[0;37m' % dmg)
                msg += buf3 + '\r\n'
            
                mob.hp -= dmg
                if mob.hp < 0:
                    mob.hp = 1
                    break

    def getGuardNum(self, ob):
        n = 0
        guard = []
        for obj in ob.objs:
            if obj['����'] == 'ȣ��':
                n += 1
                guard.append(obj)
        return n, guard
