# -*- coding: euc-kr -*-

from objs.cmd import Command
from twisted.internet import reactor

class CmdObj(Command):

    def down(self, ob):
        ob.set('cooltime', 0)
        ob.sendLine('�����ٿ� ��û������ �ɸ��� ����...')
        reactor.callLater(3, self.down1, ob)

    def down1(self, ob):
        ob.set('cooltime', 0)
        ob.sendLine('����! �������� ��������.')

    def cmd(self, ob, line):
        ob.sendLine('���ùٴÿ� �̳��� ����� ���ô븦 �帮��ϴ�.')
        reactor.callLater(3, self.down, ob)
        return
