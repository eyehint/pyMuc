from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('☞ 사용법: [금액] 수령')
            return
        mob = ob.env.findObjName('표두')
        if mob == None:
            ob.sendLine('☞ 이곳에 표국무사가 없네요.')
            return
        m = getInt(line)
        if m <= 0:
            ob.sendLine('☞ 은전 1개 이상 입력 하셔야 해요.')
            return
        if ob['레벨'] > 500:
            ob.sendLine('☞ 충분한 능력이 있어 보이는데요???')
            return
        if m > 10000000:
            ob.sendLine('☞ 너무 욕심이 크군요???')
            return
        if m > mob['은전']:
            ob.sendLine('☞ 기부금이 모잘라요^^;')
            return
        if getInt(ob['수령액']) >= 1000000000:
            ob.sendLine('☞ 더이상 수령은 곤란해요^^;')
            return
        if getInt(ob['수령액']) + m >= 1000000000:
            ob.sendLine('☞ 한도 초과에요!!!')
            return
        if getInt(ob['마지막수령']) + 86400 > time.time():
            ob.sendLine('☞ 또 오셨어요???')
            return

        ob['마지막수령'] = time.time()
        ob['은전'] += m
        ob['수령액'] = getInt(ob['수령액']) + m
        mob['은전'] -= m
        msg = '당신이 은전 %d개를 표국무사에게 수령합니다.\r\n' % m
        msg += '현재까지 수령한 기부금 총액은 은전 [1m%d[0;37m개 입니다.' %(ob['수령액'])
        ob.sendLine(msg)

        msg = '[몹정보]\n\n'
        l = list(mob.attr.keys())
        l.sort()
        for at in l:
            msg += '#%s\n' % at
            for m in str(mob.attr[at]):
                msg += ':%s\n' % m
            msg += '\n'

        try:
            f = open(mob.path, 'w')
        except:
            return False
        f.write(msg)
        f.close()
