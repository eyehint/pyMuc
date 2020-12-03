# -*- coding: euc-kr -*-

from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            name = '���'
            target = ob
        else:
            target = ob.env.findObjName(line)
            if target == None or is_player(target) == False:
                ob.sendLine('�� ����� �ȱ����δ� �׷����� ���� ���ٳ�')
                return
            name = target['�̸�']
        c = 0
        tmp = ''
        for obj in target.objs:
            if obj['����'] == 'ȣ��':
                try:
                    a = obj.hp
                except:
                    obj.hp = obj['ü��']
                guard = obj
                c += 1
                hp = (obj.hp * 100 )/ getItem(obj.index)['ü��']
                
                tmp += '[1;32m��[0;36m%2d.%s[0;37m �� %s (%d)\r\n' % (c, obj['�̸�'], ob.strBar[hp/10] , hp)
        
        if c == 0:
            if target == ob:
                ob.sendLine('����� ȣ���� �Ŵ����� �ʰ� �ֽ��ϴ�.')
            else:
                ob.sendLine('%s ȣ���� �Ŵ����� �ʰ� �ֽ��ϴ�.' % target.han_un())
            return
        msg = '��������������������������������������������������������\r\n'
        buf = '�� %s�� ȣ�� : %s, ȣ���� : %d, �г� : %d' % (name, guard['�̸�'], c, getInt(target['�г�']))
        msg += '[1;44m%-56s[0;40m\r\n' % buf
        msg += '��������������������������������������������������������\r\n'
        msg += guard['����2'] + '\r\n'
        msg += '��������������������������������������������������������\r\n'
        msg += tmp
        msg += '��������������������������������������������������������'
        ob.sendLine(msg)


