# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        mob = ob.env.findObjName('ǥ��')
        if mob == None:
            ob.sendLine('�� �̰��� ǥ�����簡 ���׿�.')
            return
        p = ob['�����']
        c1 = ob['����'] * MAIN_CONFIG['�����ܰ�']
        c2 = c1 * MAIN_CONFIG['���������'] / 100
        msg = '����� ����� �Ѿ��� ���� [1m%d[0;37m���̸�\r\n���� ������ [1m%d[0m[40m[37m�� ������ �� �ֽ��ϴ�.\r\n' %(p, ob.getInsureCount())
        msg += '���������� ����Ǵ� �ݾ��� ���� [1m%d[0;37m�� �̻��̸�\r\n' % c1
        msg += '�ѹ��� ���� ó���ÿ� ���� [1m%d[0;37m���� �ҿ�˴ϴ�.' % c2
        ob.sendLine(msg)
            

