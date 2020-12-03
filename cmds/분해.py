# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('�� ����: [���] ����')
            return
        words = line.split()

        if len(words) != 1:
            ob.sendLine('�� ����: [���] ����')
            return

        mob = ob.env.findMerchant()
        if mob == None:
            ob.sendLine('�� ������ �����. ^_^')
            return
        if mob['���Ǳ���'] == '':
            ob.sendLine('�� ������ �����. ^_^')
            return

        if line == '���':
            c = 0
            objs = copy.copy(ob.objs)
            for item in objs:
                if '�ü�����' in item.index:
                    continue
                if item.checkAttr('�����ۼӼ�', '��¾���'):
                    continue
                if item.inUse == True:
                    continue
                if item['����'] != '��' and item['����'] != '����':
                    continue
 
                op = item.getOption()
                if op == None:
                    continue  

                if len(op) >= 4:
                    c += 1
                ob.remove(item)
                if item.isOneItem():
                    ONEITEM.destroy(item.index)
                ob.sendLine('����� %s 1���� �����մϴ�.' % item.getNameA())
                ob.sendRoom('%s %s 1���� �����մϴ�.' % ( ob.han_iga(), item.getNameA()))
                del item
                c += 1
            if c == 0:
                ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
                return
            itm = getItem('��ö����')
            for i in xrange(c):
                it = itm.deepclone()
                ob.objs.append(it)
        else:
            ob.sendLine('�� ����: [���] ����')
            return


