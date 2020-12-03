# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line != '' and getInt(ob['�����ڵ��']) >= 1000:
            target = ob.env.findObjName(line)
            if target == None or is_item(target):
                ob.sendLine('�� ����� �ȱ����δ� �׷����� ���� ���ٳ�')
                return
        else:
            target = ob
        
        ob.sendLine('������������������������������������������������������������������������������')
        if target == ob:
            buf = '�� ����� ���� ��'
        else:
            buf = '�� %s�� ���� ��' % target['�̸�']
        ob.sendLine('[0m[47m[30m%-78s[0m[40m[37m' % buf)
        ob.sendLine('������������������������������������������������������������������������������')
        ob.sendLine('[1m[40m[32m�� �Ϲݹ���[0m[40m[37m')
        msg = ''
        if len(target.skillList) == 0:
            ob.sendLine('�� ����ģ ������ �����ϴ�.')
        else:
            c = 0
            for m in target.skillList:
                if m not in target.skillMap:
                    s = 1
                else:
                    s = target.skillMap[m][0]
                buf = '%s(%d��)' % (m, s)
                msg += ' �� %-20s ' % buf
                c += 1
                if c % 3 == 0:
                    msg += '\r\n'
            if c % 3 == 0:
                msg = msg[:-2]
            ob.sendLine(msg)
        ob.sendLine('������������������������������������������������������������������������������')
        
        ob.sendLine('[1m[40m[32m�� ����[0m[40m[37m')
        buf = target['��������']
        lines = target['�����̸�'].splitlines()
        if buf == '' and len(lines) == 0:
            ob.sendLine('�� ���Ǹ� ����ģ ������ �����ϴ�.')
        else:
            if buf != '':
                msg = '[1m[33m%s[0m[40m[37m(������)\r\n' % buf
            else:
                msg = ''
            c = 0
            for m in lines:
                msg += ' �� %-20s ' % m
                c += 1
                if c % 3 == 0:
                    msg += '\r\n'
            if c % 3 == 0:
                msg = msg[:-2]
            ob.sendLine(msg)
        ob.sendLine('������������������������������������������������������������������������������')
        