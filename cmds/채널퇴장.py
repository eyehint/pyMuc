# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob not in ob.adultCH:
            ob.sendLine('�� ���� ä�ο� �����ϼ���.')
            return
        ob.adultCH.remove(ob)
	buf = '\r\n[1;31m���[0;37m ' + ob.getNameA() + '���� �����ϼ̽��ϴ�.'
	for ply in ob.adultCH:
	    if ob != ply:
		ply.sendLine(buf)
		ply.lpPrompt()
        ob.sendLine('�� ä�ο��� �����մϴ�.')
