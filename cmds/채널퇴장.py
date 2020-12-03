# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob not in ob.adultCH:
            ob.sendLine('☞ 먼저 채널에 입장하세요.')
            return
        ob.adultCH.remove(ob)
	buf = '\r\n[1;31m①⑨[0;37m ' + ob.getNameA() + '님이 퇴장하셨습니다.'
	for ply in ob.adultCH:
	    if ob != ply:
		ply.sendLine(buf)
		ply.lpPrompt()
        ob.sendLine('☞ 채널에서 퇴장합니다.')
