# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('�� ����: [��ǰ�̸�] [����] ����')
            return
        words = line.split()
        count = 1
        if len(words) >= 2:
            count = getInt(words[1])
            if count <= 0:
                count = 1
            if count > 50:
                count = 50
        found = False
        mob = ob.env.findMerchant()
        if mob == None:
            ob.sendLine('�� ǰ���� ������ ������ �����. ^^')
            return
        item = None
        for l in mob['�����Ǹ�'].splitlines():
            w = l.split()
            index = w[0]
            percent = int(w[1])
            item = getItem(index)
            if item == None:
                continue
            if item['�̸�'] == words[0] or words[0] in item['�����̸�'].splitlines():
                found = True
                break
        if found == False:
            ob.sendLine('�� �׷� ������ ���� �ʾƿ�. ^_^')
            return
        if item['����'] == 'ȣ��':
            self.buyGuardMob(ob, item)
            return
        c = 0
        p = getInt(item['�ǸŰ���']) * 100 / percent
        for i in range(count):
            if ob.getItemCount() >= getInt(MAIN_CONFIG['����ھ����۰���']):
                if c == 0:
                    ob.sendLine('�� �ڳװ� ���� ��ǰ�� �Ѱ���')
                    return
                break
            if ob.getItemWeight() + item['����'] > ob.getStr() * 10:
                if c == 0:
                    ob.sendLine('�� ���ſ��� �� �̻� ���� �� �����. ^^')
                    return
                break
            money = ob['����']
            if money < p:
                if c == 0:
                    ob.sendLine('�� ���� ���ڶ�׿�. ^^')
                    return
                break
            money -= p
            ob['����'] = money
            c += 1
            obj = copy.deepcopy(item)
            ob.insert(obj)
        if c == 0:
            ob.sendLine('�� ���ſ��� �� �̻� ���� �� �����. ^^')
        else:
            ob.sendLine('����� %s %d���� ���� %d���� �����մϴ�.' % ( item.getNameA(), c, c * p))
            ob.sendRoom('%s %s %d���� ���� %d���� �����մϴ�.' % (ob.han_iga(), item.getNameA(), c, c * p))
            
    def buyGuardMob(self, ob, item):
        chI = ob['����']
        chU = item['���żӼ�']
        if chI != '����' and chI != '����':
            if chU == '����' and chI != chU:
                ob.sendLine('�� �ش� ȣ���� ���Ŀ��� ��� �����մϴ�.')
                return
            if chU == '����' and chI != chU:
                ob.sendLine('�� �ش� ȣ���� ���Ŀ��� ��� �����մϴ�.')
                return
        lines = item['��������'].splitlines()
        if len(lines) == 0:
            ob.sendLine('�� �ش� ȣ���� ����� �����ϴ�.')
            return
            
        #���ŷ���
        maxLv = 0
        count = 0
        for obj in ob.objs:
            if obj['����'] == 'ȣ��':
                if obj['�̸�'] == item['�̸�']:
                    count += 1
                lv = obj['���ŷ���']
                if lv > maxLv:
                    maxLv = lv
        if item['���ŷ���'] < maxLv:
            ob.sendLine('�� �ش� ȣ���� ����� �����ϴ�.(����)')
            return
        limit = 0
        for attr in item['�����ۼӼ�'].splitlines():
            if attr.find('�����Ѱ�') == 0:
                limit = getInt(attr.split()[1])
                break
        
        if count >= limit:
            ob.sendLine('�� �ش� ȣ���� ����� �����ϴ�.(������������)')
            return
            
        match = False
        for line in lines:
            words = line.split()
            l = len(words)
            if l == 2:
                if words[0] == '����':
                    n = self.getHurbNum(ob)
                else:
                    n = self.getGuardNum(ob, words[0])
                if n < int(words[1]):
                    continue
                gName = words[0]
                nNum = int(words[1])
                match = True
                break
            elif l == 3:
                n = self.getGuardNum(ob, words[0])
                if n < 1:
                    continue
                n = self.getHurbNum(ob)
                if n < int(words[2]):
                    continue
                match = True
                gName = words[1]
                nNum = int(words[2])
                break
            else:
                continue
        if match == False:
            ob.sendLine('�� �ش� ȣ���� ����� �����ϴ�.')
            return
        if gName == '����':
            self.delHerb(ob, nNum)
        else:
            n = 0
            objs = copy.copy(ob.objs)
            for obj in objs:
                if obj['�̸�'] == gName:
                    ob.remove(obj)
                    n += 1
                    if n == nNum:
                        break
                        
        g = item.clone()
        g.hp = g['ü��']
        ob.insert(g)
        
        ob.sendLine('����� %s �����մϴ�.' % item.han_obj())
        ob.sendRoom('%s %s �����մϴ�.' % (ob.han_iga(), item.han_obj()))
        #ob.sendLine('�� ���� ȣ���� �� �� �����^^;;')
        
    def getGuardNum(self, ob, name):
        n = 0
        for obj in ob.objs:
            if obj['�̸�'] == name:
                n += 1
        return n
        
    def delHerb(self, ob, c):
        n = 0
        herbs = ['�ռ�1', '�ռ�2', '�ռ�3', '�ռ�4', '�ռ�5', '�ռ�6', '�ռ�7', '�ռ�8', '�ռ�9']
        objs = copy.copy(ob.objs)
        for obj in objs:
            if obj.index in herbs:
                n += 1
                ob.remove(obj)
                if c == n:
                    break
        
    def getHurbNum(self, ob):
        n = 0
        herbs = ['�ռ�1', '�ռ�2', '�ռ�3', '�ռ�4', '�ռ�5', '�ռ�6', '�ռ�7', '�ռ�8', '�ռ�9']
        for obj in ob.objs:
            if obj.index in herbs:
                n += 1
        return n
