# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('�� ����: [������ �̸�] �ֿ�')
            return

        if line == '���' or line == '����':
            cnt = 0
            nCnt = {}
            objs = copy.copy(ob.env.objs)
            for obj in objs:
                if is_item(obj) == False:
                    continue
                if ob.getItemWeight() + obj['����'] > ob.getStr() * 10:
                    continue
                if ob.getItemCount() > getInt(MAIN_CONFIG['����ھ����۰���']):
                    break
                ob.env.remove(obj)
                if obj.isOneItem():
                    ONEITEM.have(obj.index, ob['�̸�'])
                ob.insert(obj)
                nc = 0
                try:
                    nc = nCnt[obj.get('�̸�')]
                except:
                    nCnt[obj.get('�̸�')] = 0
                nCnt[obj.get('�̸�')] = nc + 1
                cnt = cnt + 1
            if cnt == 0:
                ob.sendLine('�� ���̻� ���� ������ ���ٳ�')
                return
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('����� [36m' + name + '[37m' + han_obj(name) + ' ��� ǰ�ӿ� ������ �մϴ�.')
                        msg += '%s [36m%s[37m%s ��� ǰ�ӿ� ������ �մϴ�.\r\n' % (ob.han_iga(), name, han_obj(name))
                    else:
                        ob.sendLine('����� [36m' + name + '[37m %d���� ��� ǰ�ӿ� ������ �մϴ�.' % nc)
                        msg += '%s [36m%s[37m %d���� ��� ǰ�ӿ� ������ �մϴ�.\r\n' % (ob.han_iga(), name, nc)
                ob.sendRoom(msg[:-2])
        else:
            i = 1
            c = 0
            nCnt = {}
            args = line.split()
            if len(args) >= 2:
                i = getInt(args[1])
            if i < 1:
                i = 0
            if i > 100:
                i = 50
            for j in range(i):
                obj = ob.env.findObjName(args[0])
                if obj == None:
                    break
                if is_item(obj) == False:
                    ob.sendLine('�� ��ȣ�� �׷� ������ �������� �ʴ´ٳ�')
                    return
                if ob.getItemWeight() + obj['����'] > ob.getStr() * 10:
                    if c == 0:
                        ob.sendLine('�� �ڳ��� �����δ� ���̻� ���� �� ���ٳ�')
                        return
                    break
                if ob.getItemCount() > getInt(MAIN_CONFIG['����ھ����۰���']):
                    if c == 0:
                        ob.sendLine('�� �ڳװ� ���� ��ǰ�� �Ѱ���')
                        return
                    break
                c += 1
                ob.env.remove(obj)
                if obj.isOneItem():
                    ONEITEM.have(obj.index, ob['�̸�'])
                ob.insert(obj)
                nc = 0
                try:
                    nc = nCnt[obj.get('�̸�')]
                except:
                    nCnt[obj.get('�̸�')] = 0
                nCnt[obj.get('�̸�')] = nc + 1
                #ob.sendLine('����� [36m' + obj.get('�̸�') + '[37m' + han_obj(obj.get('�̸�')) + ' ��� ǰ�ӿ� ������ �մϴ�.')
            if c == 0:
                ob.sendLine('�� ��ȣ�� �׷� ������ �������� �ʴ´ٳ�')
                return
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('����� [36m' + name + '[37m' + han_obj(name) + ' ��� ǰ�ӿ� ������ �մϴ�.')
                        msg += '%s [36m%s[37m%s ��� ǰ�ӿ� ������ �մϴ�.\r\n' % (ob.han_iga(), name, han_obj(name))
                    else:
                        ob.sendLine('����� [36m' + name + '[37m %d���� ��� ǰ�ӿ� ������ �մϴ�.' % nc)
                        msg += '%s [36m%s[37m %d���� ��� ǰ�ӿ� ������ �մϴ�.\r\n' % (ob.han_iga(), name, nc)
                ob.sendRoom(msg[:-2])

