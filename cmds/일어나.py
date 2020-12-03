# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob.act == ACT_REST:
            ob.sendLine('����� ��������� ��ġ�� ���� �Ͼ�ϴ�.')
            ob.sendRoom('%s ��������� ��ġ�� ���� �Ͼ�ϴ�.' % ob.han_iga())
            ob.act = ACT_STAND
        elif ob.act == ACT_STAND:
            ob.sendLine('�� �̹� ���ִ� �����Դϴ�. ^^')
        else:
            ob.sendLine('�� ����������� ���°� �ƴմϴ�.')
