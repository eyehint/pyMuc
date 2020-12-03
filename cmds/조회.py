# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        mob = ob.env.findObjName('표두')
        if mob == None:
            ob.sendLine('☞ 이곳에 표국무사가 없네요.')
            return
        p = ob['보험료']
        c1 = ob['레벨'] * MAIN_CONFIG['보험료단가']
        c2 = c1 * MAIN_CONFIG['보험출장률'] / 100
        msg = '당신의 보험료 총액은 은전 [1m%d[0;37m개이며\r\n보험 혜택은 [1m%d[0m[40m[37m번 받으실 수 있습니다.\r\n' %(p, ob.getInsureCount())
        msg += '보험혜택이 적용되는 금액은 은전 [1m%d[0;37m개 이상이며\r\n' % c1
        msg += '한번의 출장 처리시엔 은전 [1m%d[0;37m개가 소요됩니다.' % c2
        ob.sendLine(msg)
            

