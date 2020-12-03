# -*- coding: euc-kr -*-

from objs.cmd import Command
from include.ansi import *

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('�� ����: [��|��ø��|����|����|ȸ��|�ʻ�|��|����] �÷�')
            return

        l = ['��', '��ø��', '����', '����', 'ȸ��', '�ʻ�', '��', '����']
        l1 = ['����', 'ȸ��', '�ʻ�', '��']
        if line not in l:
            ob.sendLine('�� ����: [��|��ø��|����|����|ȸ��|�ʻ�|��|����] �÷�')
            return
     
        p = getInt(ob['Ư��ġ'])
        if p == 0:
            ob.sendLine('�� ���̻� �ø� �� �ִ� ���� Ư��ġ�� �����ϴ�.')
            return

        if line in l1:
            """
            all100 = False
            all200 = False
            if ob['����'] >= 100 and ob['ȸ��'] >= 100 and ob['�ʻ�'] >= 100 and ob['��'] >= 100:
                all100 = True
            if ob['����'] >= 200 and ob['ȸ��'] >= 200 and ob['�ʻ�'] >= 200 and ob['��'] >= 200:
                all200 = True
            if all100 == False:
                if getInt(ob[line]) >= 100:
                    ob.sendLine('�� ���̻� �ø� �� �����ϴ�.')
                    return
            if all200 == False:
                if getInt(ob[line]) >= 200:
                    ob.sendLine('�� ���̻� �ø� �� �����ϴ�.')
                    return
            if getInt(ob[line]) >= 300:
                ob.sendLine('�� ���̻� �ø� �� �����ϴ�.')
                return
            """
            if getInt(ob[line]) >= 100:
                ob.sendLine('�� ���̻� �ø� �� �����ϴ�.')
                return
        if line == '��ø��':
            if ob['��ø��'] >= 2800:
                ob.sendLine('�� ���̻� �ø� �� �����ϴ�.')
                return

        ob['Ư��ġ'] -= 1
        if ob[line] == '':
            ob[line] = 0
        if line == '����':
            ob['�ְ���'] += 10
        else:
            ob[line] += 1 
        if line in ['��', '��ø��']:
            x = ob[line+'Ư��ġ']
            if x == '':
                x = 0
            x += 1
            ob[line+'Ư��ġ'] = x
        ob.save()
        ob.sendLine('�� [%s] Ư��ġ�� �÷Ƚ��ϴ�.' % line)
