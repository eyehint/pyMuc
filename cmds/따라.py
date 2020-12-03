# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('�� ����: [���] ����')
            return
        if line == '��':
            ob.delFollow()
            ob.sendLine('����� Ȧ�� ��ȣ�� �����ϱ� �����մϴ�.')
            return
        target = ob.env.findObjName(line)
        if target == None or is_player(target) == False:
            ob.sendLine('�� �׷� ����� �����. ^^')
            return
        if target.checkConfig('����ź�'):
            ob.sendLine('%s ����ź��� �Դϴ�.' % target.han_iga())
            return
        ob.delFollow()
        ob.addFollow(target)

