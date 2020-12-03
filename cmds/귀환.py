# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob.env.checkAttr('��ȯ����'):
            ob.sendLine('�� �̰����� ��ȯ�Ͻ� �� �����. ^^')
            return
        # check if player can't move
        if ob.isMovable() == False:
            ob.sendLine('�� ������ ��ȯ�� ��Ȳ�� �ƴϿ���. ^^')
            return

        ret = ob.get('��ȯ����')
        if ret == '':
            room = getRoom('���缺:42')
        else:
            room = getRoom(ret)
        if room == None:
            ob.sendLine('��ȯ������ �����ϴ�. �����ڿ��� �����ϼ���.')
            return
        if room == ob.env:
            ob.sendLine('�� ���� �ڸ�����. ^^')
            return
        ob.enterRoom(room, '��ȯ', '��ȯ')


