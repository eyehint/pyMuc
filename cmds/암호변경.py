# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        ob.write('������ȣ�� ')
        ob.INTERACTIVE = 0
        ob.input_to(ob.get_oldpass)

