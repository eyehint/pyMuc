# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        msg = '������������������������������������������������������������������������������\r\n'
        msg += '�� ���� ����Ʈ\r\n'
        msg += '������������������������������������������������������������������������������\r\n'
        for g in GUILD.attr:
            guild = GUILD.attr[g]
            buf = '[%s]' % guild['�̸�']
            if  getInt(ob['�����ڵ��']) >= 1000:
                msg += '%-12s : %-30s   %3d �� %s\r\n' % (buf, guild['�����̸�'], guild['���Ŀ���'], guild['���ĸ�'])
            else:
                msg += '%-12s : %-30s   %3d ��\r\n' % (buf, guild['�����̸�'], guild['���Ŀ���'])

        msg += '������������������������������������������������������������������������������'
        ob.sendLine(msg)
