# -*- coding: euc-kr -*-
from objs.cmd import Command

class CmdObj(Command):

    def down(self, ob):
        ob.set('cooltime', 0)
        ob.sendLine('����� �����ϰ� �����մϴ�. ^^v')

    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
            
        if ob.get('cooltime') == None:
            ob.set('cooltime', 0)
        if ob.get('cooltime') == 1:
            ob.sendLine('����� ���⿣ �ʹ��� �ٺ���~')
            return
        from twisted.internet import reactor
        ob.sendLine('����� �ο�~~ ���� �����ϴ�')
        ob.set('cooltime', 1)
        reactor.callLater(2, self.down, ob)
