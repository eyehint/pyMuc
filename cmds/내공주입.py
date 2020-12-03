# -*- coding: euc-kr -*-

from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):

    def cmd(self, ob, line):
        c = 0
        tmp = ''
        n, guard = self.getGuardNum(ob)
        if n == 0:
            ob.sendLine('☞ 호위를 거느리지 않고 있습니다.')
            return
        for obj in guard:
            maxhp = getItem(obj.index)['체력']
            if obj.hp >= maxhp:
                continue
            mp = ob['힘'] * obj['내공감소'] / 100
            if ob['내공'] - mp < 0:
                if c == 0:
                    ob.sendLine('☞ 내가진기를 주입할 내공이 부족합니다.')
                    return
                break
            ob['내공'] -= mp
            c += 1
            hp = maxhp * obj['체력증가'] / 100
            obj.hp += hp
            if obj.hp >= maxhp:
                obj.hp = maxhp

            tmp += '당신이 %s에게 내가진기를 주입하여 체력을 회복 시킵니다. ([1;36m+%d[0;37m)\r\n' % (obj['이름'], hp)
        
        if c == 0:
            ob.sendLine('☞ 회복할 호위가 없습니다.')
            return

        ob.sendLine(tmp)
        ob.sendLine('당신이 소모된 진기를 다스립니다. ([1;32m-%d[0;37m)' % (mp * c))
        
    def getGuardNum(self, ob):
        n = 0
        guard = []
        for obj in ob.objs:
            if obj['종류'] == '호위':
                n += 1
                guard.append(obj)
        return n, guard


