# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        mob = ob.env.findMerchant()
        if mob == None:
            ob.sendLine('�� ǰ���� ������ ������ �����. ^^')
            return
        if mob['�����ǸŽ�ũ��'] == '':
            ob.sendLine('�� ǰ���� ������ ������ �����. ^^')
            return
        ob.sendLine(mob['�����ǸŽ�ũ��'])


