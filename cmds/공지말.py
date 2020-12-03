# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('☞ 운영자 명령: [내용] 공지말')
            return
            
        buf = '───────────────────────────────────────\r\n'
        buf += '[7m☞ 공지 : %-68s[0m\r\n' % (line)
        buf += '───────────────────────────────────────'
        from client import Client
        for ply in Client.players:
            if ply.state != ACTIVE:
                continue
            if ply == ob:
                ply.sendLine(buf)
            else:
                ply.sendLine('\r\n' + buf)
                ply.lpPrompt()

