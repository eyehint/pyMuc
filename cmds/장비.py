# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        from lib.script import get_arm_script
        ob.sendLine('������������������������������������������������������')
        ob.sendLine('[0m[44m[1m[37m�� %-51s[0m[37m[40m' % han_parse('���', get_arm_script(ob)))
        ob.sendLine('������������������������������������������������������')
        c = 0
        item_str = ''
        for lv in ob.ItemLevelList:
            for item in ob.objs:
                if item.inUse and lv == item['����']:
                    c += 1
                    name = stripANSI(item.get('�̸�'))
                    if is_han(name):
                        item_str += '[' + ob.ItemUseLevel[item.get('����')] + '] [36m' + item.get('�̸�') + '[37m\r\n'
                    else:
                        item_str += '[' + ob.ItemUseLevel[item.get('����')] + '] [36m' + item.get('�̸�') + '(' + item.get('�����̸�').split()[0] + ')[37m\r\n'
        ob.write(item_str)
        if c == 0:
            ob.sendLine('[36m�� �����ܽ� �Ǹ����� ��ȣ�� �������Դϴ�.[37m')
        ob.sendLine('������������������������������������������������������')
        ob.sendLine('�����¡��� %d    �����ݷ¡��� %d' % (ob.getArmor(),ob.getAttPower()))
        ob.sendLine('������������������������������������������������������')
