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
            ob.sendLine('�� ����: [���] [�����̸�] ��������')
            return
        words = line.split(None, 1)
        target = ob.env.findObjName(words[0])
        if target == None:
            ob.sendLine('�� �׷� ����� �����!')
            return
        target.skillList.append(words[1])
        ob.sendLine('�� ������ �����Ǿ����ϴ�.')
