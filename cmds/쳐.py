# -*- coding: euc-kr -*-

from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):

    def cmd(self, ob, line):
    
        if len(line) == 0:
            ob.sendLine('�� ����: [���] ����')
            return
        
        if ob.env.checkAttr('��������'):
            ob.sendLine('�� �̰����� ��� ������ �����Ǿ� �־��. ^^')
            return
            
        if line.find('��ü') != -1:
            ob.sendLine('�� ��ȣ���� ������ �� �ִ°Ͱ� ���°��� ����!')
            return
            
        mob = ob.env.findObjName(line)

        if mob == None:
            ob.sendLine('�� ��ȣ���� ������ �� �ִ°Ͱ� ���°��� ����!')
            return

        if is_item(mob) or is_box(mob) or is_player(mob):
            ob.sendLine('�� ��ȣ���� ������ �� �ִ°Ͱ� ���°��� ����!')
            return
        if is_player(mob) and ob.env.checkAttr('�������������'):
            ob.sendLine('�� ������ [1m[31m���[0m[37m[40m�� ����Ű�⿡ �������� ��Ȳ �̶��')
            return
            
        if is_player(mob) == False and mob['������'] != 1:
            ob.sendLine('�� ��ȣ���� ������ �� �ִ°Ͱ� ���°��� ����!')
            return
        if mob.act > ACT_FIGHT:
            ob.sendLine('�� ��ȣ���� ������ �� �ִ°Ͱ� ���°��� ����!')
            return
        
        #if mob['�̸�'] != '���ĸ�' and len(mob.target) != 0 and ob not in mob.target:
        #    ob.sendLine('�� �׷� ��밡 �����ϴ�.')
        #    return

        if mob in ob.target:
            ob.sendLine('�� �̹� �������̿���. ^_^')
            return
        
        if len(ob.target) != 0:
            ob.sendLine('�� ������ �񹫿� �Ű��� �����ϼ���. @_@')
            return
        ob.setFight(mob)
        if is_player(mob):
            mob.fightMode = True

        #ob.sendLine('����� ' + mob.get('�̸�') + han_obj(mob.get('�̸�')) + \
        #    ' �����ϱ� �����մϴ�.')
