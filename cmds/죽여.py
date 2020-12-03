# -*- coding: euc-kr -*-

from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
            
        if len(line) == 0:
            ob.sendLine('�� ����: [���] �׿�') #
            return
        
            
        #from lib.object import find_obj, is_mob
        mob = ob.env.findObjName(line)

        if mob == None:
            ob.sendLine('�� ��ȣ���� ������ �� �ִ°Ͱ� ���°��� ����!')
            return

        if not is_mob(mob):
            ob.sendLine('�� ��ȣ���� ������ �� �ִ°Ͱ� ���°��� ����!')
            return

        if mob.get('���ݱ���'):
            ob.sendLine('�� ��ȣ���� ������ �� �ִ°Ͱ� ���°��� ����!')
            return

        mob.die(ob['�̸�'])
        #mob.act = ACT_DEATH

        #ob.sendLine('����� ' + mob.get('�̸�') + han_obj(mob.get('�̸�')) + \
        #    ' �����ϱ� �����մϴ�.')
