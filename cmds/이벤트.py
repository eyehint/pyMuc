# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            ob.sendLine('�� ����: [���] �̺�Ʈ')
            return
            
        target = ob.env.findObjName(line)
        if target == None:
            ob.sendLine('�� �׷� ����� �����!')
            return
        for l in target['�̺�Ʈ��������Ʈ'].splitlines():
            ob.sendLine(l)

