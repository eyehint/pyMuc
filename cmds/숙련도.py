# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        ob.sendLine('[1m �� ����� ���� ���õ� ��[0m[40m[37m')
        ob.sendLine('��������������������������')
        ob.sendLine('����  ��  ����[1m%10d[0m[40m[37m��' % getInt(ob['1 ���õ�']))
        ob.sendLine('��������������������������')
        ob.sendLine('����  ��  ����[1m%10d[0m[40m[37m��' % getInt(ob['2 ���õ�']))
        ob.sendLine('��������������������������')
        ob.sendLine('����  â  ����[1m%10d[0m[40m[37m��' % getInt(ob['3 ���õ�']))
        ob.sendLine('��������������������������')
        ob.sendLine('���� ��Ÿ ����[1m%10d[0m[40m[37m��' % getInt(ob['4 ���õ�']))
        ob.sendLine('��������������������������')
        ob.sendLine('���� �Ǽ� ����[1m%10d[0m[40m[37m��' % getInt(ob['5 ���õ�']))
        ob.sendLine('��������������������������')

