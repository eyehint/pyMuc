# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        mode = False
        msg = ''
        cnt = 0
        if line == '��' or line == '����':
            if ob['�Ҽ�'] == '':
                ob.sendLine('�� ����� �Ҽ��� �����ϴ�.')
                return
            mode = True
        
        for c in ob.channel.players:
            if c['�������'] == 1:
                continue
            if c['�̸�'] != '' and c.state == ACTIVE:
                if mode and c['�Ҽ�'] != ob['�Ҽ�']:
                    continue
                nick = c['������ȣ']
                
                if nick == '':
                    buf = '[[0;37m%s[0;37m]' % '����'
                else:
                    bright = 1
                    if c['�����ʱ�ȭ'] != '':
                       bright = 0

                    if c['����'] == '����':
                        buf = '[[%d;32m%s[0;37m]' % (bright, nick)
                    elif c['����'] == '����':
                        buf = '[[%d;33m%s[0;37m]' % (bright, nick)
                    elif c['����'] == '����':
                        buf = '[[%d;36m%s[0;37m]' % (bright, nick)
                    else:
                        buf = '<[%d;31m%s[0;37m>' % (bright, nick)
                    
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

