# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
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
	for s in target.skills:
            if s.name == words[1]:
                ob.sendLine('�� ������ ���ŵǾ����ϴ�.')
                target.skills.remove(s)
                break
