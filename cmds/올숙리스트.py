# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        msg = '[�ü��������ε���]\r\n'
        for index in Item.Items:
            item = Item.Items[index]
            if item['�����'] != 0 and item['�����'] != '':
                msg += '#%s\r\n:%s\r\n\r\n' % (item['�̸�'], item.index)
        ob.sendLine(msg)
