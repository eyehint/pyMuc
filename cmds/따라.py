# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('☞ 사용법: [대상] 동행')
            return
        if line == '나':
            ob.delFollow()
            ob.sendLine('당신은 홀로 강호를 주유하기 시작합니다.')
            return
        target = ob.env.findObjName(line)
        if target == None or is_player(target) == False:
            ob.sendLine('☞ 그런 대상이 없어요. ^^')
            return
        if target.checkConfig('동행거부'):
            ob.sendLine('%s 동행거부중 입니다.' % target.han_iga())
            return
        ob.delFollow()
        ob.addFollow(target)

