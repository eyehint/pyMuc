# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        from objs.skill import MUGONG
        
        if line == '':
            if ob['��������'] == '':
                ob.sendLine('�� ���� : ����')
                return
            else:
                ob.sendLine('�� ���� : [[1;37m%s[0;37m]' % ob['��������'])
                return
        s = None
        vision = ob['�����̸�'].splitlines()
        if line not in vision:
            ob.sendLine('�� ����� �׷� ������ ������� �����ϴ�.')
            return
        ob['��������'] = line
        ob.sendLine('�� ������ �����Ͽ����ϴ�.')
