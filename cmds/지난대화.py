# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        for msg in ob.talkHistory:
            ob.sendLine(msg)

