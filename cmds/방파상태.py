# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob['�Ҽ�'] == '':
            ob.sendLine('�� ����� �Ҽ��� �����ϴ�.')
            return
        g = GUILD[ob['�Ҽ�']]
        l1 = []
        l2 = []
        l3 = []
        if '�ι��ָ���Ʈ' in g:
            l1 = g['�ι��ָ���Ʈ']
        if '��θ���Ʈ' in g:
            l2 = g['��θ���Ʈ']
        if '�����θ���Ʈ' in g:
            l3 = g['�����θ���Ʈ']

        Num = 0
        msg = MAIN_CONFIG['���Ļ�����»��']
        msg += MAIN_CONFIG['���Ļ������']
        msg += '[1;31m[1;47m%s[0;37;40m\r\n' % ob['�Ҽ�']
        msg += MAIN_CONFIG['���Ļ�������ϴ�']
        msg += '\r\n  [[1m[31m��  ��[0m[40m[37m]     %-11s' % g['�����̸�']
        Num += 1
        for buf in l1:
            msg += '  [[1m[33m�ι���[0m[40m[37m]     %-11s' % buf
            Num += 1
        if Num % 3 == 0:
            msg += '\r\n'
        for buf in l2:
            msg += '  [[1m[32m��  ��[0m[40m[37m]     %-11s' % buf
            Num += 1
            if Num % 3 == 0:
                msg += '\r\n'
        for buf in l3:
            msg += '  [[1m���Ŀ�[0m[40m[37m]     %-11s' % buf
            Num += 1
            if Num % 3 == 0:
                msg += '\r\n'

        msg += '\r\n' + MAIN_CONFIG['���Ļ�������ϴ�']
        msg += '\r\n�������ο� : %-8d' % g['���Ŀ���']
        cnt = 0
        for ply in ob.channel.players:
            if ply['�Ҽ�'] == ob['�Ҽ�'] and ply.state == ACTIVE and getInt(ply['�������']) != 1:
                cnt += 1
        msg += '�� ���� %d���� Ȱ���� �Դϴ�.' % cnt
        
        ob.sendLine(msg)
        
