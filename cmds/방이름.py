# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        #words = line.split()
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            ob.sendLine('�� ����: [�̸�] ���̸�')
            return
        ob.env['�̸�'] = line
        ob.env.save()
        ob.sendLine('���� �̸��� ���� �Ǿ����ϴ�.')
        
