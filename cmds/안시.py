from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        hp = ob.get('체력')
        maxhp = ob.get('최고체력')

        hcnt = 10*hp//maxhp
        msg = '[32m'
        for i in range(hcnt):
            msg += '━'
        msg += '[37m'
        for i in range(10-hcnt):
            msg += '━'
        ob.sendLine(msg)
