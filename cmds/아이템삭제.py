# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if len(line) == 0:
            ob.sendLine('����: [������ �ε���] �����ۻ���')
            return

        item = getItem(line)
        if item == None:
            ob.sendLine('���������ʴ� �������Դϴ�.')
            return
        Item.Items.__delitem__(item.index)
        del item
        ob.sendLine('�������� �����Ǿ����ϴ�.')
        

