# -*- coding: euc-kr -*-

from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):

    def cmd(self, ob, line):
    
        if len(line) == 0:
            ob.sendLine('☞ 사용법: [대상] 공격')
            return
        
        if ob.env.checkAttr('전투금지'):
            ob.sendLine('☞ 이곳에선 모든 전투가 금지되어 있어요. ^^')
            return
            
        if line.find('시체') != -1:
            ob.sendLine('☞ 강호에는 공격할 수 있는것과 없는것이 있지!')
            return
            
        mob = ob.env.findObjName(line)

        if mob == None:
            ob.sendLine('☞ 강호에는 공격할 수 있는것과 없는것이 있지!')
            return

        if is_item(mob) or is_box(mob) or is_player(mob):
            ob.sendLine('☞ 강호에는 공격할 수 있는것과 없는것이 있지!')
            return
        if is_player(mob) and ob.env.checkAttr('사용자전투금지'):
            ob.sendLine('☞ 지금은 [1m[31m살겁[0m[37m[40m을 일으키기에 부적합한 상황 이라네')
            return
            
        if is_player(mob) == False and mob['몹종류'] != 1:
            ob.sendLine('☞ 강호에는 공격할 수 있는것과 없는것이 있지!')
            return
        if mob.act > ACT_FIGHT:
            ob.sendLine('☞ 강호에는 공격할 수 있는것과 없는것이 있지!')
            return
        
        #if mob['이름'] != '똥파리' and len(mob.target) != 0 and ob not in mob.target:
        #    ob.sendLine('☞ 그런 상대가 없습니다.')
        #    return

        if mob in ob.target:
            ob.sendLine('☞ 이미 공격중이에요. ^_^')
            return
        
        if len(ob.target) != 0:
            ob.sendLine('☞ 현재의 비무에 신경을 집중하세요. @_@')
            return
        ob.setFight(mob)
        if is_player(mob):
            mob.fightMode = True

        #ob.sendLine('당신은 ' + mob.get('이름') + han_obj(mob.get('이름')) + \
        #    ' 공격하기 시작합니다.')
