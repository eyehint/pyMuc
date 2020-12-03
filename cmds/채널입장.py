from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob in ob.adultCH:
            ob.sendLine('☞ 이미 입장하셨습니다.')
            return
        ob.adultCH.append(ob)
        ob.sendLine('☞ 채널에 입장합니다.')
        buf = '\r\n[1;31m①⑨[0;37m ' + ob.getNameA() + '님이 입장하셨습니다.'
        for ply in ob.adultCH:
            if ob != ply:
                ply.sendLine(buf)
                ply.lpPrompt()
