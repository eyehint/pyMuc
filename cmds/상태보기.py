# -*- coding: euc-kr -*-

from objs.cmd import Command
from include.ansi import *

class CmdObj(Command):

    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            ob.sendLine('�� ��� ���: [���] ���º���')
            return
        obj = ob.env.findObjName(line)
        if obj == None or is_item(obj):
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if is_player(obj) == False:
            ob.sendLine('Index : %s' % obj.index)
        write = ob.sendLine
        get = obj.get
        write('�Ȧ���������������������������������������������������')
        write('��[0m[44m[1m[37m ���������� %10s�� ���� ����     ���������� [0m[40m[37m��' % obj['�̸�'])
        write('������������������������������������������������������')
        write('�� [��  ��]       [%5d] �� [��  ��]          %4d ��' % (get('����'), getInt(get('����'))) )
        if is_player(obj):
            temp = '%d/%d' % (obj.getHp(), obj.getMaxHp())
        else:
            temp = '%d/%d' % (obj.hp, get('ü��'))
        tmp = get('����')
        if tmp == '':
            tmp = '--------'
        write('�� [ü  ��] %13s �� [��  ��]      %8s ��' % (temp, tmp))
        temp = 0
        tmp = get('����')
        if tmp == '':
            tmp = '--'
        write('�� [  ��  ]  %4d + %5d �� [��  ��]            %2s ��' % (obj.getAttPower(), obj.getStr(), tmp) )

        tmp = get('�Ҽ�')
        if tmp == '':
            tmp = '--------'
        write('�� [��  ��] %5d + %5d �� [��  ��]      %8s ��' % (obj.getArmor(), obj.getArm(), tmp) )
        tmp = get('����')
        if tmp == '':
            tmp = '--------'
        write('�� [��  ø]  %12d �� [��  ��]      %8s ��' % (obj.getDex(), tmp) )
        tmp = get('�����')
        if tmp == '':
            tmp = '--------'
        temp = '%d/%d' % (obj.getMp(), obj.getMaxMp())
        write('�� [��  ��]  %12s �� [�����]      %8s ��' % (temp, tmp) )

        temp = '%d/%d' % (obj.getItemWeight(), obj.getStr() * 10)
        
        write('�� [��  ��]  %12d �� [����ǰ]  %12s ��' % (getInt(obj['�������ġ']), temp) )

        write('�� [��  ��]  %12d �� [��  ��]           %3d ��' % (obj.getTotalExp(), 0) )
        write('�� [٤  ��] %15d �� [��  ��] %15d ��' % (obj.getHit(), obj.getMiss()))
        write('�� [��  ߯] %15d �� [  �  ] %15d ��' % (obj.getCritical(), obj.getCriticalChance()))
        write('������������������������������������������������������')
        write('��[0m[47m[30m [��  ��]                    %20d [0m[40m[37m��' % getInt(get('����')))
        write('�Ʀ���������������������������������������������������')
        from lib.script import get_hp_script, get_mp_script
        write( '�� ' + han_parse(get('�̸�'), get_hp_script(ob)) )
        p = obj.getInsureCount()
        if p == 0:
            ob.sendLine('�� %s�� ǥ�������� ȿ���� �����ϴ�.' % obj.getNameA())
        else:
            ob.sendLine('�� %s %d���� ǥ������ ������ ������ �� �ֽ��ϴ�.' % (obj.han_iga(), p))
        write( '�� ' + han_parse(get('�̸�'), get_mp_script(obj)) )

        p = getInt(obj['Ư��ġ'])
        if p != 0:
            ob.sendLine('�� %s %d���� ���� Ư��ġ�� �����ϰ� �ֽ��ϴ�.' % (obj.han_un(), p))
