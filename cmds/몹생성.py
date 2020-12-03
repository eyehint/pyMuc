# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if len(line) == 0:
            ob.sendLine('����: [�� �̸�] ����')
            return

        mob = getMob(line)

        if mob == None:
            ob.sendLine('* ���� ����!!!')
            return
            

        mob = mob.clone()
        mob.place()
        ob.sendLine('[1;32m* [' + mob.get('�̸�') + '] ���� �Ǿ����ϴ�.[0;37m')

