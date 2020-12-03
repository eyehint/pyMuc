# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        words = line.split()
        if len(line) == 0 or len(words) < 2:
            ob.sendLine('�� ����: [�������̸�] [��ǰ] �־�')
            return
        box = ob.env.findObjName(words[0])
        if box == None or is_box(box) == False:
            ob.sendLine('�� ����� �ȱ����δ� �׷����� ���� ���ٳ�')
            return
            
        if words[1] == '����':
            if box.isExpandable() == False:
                ob.sendLine('�� �� �̻� ������ ������ �ȵǿ�. ^^')
                return
            if len(words) < 3:
                m = 1
            else:
                m = getInt(words[2])
            if m <= 0:
                m = 1
            if ob['����'] < m:
                ob.sendLine('�� ���� ���ڶ�׿�. ^^')
                return
            n = box.addMoney(m)
            ob['����'] -= n
            ob.sendLine('����� %s�� ���� %d���� �����մϴ�.' % ( box.getNameA(), n ))
            ob.sendRoom('%s %s�� ���� %d���� �����մϴ�.' % ( ob.han_iga(), box.getNameA(), n))
            box.save()
            return
        if words[1] == '���':
            objs = copy.copy(ob.objs)
            c = 0
            nCnt = {}
            for item in objs:
                if box.isFull():
                    if c == 0:
                        ob.sendLine('�� �����Կ� �� �̻� ���� �� �����. ^^')
                        return
                    break
                if item['����'] not in box['��������'].splitlines():
                    continue
                if item.checkAttr('�����ۼӼ�', '��������'):
                    continue
                if box.checkAttr('�����ۼӼ�', '���뺸����') and \
                    (item.checkAttr('�����ۼӼ�', '�ټ�����') or \
                    item.checkAttr('�����ۼӼ�', '����������') or \
                    item.checkAttr('�����ۼӼ�', '��������') or \
                    item.checkAttr('�����ۼӼ�', '�μ�������')):
                    continue
                if item.inUse:
                    continue
                ob.remove(item)
                box.insert(item)
                if item.isOneItem():
                    ONEITEM.keep(item.index, ob['�̸�'] + ' %s' % box['�̸�'])
                nc = 0
                try:
                    nc = nCnt[item['�̸�']]
                except:
                    nCnt[item['�̸�']] = 0
                nCnt[item['�̸�']] = nc + 1
                c += 1
            if c == 0:
                ob.sendLine('�� ���̻� ������ ������ �����. ^^')
                return
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('����� %s�� [36m%s[37m%s �����մϴ�.' % (box.getNameA(), name, han_obj(name)))
                        msg += '%s %s�� [36m%s[37m%s �����մϴ�.\r\n' % (ob.han_iga(), box.getNameA(), name, han_obj(name))
                    else:
                        ob.sendLine('����� %s�� [36m%s[37m %d���� �����մϴ�.' % (box.getNameA(), name, nc))
                        msg += '%s %s�� [36m%s[37m %d���� �����մϴ�.\r\n' % (ob.han_iga(), box.getNameA(), name, nc)
                ob.sendRoom(msg[:-2])
            box.save()
            return
        if words[1] == '�Ӽ�������':
            objs = copy.copy(ob.objs)
            c = 0
            nCnt = {}
            for item in objs:
                if box.isFull():
                    if c == 0:
                        ob.sendLine('�� �����Կ� �� �̻� ���� �� �����. ^^')
                        return
                    break
                if item['����'] not in box['��������'].splitlines():
                    continue
                if item.checkAttr('�����ۼӼ�', '��������'):
                    continue
                if box.checkAttr('�����ۼӼ�', '���뺸����') and \
                    (item.checkAttr('�����ۼӼ�', '�ټ�����') or \
                    item.checkAttr('�����ۼӼ�', '����������') or \
                    item.checkAttr('�����ۼӼ�', '��������') or \
                    item.checkAttr('�����ۼӼ�', '�μ�������')):
                    continue
                if item.inUse:
                    continue
                if item.getOption() == None:
                    continue
                ob.remove(item)
                box.insert(item)
                if item.isOneItem():
                    ONEITEM.keep(item.index, ob['�̸�'] + ' %s' % box['�̸�'])
                nc = 0
                try:
                    nc = nCnt[item['�̸�']]
                except:
                    nCnt[item['�̸�']] = 0
                nCnt[item['�̸�']] = nc + 1
                c += 1
            if c == 0:
                ob.sendLine('�� ���̻� ������ ������ �����. ^^')
                return
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('����� %s�� [36m%s[37m%s �����մϴ�.' % (box.getNameA(), name, han_obj(name)))
                        msg += '%s %s�� [36m%s[37m%s �����մϴ�.\r\n' % (ob.han_iga(), box.getNameA(), name, han_obj(name))
                    else:
                        ob.sendLine('����� %s�� [36m%s[37m %d���� �����մϴ�.' % (box.getNameA(), name, nc))
                        msg += '%s %s�� [36m%s[37m %d���� �����մϴ�.\r\n' % (ob.han_iga(), box.getNameA(), name, nc)
                ob.sendRoom(msg[:-2])
            box.save()
            return
        if words[1] == '����':
            objs = copy.copy(ob.objs)
            c = 0
            nCnt = {}
            for item in objs:
                if box.isFull():
                    if c == 0:
                        ob.sendLine('�� �����Կ� �� �̻� ���� �� �����. ^^')
                        return
                    break
                if item['����'] not in box['��������'].splitlines():
                    continue
                if item.checkAttr('�����ۼӼ�', '��������'):
                    continue
                if box.checkAttr('�����ۼӼ�', '���뺸����') and \
                    (item.checkAttr('�����ۼӼ�', '�ټ�����') or \
                    item.checkAttr('�����ۼӼ�', '����������') or \
                    item.checkAttr('�����ۼӼ�', '��������') or \
                    item.checkAttr('�����ۼӼ�', '�μ�������')):
                    continue
                if item.inUse:
                    continue
                if item['�����̸�'] != '����':
                    continue
                ob.remove(item)
                box.insert(item)
                if item.isOneItem():
                    ONEITEM.keep(item.index, ob['�̸�'] + ' %s' % box['�̸�'])
                nc = 0
                try:
                    nc = nCnt[item['�̸�']]
                except:
                    nCnt[item['�̸�']] = 0
                nCnt[item['�̸�']] = nc + 1
                c += 1
            if c == 0:
                ob.sendLine('�� ���̻� ������ ������ �����. ^^')
                return
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('����� %s�� [36m%s[37m%s �����մϴ�.' % (box.getNameA(), name, han_obj(name)))
                        msg += '%s %s�� [36m%s[37m%s �����մϴ�.\r\n' % (ob.han_iga(), box.getNameA(), name, han_obj(name))
                    else:
                        ob.sendLine('����� %s�� [36m%s[37m %d���� �����մϴ�.' % (box.getNameA(), name, nc))
                        msg += '%s %s�� [36m%s[37m %d���� �����մϴ�.\r\n' % (ob.han_iga(), box.getNameA(), name, nc)
                ob.sendRoom(msg[:-2])
            box.save()
            return
        itm = None 
        item = ob.findObjInven(words[1])
        if item == None:
            name, order = getNameOrder(words[1])
            itm = item = ob.findObjInven(name, order) 
            if item == None:
                ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
                return
            
        if item['����'] not in box['��������'].splitlines():
            ob.sendLine('�� ���� �� �� ���� ��ǰ�Դϴ�. ^^')
            return
        
        if item.checkAttr('�����ۼӼ�', '��������'):
            ob.sendLine('�� ���� �� �� ���� ��ǰ�Դϴ�. ^^')
            return
            
        if box.checkAttr('�����ۼӼ�', '���뺸����') and \
            (item.checkAttr('�����ۼӼ�', '�ټ�����') or \
            item.checkAttr('�����ۼӼ�', '����������') or \
            item.checkAttr('�����ۼӼ�', '��������') or \
            item.checkAttr('�����ۼӼ�', '�μ�������')):
                ob.sendLine('�� ���� �� �� ���� ��ǰ�Դϴ�. ^^')
                return
        count = 1
        if len(words) > 2:
            count = getInt(words[2])
        
        if itm != None:
            count = 1
        objs = copy.copy(ob.objs)
        c = 0
        nCnt = {}
        oCnt = 1
        for item in objs:
            if itm == None:
                if words[1] != item['�̸�'] and words[1] not in item['�����̸�'].splitlines():
                    continue
            else:
                if name != item['�̸�'] and name not in item['�����̸�'].splitlines():
                    continue

            if itm != None:
                if order != oCnt:
                    oCnt += 1
                    continue

            if box.isFull():
                if c == 0:
                    ob.sendLine('�� �����Կ� �� �̻� ���� �� �����. ^^')
                    return
                break
            if item['����'] not in box['��������'].splitlines():
                continue
            if item.checkAttr('�����ۼӼ�', '��������'):
                continue
            if item.inUse:
                continue
            ob.remove(item)
            box.insert(item)
            if item.isOneItem():
                ONEITEM.keep(item.index, ob['�̸�'] + ' %s' % box['�̸�'])
            nc = 0
            try:
                nc = nCnt[item['�̸�']]
            except:
                nCnt[item['�̸�']] = 0
            nCnt[item['�̸�']] = nc + 1
            c += 1
            if c == count:
                break
        if c == 0:
            ob.sendLine('�� ���̻� ������ ������ �����. ^^')
            return
        else:
            msg = ''
            for name in nCnt:
                nc = nCnt[name]
                if nc == 1:
                    ob.sendLine('����� %s�� [36m%s[37m%s �����մϴ�.' % (box.getNameA(), name, han_obj(name)))
                    msg += '%s %s�� [36m%s[37m%s �����մϴ�.\r\n' % (ob.han_iga(), box.getNameA(), name, han_obj(name))
                else:
                    ob.sendLine('����� %s�� [36m%s[37m %d���� �����մϴ�.' % (box.getNameA(), name, nc))
                    msg += '%s %s�� [36m%s[37m %d���� �����մϴ�.\r\n' % (ob.han_iga(), box.getNameA(), name, nc)
            ob.sendRoom(msg[:-2])
        box.save()
        
