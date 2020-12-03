# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('☞ 사용법: [금액] 기부')
            return
        mob = ob.env.findObjName('표두')
        if mob == None:
            ob.sendLine('☞ 이곳에 표국무사가 없네요.')
            return
        m = getInt(line)
        if m <= 0:
            ob.sendLine('☞ 은전 1개 이상 입금 하셔야 해요.')
            return
        if m > ob['은전']:
            m = ob['은전']
        ob['은전'] -= m
        mob['은전'] += m
        msg = '당신이 은전 %d개를 표국무사에게 기탁합니다.\r\n' % m
        msg += '현재까지 모여진 기부금 총액은 은전 [1m%d[0;37m개 입니다.' %(mob['은전'])
        ob.sendLine(msg)

        msg = '[몹정보]\n\n'
        l = mob.attr.keys()
        l.sort()
        for at in l:
            msg += '#%s\n' % at
            for m in str(mob.attr[at]).splitlines():
                msg += ':%s\n' % m
            msg += '\n'

        try:
            f = open(mob.path, 'w')
        except:
            return False
        f.write(msg)
        f.close()
