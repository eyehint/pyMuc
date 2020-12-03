# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('�� ����: [�̸�] ����')
            return
        found = False
        doctor = False
        for mob in ob.env.objs:
            if is_mob(mob) == False:
                continue
            if '�ǿ�' in mob['�����̸�'].splitlines():
                doctor = True
                key = '���� %s' % line
                if key in mob.attr:
                    found = True
                    break
        if doctor == False:
            ob.sendLine('�� �̰��� ���� �����Ҹ��� �ǿ��� �����. ^^')
            return
        if found == False:
            ob.sendLine('�� �׷��� ���� ������ �ǿ��� �����. ^^')
            return
        take = []
        for l in mob[key].splitlines():
            words = l.split()
            if len(words) < 2:
                continue
            if words[0][0] == '+':
                give = words[0][1:]
                ngive = int(words[1])
            else:
                take.append( (words[0] , int(words[1])) )
        indexs = []
        for obj in ob.objs:
            if obj.inUse:
                continue
            indexs.append(obj.index)
        
        for i in take:
            c = 0
            for j in range(0, i[1]):
                if i[0] in indexs:
                    c += 1
                    indexs.remove(i[0])
                    continue
                break
            if c != i[1]:
                ob.sendLine('%s ���մϴ�. "��.. �����Ѱ� �ִٳ�... ��Ḧ �� ���ؿ��Գ�"' % mob.han_iga())
                return
        msg = ''
        items = []
        for i in range(0, ngive):
            item = getItem(give)
            if item == None:
                ob.sendLine('%s ���մϴ�. "��.. ��ᰡ �� �������� �ѵ��� ������ ����ھ�..."' % mob.han_iga())
                return
            item = item.clone()
            items.append(item)
            msg += '%s ��ſ��� %s �ݴϴ�.' % (mob.han_iga(), item.han_obj())
        ob.sendLine('����� %s���� [36m%s[37m%s ����� �ִ� ������ �ǳ��ݴϴ�.' % ( mob.getNameA(), line, han_obj(line)))
        ob.sendLine('%s ������ ������ �ɿ��� �⸦ �Ҿ� ������ �۾��մϴ�.'% mob.han_iga())
        ob.sendLine(msg)
        objs = copy.copy(ob.objs)
        for i in take:
            c = 0
            for j in range(0, i[1]):
                self.delItem(ob, i[0]) 
        for i in items:
            ob.insert(i)

    def delItem(self, ob, index):
        for obj in ob.objs:
            if obj.inUse:
                continue
            if obj.index == index:
                ob.objs.remove(obj)
                return
