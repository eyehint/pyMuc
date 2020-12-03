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
        s = MUGONG[words[1]]
        if s == '':
            for sName in MUGONG.attr:
                if sName.find(words[1]) == 0:
                    s = MUGONG[sName]
                    break
        if s == '':
            ob.sendLine('�� �׷� ������ ������ ���� �����ϴ�.')
            return
        if s.name in target.skillList:
            ob.sendLine('�� �̹� ������ �����̴°ɿ�')
            return
        target.skillList.append(s.name)
        ob.sendLine('�� ������ �����Ǿ����ϴ�.')
