# -*- coding: euc-kr -*-

from objs.cmd import Command
from include.ansi import *

class CmdObj(Command):

    def cmd(self, ob, line):
        ob['部府富'] = ''
        ob.sendLine('⒀ 部府富阑 力芭 窍看嚼聪促.')
