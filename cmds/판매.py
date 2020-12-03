# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('�� ����: [��ǰ�̸�] [����] �Ǹ�')
            return
        words = line.split()
        count = 1
        if len(words) >= 2:
            count = getInt(words[1])
            if count <= 0:
                count = 1
            if count > 100:
                count = 100

        mob = ob.env.findMerchant()
        if mob == None:
            ob.sendLine('�� �׷� ������ �� ������ �����. ^_^')
            return
        if mob['���Ǳ���'] == '':
            ob.sendLine('�� �׷� ������ �� ������ �����. ^_^')
            return

        w = mob['���Ǳ���'].split()
        percent = int(w[1])

        if line == '�Ӽ�1':
            c = 0
            objs = copy.copy(ob.objs)
            for item in objs:
                if item.checkAttr('�����ۼӼ�', '��¾���'):
                    continue
                if item.inUse == True:
                    continue
                if item.checkAttr('�����ۼӼ�', '��������'):
                    continue
                if item['����'] != '��' and item['����'] != '����':
                    continue
                if item['�ɼ�'] != None and len(item['�ɼ�'].split('\n')) > 2:
                    continue
 
                p = (getInt(item['�ǸŰ���']) * percent) / 100
                op = item.getOption()
                if op != None:
                    p = int( p * (len(op) * 1.2) )
                ob['����'] += p
                ob.remove(item)
                if item.isOneItem():
                    ONEITEM.destroy(item.index)
                ob.sendLine('����� %s 1���� ���� %d���� �Ǹ��մϴ�.' % ( item.getNameA(), p))
                ob.sendRoom('%s %s 1���� ���� %d���� �Ǹ��մϴ�.' % ( ob.han_iga(), item.getNameA(), p))
                del item
                c += 1
            if c == 0:
                ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            return
        if line == '�Ӽ�2':
            c = 0
            objs = copy.copy(ob.objs)
            for item in objs:
                if item.checkAttr('�����ۼӼ�', '��¾���'):
                    continue
                if item.inUse == True:
                    continue
                if item.checkAttr('�����ۼӼ�', '��������'):
                    continue
                if item['����'] != '��' and item['����'] != '����':
                    continue
                if item['�ɼ�'] != None and len(item['�ɼ�'].split('\n')) > 3:
                    continue
 
                p = (getInt(item['�ǸŰ���']) * percent) / 100
                op = item.getOption()
                if op != None:
                    p = int( p * (len(op) * 1.2) )
                ob['����'] += p
                ob.remove(item)
                if item.isOneItem():
                    ONEITEM.destroy(item.index)
                ob.sendLine('����� %s 1���� ���� %d���� �Ǹ��մϴ�.' % ( item.getNameA(), p))
                ob.sendRoom('%s %s 1���� ���� %d���� �Ǹ��մϴ�.' % ( ob.han_iga(), item.getNameA(), p))
                del item
                c += 1
            if c == 0:
                ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            return
        if line == '�Ӽ�3':
            c = 0
            objs = copy.copy(ob.objs)
            for item in objs:
                if item.checkAttr('�����ۼӼ�', '��¾���'):
                    continue
                if item.inUse == True:
                    continue
                if item.checkAttr('�����ۼӼ�', '��������'):
                    continue
                if item['����'] != '��' and item['����'] != '����':
                    continue
                if item['�ɼ�'] != None and len(item['�ɼ�'].split('\n')) > 4:
                    continue
 
                p = (getInt(item['�ǸŰ���']) * percent) / 100
                op = item.getOption()
                if op != None:
                    p = int( p * (len(op) * 1.2) )
                ob['����'] += p
                ob.remove(item)
                if item.isOneItem():
                    ONEITEM.destroy(item.index)
                ob.sendLine('����� %s 1���� ���� %d���� �Ǹ��մϴ�.' % ( item.getNameA(), p))
                ob.sendRoom('%s %s 1���� ���� %d���� �Ǹ��մϴ�.' % ( ob.han_iga(), item.getNameA(), p))
                del item
                c += 1
            if c == 0:
                ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            return

        if line == '�Ϲ�':
            c = 0
            objs = copy.copy(ob.objs)
            for item in objs:
                if item.checkAttr('�����ۼӼ�', '��¾���'):
                    continue
                if item.inUse == True:
                    continue
                if item.checkAttr('�����ۼӼ�', '��������'):
                    continue
                if item['����'] != '��' and item['����'] != '����':
                    continue
                if item['�ɼ�'] == None:
                    pass
                elif item['�ɼ�'] != None and len(item['�ɼ�']) != 0:
                    continue
 
                p = (getInt(item['�ǸŰ���']) * percent) / 100
                op = item.getOption()
                if op != None:
                    p = int( p * (len(op) * 1.2) )
                ob['����'] += p
                ob.remove(item)
                if item.isOneItem():
                    ONEITEM.destroy(item.index)
                ob.sendLine('����� %s 1���� ���� %d���� �Ǹ��մϴ�.' % ( item.getNameA(), p))
                ob.sendRoom('%s %s 1���� ���� %d���� �Ǹ��մϴ�.' % ( ob.han_iga(), item.getNameA(), p))
                del item
                c += 1
            if c == 0:
                ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            return

        if line == '���':
            c = 0
            objs = copy.copy(ob.objs)
            for item in objs:
                if item.checkAttr('�����ۼӼ�', '��¾���'):
                    continue
                if item.inUse == True:
                    continue
                if item.checkAttr('�����ۼӼ�', '��������'):
                    continue
                if item['����'] != '��' and item['����'] != '����':
                    continue
 
                p = (getInt(item['�ǸŰ���']) * percent) / 100
                op = item.getOption()
                if op != None:
                    p = int( p * (len(op) * 1.2) )
                ob['����'] += p
                ob.remove(item)
                if item.isOneItem():
                    ONEITEM.destroy(item.index)
                ob.sendLine('����� %s 1���� ���� %d���� �Ǹ��մϴ�.' % ( item.getNameA(), p))
                ob.sendRoom('%s %s 1���� ���� %d���� �Ǹ��մϴ�.' % ( ob.han_iga(), item.getNameA(), p))
                del item
                c += 1
            if c == 0:
                ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            return

        if line == '���':
            c = 0
            objs = copy.copy(ob.objs)
            for item in objs:
                if item.checkAttr('�����ۼӼ�', '��¾���'):
                    continue
                if item.inUse == True:
                    continue
                if item.checkAttr('�����ۼӼ�', '��������'):
                    continue
 
                p = (getInt(item['�ǸŰ���']) * percent) / 100
                op = item.getOption()
                if op != None:
                    p = int( p * (len(op) * 1.2) )
                ob['����'] += p
                ob.remove(item)
                if item.isOneItem():
                    ONEITEM.destroy(item.index)
                ob.sendLine('����� %s 1���� ���� %d���� �Ǹ��մϴ�.' % ( item.getNameA(), p))
                ob.sendRoom('%s %s 1���� ���� %d���� �Ǹ��մϴ�.' % ( ob.han_iga(), item.getNameA(), p))
                del item
                c += 1
            if c == 0:
                ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            return

        name, order = getNameOrder(words[0])
        if order != 1:
            count = 1

        item = ob.findObjInven(name, order)
        if item == None:
            ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            return
        if item.checkAttr('�����ۼӼ�', '��¾���'):
            ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            return
        if item.inUse == True:
            ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            return
        if item.checkAttr('�����ۼӼ�', '��������'):
            ob.sendLine('�� �� �������� �� ���� �����~')
            return
        
        c = 0
        sum = 0
        p = (getInt(item['�ǸŰ���']) * percent) / 100
        obj = item
        for i in range(count):
            p = (getInt(obj['�ǸŰ���']) * percent) / 100
            op = obj.getOption()
            if op != None:
                p = int( p * (len(op) * 1.3) )
            ob['����'] += p
            sum += p
            c += 1
            ob.remove(obj)
            if obj.isOneItem():
                ONEITEM.destroy(obj.index)
            del obj
            if order != 1:
                break
            obj = ob.findObjInven(name)
            if obj == None:
                break
            if obj.inUse == True:
                break
        if c == 0:
            ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
        else:
            ob.sendLine('����� %s %d���� ���� %d���� �Ǹ��մϴ�.' % ( item.getNameA(), c, sum))
            ob.sendRoom('%s %s %d���� ���� %d���� �Ǹ��մϴ�.' % ( ob.han_iga(), item.getNameA(), c, sum))
