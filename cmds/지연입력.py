# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('�� ����: [�Է±�] �����Է�')
            return
        from twisted.internet import reactor
        reactor.callLater(1, ob.do_command, line)
        

