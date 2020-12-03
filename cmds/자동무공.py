# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        from objs.skill import MUGONG
        
        if line == '':
            if ob['�ڵ�����'] == '':
                ob.sendLine('�� �ڵ����� : ����')
                return
            else:
                ob.sendLine('�� �ڵ����� : [[1;37m%s[0;37m]' % ob['�ڵ�����'])
                return
        s = None
        if line in ob.skillList:
            s = MUGONG[line]
        else:
            for sName in ob.skillList:
                if sName.find(line) == 0:
                    s = MUGONG[sName]
                    break
        if s == None or s == '':
            ob.sendLine('�� �׷� ������ ������ ���� �����ϴ�.')
            return
        if s['����'] != '����':
            ob.sendLine('�� �ڵ������� �� �� ���� �����Դϴ�.')
            return
        ob['�ڵ�����'] = s.name
        ob.sendLine('�� �ڵ������� �����Ͽ����ϴ�.')
