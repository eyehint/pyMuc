# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        words = line.split()
        if line == '' or len(words) < 2:
            ob.sendLine('�� ����: [���] [Ű] ������')
            return
        words = line.split(None, 1)
        if words[0] == '��':
            target = ob.env
        else:
            target = ob.env.findObjName(words[0])
        if target == None:
            ob.sendLine('�� �׷� ����� �����!')
            return
        try:
            target.attr.__delitem__(words[1])
        except:
            ob.sendLine('�� �ش� Ű�� �����ϴ�.')
            return
        ob.sendLine('�� ���� �����Ǿ����ϴ�.')
