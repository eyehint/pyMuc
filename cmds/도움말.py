# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        from objs.help import Help, HELP
        if line == '':
            ob.sendLine(HELP['����'])
        else:
            help = HELP[line]
            if help == '':
                ob.sendLine('�� �ش� ������ �����. ^^')
            else:
                ob.sendLine(help)

