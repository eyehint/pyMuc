from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):

    def cmd(self, ob, line):

        if ob.act != ACT_FIGHT or len(ob.target) == 0:
            ob.sendLine('☞ 지금은 [1m[31m살겁[0m[37m[40m을 일으키기에 부적합한 상황 이라네')
            return
        if ob['분노'] < 100:
            ob.sendLine('☞ 당신은 아직 [1;40;31m분노[0;40;37m를 표출할 수 없습니다.')
            return
        n, guard = self.getGuardNum(ob)
        if n < 1:
            ob.sendLine('☞ 당신이 [1;40;31m분노[0;40;37m를 스스로 다스립니다.')
            ob['분노'] -= 100
            return
        mob = None
        if line != '':
            mob = ob.env.findObjName(line)
            if mob == None:
                ob.sendLine('☞ 공격할 그런 대상이 없습니다.')
                return
            if mob not in ob.target:
                ob.sendLine('☞ 현재의 비무에 신경을 집중하세요. @_@')
                return
        ob['분노'] -= 100
        if mob == None:
            for mob in ob.target:
                if mob.env != ob.env:
                    continue
                break
        if mob == None:
            ob.sendLine('☞ 공격할 그런 대상이 없습니다.')
            return
        msg = ''
        msg1 = guard[0]['사용스크립']
        msg2 = guard[0]['공격스크립']
        msg3 = guard[0]['실패스크립']
        buf1, buf2, buf3 = ob.makeFightScript(msg1, mob, guard[0])
        ob.sendLine(buf1 + '\r\n')
        msg += buf3 + '\r\n'
        for g in guard:
            c = 100 + g['명중력'] - ( mob['레벨'] - ob['레벨'] + 90 ) / 3
            if g.hp < 1 or randint(0, 99) > c:
                buf1, buf2, buf3 = ob.makeFightScript(msg3, mob, g)
                ob.sendLine(buf1)
                msg += buf3 + '\r\n'
            else:
                if randint(0, 1) == 0:
                    dmg = (ob['힘'] * g['공격력']) / 100 + randint(0, 9)
                else:
                    dmg = (ob['힘'] * g['공격력']) / 100 - randint(0, 9)
                    
                if dmg < 1:
                    dmg = 1
                g.hp -= (dmg * g['체력감소']) / 100
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
            if obj['종류'] == '호위':
                n += 1
                guard.append(obj)
        return n, guard
