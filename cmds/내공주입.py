# -*- coding: euc-kr -*-

from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):

    def cmd(self, ob, line):
        c = 0
        tmp = ''
        n, guard = self.getGuardNum(ob)
        if n == 0:
            ob.sendLine('�� ȣ���� �Ŵ����� �ʰ� �ֽ��ϴ�.')
            return
        for obj in guard:
            maxhp = getItem(obj.index)['ü��']
            if obj.hp >= maxhp:
                continue
            mp = ob['��'] * obj['��������'] / 100
            if ob['����'] - mp < 0:
                if c == 0:
                    ob.sendLine('�� �������⸦ ������ ������ �����մϴ�.')
                    return
                break
            ob['����'] -= mp
            c += 1
            hp = maxhp * obj['ü������'] / 100
            obj.hp += hp
            if obj.hp >= maxhp:
                obj.hp = maxhp

            tmp += '����� %s���� �������⸦ �����Ͽ� ü���� ȸ�� ��ŵ�ϴ�. ([1;36m+%d[0;37m)\r\n' % (obj['�̸�'], hp)
        
        if c == 0:
            ob.sendLine('�� ȸ���� ȣ���� �����ϴ�.')
            return

        ob.sendLine(tmp)
        ob.sendLine('����� �Ҹ�� ���⸦ �ٽ����ϴ�. ([1;32m-%d[0;37m)' % (mp * c))
        
    def getGuardNum(self, ob):
        n = 0
        guard = []
        for obj in ob.objs:
            if obj['����'] == 'ȣ��':
                n += 1
                guard.append(obj)
        return n, guard


