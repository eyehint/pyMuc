# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            ob.sendLine('�� ����: [�⿬�̸�] �⿬����')
            return
            
        msg = ''
        if line not in ONEITEM.index:
            ob.sendLine('�� �׷� �������� �����ϴ�.!')
            return
        index = ONEITEM.index[line]
        ONEITEM.attr.__delitem__(index)
        ONEITEM.save()
        ob.sendLine('�� �⿬�� �����Ǿ����ϴ�.')

