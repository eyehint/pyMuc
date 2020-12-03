# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob in ob.adultCH:
            ob.sendLine('�� �̹� �����ϼ̽��ϴ�.')
            return
        ob.adultCH.append(ob)
        ob.sendLine('�� ä�ο� �����մϴ�.')
        buf = '\r\n[1;31m���[0;37m ' + ob.getNameA() + '���� �����ϼ̽��ϴ�.'
        for ply in ob.adultCH:
            if ob != ply:
                ply.sendLine(buf)
                ply.lpPrompt()
