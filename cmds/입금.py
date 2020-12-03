from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('☞ 사용법: [금액] 입금')
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
        ob['보험료'] += m
        msg = '당신이 은전 %d개를 표국무사에게 입금합니다.\r\n\r\n' % m
        msg += '당신의 보험료 총액은 은전 [1m%d[0;37m개이며\r\n보험 혜택은 [1m%d[0m[40m[37m번 받으실 수 있습니다.' %(ob['보험료'], ob.getInsureCount())

        ob.sendLine(msg)
            

