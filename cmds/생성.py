# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if len(line) == 0:
            ob.sendLine('����: [������ �̸�] [����] ����')
            return
        var = line.split()
        if len(var) == 1:
            cnt = 1
        else:
            cnt = int(var[1])

        item = getItem(var[0])

        if item == None:
            ob.sendLine('* ���� ����!!!')
            return
            
        if item.isOneItem():
            if item.isOneThere():
                ob.sendLine('[���Ͼ�����] %s �̹� �����Ǿ� �ֽ��ϴ�.' % item.han_iga())
                return
            else:
                ONEITEM.have(item.index, ob['�̸�'])
        for i in range(cnt):
            item = item.deepclone()
            ob.objs.append(item)
            if item['����'] == 'ȣ��':
                item.hp = item['ü��']
        
        ob.sendLine('[1;32m* [' + item.get('�̸�') + '] ���� �Ǿ����ϴ�.[0;37m')
