# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('☞ 사용법: [대상] 비교')
            return
        obj = ob.env.findObjName(line)
        if is_mob(obj) == False and is_player(obj) == False:
            ob.sendLine('자신의 상태를 통탄해 합니다. @_@')
            return
        if obj == None or obj['몹종류'] == 7:
            ob.sendLine('☞ 그런 비교대상이 없어요. ^^')
            return
        if ob == obj:
            ob.sendLine('자신의 상태를 통탄해 합니다. @_@')
            return
        if ob.checkConfig('비교거부') or (is_player(obj) and obj.checkConfig('비교거부')):
            ob.sendLine('☞ 진정한 승부란 비무를 통해서 알 수 있는 것 이지')
            return
        
        mT, c1, c2 = ob.getAttackPoint(obj)
        uT, c1, c2 = obj.getAttackPoint(ob)
        if is_player(obj):
            mH = obj['최고체력'] / mT
        else:
            mH = obj['체력'] / mT
        uH = ob['최고체력'] / uT
        ob.sendLine('━━━━━━━━━━━━━━━')
        ob.sendLine('▶ [1m%s[0;37m%s의 상대비교' % ( obj['이름'] , han_wa(obj['이름']) ))
        ob.sendLine('───────────────')
        ob.sendLine('☞ 당신의 승률 오차ː%d' % uH)
        ob.sendLine('☞ 상대의 승률 오차ː%d' % mH)
        ob.sendLine('☞ 승  률 오차 결과ː%d' % (uH-mH))
        ob.sendLine('━━━━━━━━━━━━━━━')

