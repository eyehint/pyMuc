# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    #level = 1000
    def cmd(self, ob, line):
    #    if getInt(ob['�����ڵ��']) < 1000:
    #        ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
    #        return
        if len(line) == 0:
            ob.sendLine('�� ����: [��ǰ�̸�] �Ұ�')
            return
        i = 1
        c = 0
        
        args = line.split()
        if len(args) >= 2:
            i = getInt(args[1])
        if i < 1:
            i = 1
        if i > 100:
            i = 100
        name = args[0]
        order = getInt(name)
        if order != 0:
            for i in range( len(name) ):
                if name[i].isdigit() == False:
                    name = name[i:]
                    break
        else:
            order = 1
        if order != 1:
            i = 1
        objs = copy.copy(ob.objs)
        n = 0
        for obj in objs:
            if c >= i:
                break
            if name != obj.get('�̸�') and name not in obj.get('�����̸�').splitlines():
                continue

            if obj.inUse:
                continue
            
            n += 1
            if n < order:
                continue

            c += 1
            name = obj['�̸�']
            ob.remove(obj)
            if obj.isOneItem():
                ONEITEM.destroy(obj.index)
        if c == 0:
            ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
        elif c == 1:
            ob.sendLine('����� [36m%s[37m%s �Ұ��ع����ϴ�.' % (name, han_obj(name)))
            ob.sendRoom('%s [36m%s[37m%s �Ұ��ع����ϴ�.' % (ob.han_iga(), name, han_obj(name)))
        else:
            ob.sendLine('����� [36m%s[37m %d���� �Ұ��ع����ϴ�.' % (name, c))
            ob.sendRoom('%s [36m%s[37m %d���� �Ұ��ع����ϴ�.' % (ob.han_iga(), name, c))
