# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('�� ����: [����] ǥ��(\')')
            return
        if ob.env.noComm():
            ob.sendLine('�� ������������ ��� ��ŵ� �Ұ����մϴ�.')
            return
        ob.sendLine('����� ' + line)
        ob.sendRoom(ob['�̸�'] + han_iga(ob['�̸�']) + ' ' + line)

