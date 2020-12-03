# -*- coding: euc-kr -*-

from objs.cmd import Command
from include.ansi import *

class CmdObj(Command):

    def cmd(self, ob, line):
        write = ob.sendLine
        get = ob.get
        write('�� ' + ob.getDesc(True))
        write('�Ȧ�������������������������������������������������������')
        write('��[0m[44m[1m[37m ������������      ����� ���� ����      ������������ [0m[40m[37m��')
        write('����������������������������������������������������������')
        write('�� [��  ��]        [%6d] �� [��  ��]          %6d ��' % (get('����'), get('����')) )
        temp = '%d/%d' % (ob.getHp(), ob.getMaxHp())
        tmp = get('����')
        if tmp == '':
            tmp = '----------'
        write('�� [ü  ��] %15s �� [��  ��]      %10s ��' % (temp, tmp))
        temp = 0
        
        write('�� [  ��  ]  %5d + %6d �� [��  ��]              %2s ��' % (ob.getAttPower(), ob.getStr(), get('����')) )
        tmp = get('�Ҽ�')
        if tmp == '':
            tmp = '----------'
        write('�� [��  ��] %6d + %6d �� [��  ��]      %10s ��' % (ob.getArmor(), ob.getArm(), tmp) )
        tmp = get('����')
        if tmp == '':
            tmp = '----------'
        else:
            g = GUILD[ob['�Ҽ�']]
            if '%s��Ī' % ob['����'] in g:
                tmp = g['%s��Ī' % ob['����']]
            else:
                tmp = ob['����']
        write('�� [��  ø] %15d �� [��  ��]      %10s ��' % (ob.getDex(), tmp) )
        write('�� [٤  ��] %15d �� [��  ��] %15d ��' % (ob.getHit(), ob.getMiss()))
        write('�� [��  ߯] %15d �� [  �  ] %15d ��' % (ob.getCritical(), ob.getCriticalChance()))
        tmp = get('�����')
        if tmp == '':
            tmp = '----------'
        temp = '%d/%d' % (ob.getMp(), ob.getMaxMp())
        #write('�� [��  ��] %15d �� [�����]      %10s ��' % (ob.getMp(), tmp) )
        write('�� [��  ��] %15s �� [�����]      %10s ��' % (temp, tmp) )

        temp = '%d/%d' % (ob.getItemWeight(), ob.getStr() * 10)
        write('�� [��  ��] %15d �� [����ǰ] %15s ��' % (ob['�������ġ'], temp) )
        anger = getInt(ob['�г�'])
        if anger >= 100:
            temp = '[1;31m%d[0;37m' % anger
        else:
            temp = '%d' % anger
        write('�� [��  ��] %15d �� [��  ��]             %3s ��' % (ob.getTotalExp(), temp))
        write('����������������������������������������������������������')
        write('��[0m[47m[30m [��  ��]    %40d [0m[40m[37m��' % get('����'))
        if ob['����'] == '':
            ob['����'] = 0
        if ob['����'] > 0:
            write('��[0m[43m[30m [��  ��]    %40d [0m[40m[37m��' % get('����'))
        write('�Ʀ�������������������������������������������������������')
        if ob['�Ҽ�'] != '':
            g = GUILD[ob['�Ҽ�']]
            if '%s��Ī' % ob['����'] in g:
                buf = g['%s��Ī' % ob['����']]
            else:
                buf = ob['����']
            temp = ''
            if ob['���ĺ�ȣ'] != '':
                temp = '(%s)' % ob['���ĺ�ȣ']
            write('�� %s%s [1m��%s��[0m ������ [1m%s%s[0m �Դϴ�.' % \
                ('���', han_un('���'), ob['�Ҽ�'], buf, temp ))
        from lib.script import get_hp_script, get_mp_script
        write( '�� ' + han_parse('���', get_hp_script(ob)) )
        p = ob.getInsureCount()
        if p == 0:
            ob.sendLine('�� ����� ǥ�������� ȿ���� �����ϴ�.')
        else:
            ob.sendLine('�� ����� %d���� ǥ������ ������ ������ �� �ֽ��ϴ�.' % p)
        write( '�� ' + han_parse('���', get_mp_script(ob)) )

        p = getInt(ob['Ư��ġ'])
        if p != 0:
            ob.sendLine('�� ����� %d���� ���� Ư��ġ�� �����ϰ� �ֽ��ϴ�.' % p)
