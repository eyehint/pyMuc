# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        words = line.split()
        if len(line) == 0 or len(words) < 2:
            ob.sendLine('�� ����: [�������̸�] [��ǰ] ����')
            return
        box = ob.env.findObjName(words[0])
        if box == None or is_box(box) == False:
            ob.sendLine('�� ����� �ȱ����δ� �׷����� ���� ���ٳ�')
            return
            
        if words[1] == '���':
            objs = copy.copy(box.objs)
            c = 0
            nCnt = {}
            for item in objs:
                if ob.getItemWeight() + item['����'] > ob.getStr() * 10:
                    if c == 0:
                        ob.sendLine('�� �ڳ��� �����δ� ���̻� ���� �� ���ٳ�')
                        return
                    break
                if ob.getItemCount() > getInt(MAIN_CONFIG['����ھ����۰���']):
                    if c == 0:
                        ob.sendLine('�� �ڳװ� ���� ��ǰ�� �Ѱ���')
                        return
                    break
                box.remove(item)
                ob.insert(item)
                if item.isOneItem():
                    ONEITEM.have(item.index, ob['�̸�'])
                nc = 0
                try:
                    nc = nCnt[item['�̸�']]
                except:
                    nCnt[item['�̸�']] = 0
                nCnt[item['�̸�']] = nc + 1
                c += 1
            if c == 0:
                ob.sendLine('�� �� �̻� ���� ������ �����. ^^')
                return
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('����� %s���� [36m%s[37m%s �����ϴ�.' % (box.getNameA(), name, han_obj(name)))
                        msg += '%s %s���� [36m%s[37m%s �����ϴ�.\r\n' % (ob.han_iga(), box.getNameA(), name, han_obj(name))
                    else:
                        ob.sendLine('����� %s���� [36m%s[37m %d���� �����ϴ�.' % (box.getNameA(), name, nc))
                        msg += '%s %s���� [36m%s[37m %d���� �����ϴ�.\r\n' % (ob.han_iga(), box.getNameA(), name, nc)
                ob.sendRoom(msg[:-2])
            box.save()
            return
        if words[1] == '����':
            objs = copy.copy(box.objs)
            c = 0
            nCnt = {}
            for item in objs:
                if item['�����̸�'] != '����':
                    continue
                if ob.getItemWeight() + item['����'] > ob.getStr() * 10:
                    if c == 0:
                        ob.sendLine('�� �ڳ��� �����δ� ���̻� ���� �� ���ٳ�')
                        return
                    break
                if ob.getItemCount() > getInt(MAIN_CONFIG['����ھ����۰���']):
                    if c == 0:
                        ob.sendLine('�� �ڳװ� ���� ��ǰ�� �Ѱ���')
                        return
                    break
                box.remove(item)
                ob.insert(item)
                if item.isOneItem():
                    ONEITEM.have(item.index, ob['�̸�'])
                nc = 0
                try:
                    nc = nCnt[item['�̸�']]
                except:
                    nCnt[item['�̸�']] = 0
                nCnt[item['�̸�']] = nc + 1
                c += 1
            if c == 0:
                ob.sendLine('�� �� �̻� ���� ������ �����. ^^')
                return
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('����� %s���� [36m%s[37m%s �����ϴ�.' % (box.getNameA(), name, han_obj(name)))
                        msg += '%s %s���� [36m%s[37m%s �����ϴ�.\r\n' % (ob.han_iga(), box.getNameA(), name, han_obj(name))
                    else:
                        ob.sendLine('����� %s���� [36m%s[37m %d���� �����ϴ�.' % (box.getNameA(), name, nc))
                        msg += '%s %s���� [36m%s[37m %d���� �����ϴ�.\r\n' % (ob.han_iga(), box.getNameA(), name, nc)
                ob.sendRoom(msg[:-2])
            box.save()
            return

        count = 1
        if len(words) > 2:
            count = getInt(words[2])
        item = None 
        order = -1
        if words[1].isdigit():
            idx = getInt(words[1])
            if len(box.objs) - idx >= 0:
                item = box.objs[idx - 1]
                order = 0
                name = item['�̸�']
        if item == None: 
            item = box.findObjName(words[1])
        if item == None:
            name, order = getNameOrder(words[1])
            item = box.findObjInven(name, order) 
            if item == None:
                ob.sendLine('�� �׷� ������ �����. ^^')
                return
            count = 1
        
        if order != -1 and item != None:
            if ob.getItemWeight() + item['����'] > ob.getStr() * 10:
                ob.sendLine('�� �ڳ��� �����δ� ���̻� ���� �� ���ٳ�')
                return
            if ob.getItemCount() > getInt(MAIN_CONFIG['����ھ����۰���']):
                ob.sendLine('�� �ڳװ� ���� ��ǰ�� �Ѱ���')
                return
            box.remove(item)
            ob.insert(item)
            if item.isOneItem():
                ONEITEM.have(item.index, ob['�̸�'])
            ob.sendLine('����� %s���� [36m%s[37m%s �����ϴ�.' % (box.getNameA(), item['�̸�'], han_obj(name)))
            msg = '%s %s���� [36m%s[37m%s �����ϴ�.\r\n' % (ob.han_iga(), box.getNameA(), item['�̸�'], han_obj(name))
            ob.sendRoom(msg[:-2])
            box.save()
            return

        objs = copy.copy(box.objs)
        c = 0
        nCnt = {}
        for item in objs:
            if words[1] != item['�̸�'] and words[1] not in item['�����̸�'].splitlines():
                continue
            if ob.getItemWeight() + item['����'] > ob.getStr() * 10:
                if c == 0:
                    ob.sendLine('�� �ڳ��� �����δ� ���̻� ���� �� ���ٳ�')
                    return
                break
            if ob.getItemCount() > getInt(MAIN_CONFIG['����ھ����۰���']):
                if c == 0:
                    ob.sendLine('�� �ڳװ� ���� ��ǰ�� �Ѱ���')
                    return
                break
            box.remove(item)
            ob.insert(item)
            if item.isOneItem():
                ONEITEM.have(item.index, ob['�̸�'])
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
            ob.sendLine('�� ���̻� ���� ������ �����. ^^')
            return
        else:
            msg = ''
            for name in nCnt:
                nc = nCnt[name]
                if nc == 1:
                    ob.sendLine('����� %s���� [36m%s[37m%s �����ϴ�.' % (box.getNameA(), name, han_obj(name)))
                    msg += '%s %s���� [36m%s[37m%s �����ϴ�.\r\n' % (ob.han_iga(), box.getNameA(), name, han_obj(name))
                else:
                    ob.sendLine('����� %s���� [36m%s[37m %d���� �����ϴ�.' % (box.getNameA(), name, nc))
                    msg += '%s %s���� [36m%s[37m %d���� �����ϴ�.\r\n' % (ob.han_iga(), box.getNameA(), name, nc)
            ob.sendRoom(msg[:-2])
        box.save()
        
