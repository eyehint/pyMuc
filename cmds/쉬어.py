# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob.env.checkAttr('������'):
            ob.sendLine('�� �̰����� ��������ϱ⿣ �������� �ʱ���.')
            return
        if ob.act == ACT_REST:
            ob.sendLine('�� ���� ���� �־��. ^^')
        elif ob.act == ACT_STAND:
            ob.sendLine('����� �ڼ��� ����� �ϸ� ������Ŀ� ���ϴ�.')
            ob.sendRoom('%s �ڼ��� ����� �ϸ� ������Ŀ� ���ϴ�.' % ob.han_iga())
            ob.act = ACT_REST
        else:
            ob.sendLine('�� ���� ���⿡�� ������ �ʳ׿�. ^^')
