# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            ob.sendLine('�� ��� ���: [���] ��ȸ��')
            return
        obj = ob.env.findObjName(line)
        if obj == None or is_mob(obj) == False:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        obj.hp = obj['ü��']
        ob.sendLine('* ȸ���Ǿ����ϴ�.')
