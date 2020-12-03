# -*- coding: euc-kr -*-

from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):

    def view(self, obj, ob):
        p = int(obj['��������'])
        pm = obj['������������']
        pp = obj['�����ִ����']
        
        ob.sendLine('������������������������������������������������������������������������������')
        buf = '�� %s�� %s ��' % (obj['����'], obj['�̸�'])
        ob.sendLine('[1m[44m[37m%-78s[0m[40m[37m' % buf)
        ob.sendLine('������������������������������������������������������������������������������')
        c = 0
        msg = ''
        for item in obj.objs:
            c += 1
            s = item['�̸�'] + ' ' + item.getOptionStr()
            s = '[%4d] %s' % (c, s)
            s1 = stripANSI(s)
            space = ' ' * (38 - len(s1))
            msg += '%-38s' % (s + space)
            #msg += '��%-24s' % (s + space)
            #msg += '[1;36m��[0;36m%-38s[0;37m  ' % (item['�̸�'] + ' ' + item.getOptionStr())
            if c % 2 == 0:
                msg += '\r\n'
        if msg != '':
            ob.sendLine(msg)

        if c == 0:
            ob.sendLine('�� �ƹ��͵� �����ϴ�.')

        if obj['��������'] == obj['�����ִ����']:
            buf = '�� ���� (%d/%d)' % ( len(obj.objs), obj['��������'])
        else:
            buf = '�� ���� (%d/%d)  �� �ִ���� (%d)  �� Ȯ�忡 �ʿ��� ���� (%d/%d)' % ( len(obj.objs), obj['��������'], \
            obj['�����ִ����'], getInt(obj['����']), obj['������������'])
        ob.sendLine('������������������������������������������������������������������������������')
        ob.sendLine('[0m[47m[30m%-78s[0m[40m[37m' % buf)
        ob.sendLine('������������������������������������������������������������������������������')

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.viewMapData()
            return
        if ob.env == None:
            print ob['�̸�']
            return

        words = line.split()
        if line == 'ȣ��' or (len(words) > 1 and words[1] == 'ȣ��'):
            ob.do_command(line, True)
            return
        name, order = getNameOrder(line)

        
        if line == '��':
            obj = ob
        else:
            obj = ob.findObjInven(name, order)

        if obj == None:
            obj = ob.env.findObjName(line)
            if obj == None:
                ob.sendLine('�� ����� �ȱ����δ� �׷����� ���� ���ٳ�')
                return
        if getInt(ob['�����ڵ��']) >= 1000 and is_player(obj) == False:
            ob.sendLine('Index : %s' % obj.index)
        if (line == '�����' or line == 'ȭ����' or line == '�ѿ���') and is_box(obj):
            self.view(obj, ob)
        else:
            obj.view(ob)
        if is_player(obj) and obj != ob:
            obj.sendLine('\r\n%s ����� ���캾�ϴ�.' % ob.han_iga())
            obj.lpPrompt()
