# -*- coding: euc-kr -*-

from objs.cmd import Command
from include.ansi import *

class CmdObj(Command):

    def cmd(self, ob, line):
        ob['꼬리말'] = ''
        ob.sendLine('☞ 꼬리말을 제거 하였습니다.')
