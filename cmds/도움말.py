from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        from objs.help import HELP
        if line == '':
            ob.sendLine(HELP['도움말'])
        else:
            help = HELP[line]
            if help == '':
                ob.sendLine('☞ 해당 도움말이 없어요. ^^')
            else:
                ob.sendLine(help)

