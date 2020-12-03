# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('�� ����: [�ݾ�] �Ա�')
            return
        mob = ob.env.findObjName('ǥ��')
        if mob == None:
            ob.sendLine('�� �̰��� ǥ�����簡 ���׿�.')
            return
        m = getInt(line)
        if m <= 0:
            ob.sendLine('�� ���� 1�� �̻� �Ա� �ϼž� �ؿ�.')
            return
        if m > ob['����']:
            m = ob['����']
        ob['����'] -= m
        ob['�����'] += m
        msg = '����� ���� %d���� ǥ�����翡�� �Ա��մϴ�.\r\n\r\n' % m
        msg += '����� ����� �Ѿ��� ���� [1m%d[0;37m���̸�\r\n���� ������ [1m%d[0m[40m[37m�� ������ �� �ֽ��ϴ�.' %(ob['�����'], ob.getInsureCount())

        ob.sendLine(msg)
            

