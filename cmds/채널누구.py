# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        mode = False
        msg = ''
        cnt = 0
        
        for c in ob.adultCH:
            if c['�������'] == 1:
                continue
            if c['�̸�'] != '' and c.state == ACTIVE:
                if mode and c['�Ҽ�'] != ob['�Ҽ�']:
                    continue
                nick = c['������ȣ']
                
                if nick == '':
                    buf = '[[0;37m%s[0;37m]' % '����'
                else:
                    if c['����'] == '����':
                        buf = '[[1;32m%s[0;37m]' % nick
                    elif c['����'] == '����':
                        buf = '[[1;33m%s[0;37m]' % nick
                    elif c['����'] == '����':
                        buf = '[[1;36m%s[0;37m]' % nick
                    else:
                        buf = '<[1;31m%s[0;37m>' % nick
                    
                msg += '  %-26s %-10s' % (buf, c['�̸�'])
                cnt += 1
                if cnt % 3 == 0:
                    msg += '\r\n'
        if cnt % 3 == 0:
            msg = msg[:-2]
        ob.sendLine('������������������������������������������������������������������������������')
        ob.sendLine('��[7m%-74s[0;37m��' % ' ��     ��       ��       ũ       ��       ��       Ʈ      ��-��     ��');
        ob.sendLine('������������������������������������������������������������������������������')
        ob.sendLine(msg);
        ob.sendLine(' ����������������������������������������������������������������������������')
        if mode:
            ob.sendLine(' �� �� %d���� [1m��[36m%s[37m��[0;37m�� �������� Ȱ���ϰ� �ֽ��ϴ�.' % (cnt, ob['�Ҽ�']))
        else:
            ob.sendLine(' �� �� %d���� �������� Ȱ���ϰ� �ֽ��ϴ�.' % cnt)

