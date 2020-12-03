# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('�� ����: [������ �̸�] ����')
            return
        
        if ob.env == None:
            ob.sendLine('�� �ƹ��͵� ������ �����ϴ�.')
            return
            
        if line.find('����') == 0:
            ob.sendLine('�� ������ ���� �� �����. ^^')
            return
            
        if line == '���' or line == '����':
            cnt = 0
            objs = copy.copy(ob.objs)
            nCnt = {}
            nFail = {}
            for obj in objs:
                if is_item(obj):
                    if obj.inUse:
                        continue
                    if obj.checkAttr('�����ۼӼ�', '����������'):
                        continue
                    if obj.checkAttr('�����ۼӼ�', '��¾���'):
                        continue
                    ob.remove(obj)
                    
                    cnt += 1
                    if ob.env.getItemCount() < 50:
                        ob.env.insert(obj)
                        obj.drop()
                        if obj.isOneItem():
                            ONEITEM.drop(obj.index, ob['�̸�'])
                        nc = 0
                        try:
                            nc = nCnt[obj.get('�̸�')]
                        except:
                            nCnt[obj.get('�̸�')] = 0
                        nCnt[obj.get('�̸�')] = nc + 1
                    else:
                        if obj.isOneItem():
                            ONEITEM.destroy(obj.index)
                        nc = 0
                        try:
                            nc = nFail[obj.get('�̸�')]
                        except:
                            nFail[obj.get('�̸�')] = 0
                        nFail[obj.get('�̸�')] = nc + 1
                        obj.env = None
                        del obj
            if cnt == 0:
                ob.sendLine('�� ���̻� ���� ������ ���ٳ�')
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('����� [36m' + name + '[37m' + han_obj(name) + ' �����ϴ�.')
                        msg += '%s [36m%s[37m%s �����ϴ�.\r\n' % (ob.han_iga(), name, han_obj(name))
                    else:
                        ob.sendLine('����� [36m' + name + '[37m %d���� �����ϴ�.' % nc)
                        msg += '%s [36m%s[37m %d���� �����ϴ�.\r\n' % (ob.han_iga(), name, nc)
                for name in nFail:
                    nc = nFail[name]
                    if nc == 1:
                        ob.sendLine('����� [36m' + name + '[37m' + han_obj(name) + ' ������ �ٷ� �μ����ϴ�.')
                        msg += '%s [36m%s[37m%s ������ �ٷ� �μ����ϴ�.\r\n' % (ob.han_iga(), name, han_obj(name))
                    else:
                        ob.sendLine('����� [36m' + name + '[37m %d���� ������ �ٷ� �μ����ϴ�.' % nc)
                        msg += '%s [36m%s[37m %d���� ������ �ٷ� �μ����ϴ�.\r\n' % (ob.han_iga(), name, nc)
                ob.sendRoom(msg[:-2])
        else:
            i = 1
            c = 0
            nCnt = {}
            nFail = {}
            
            args = line.split()
            if len(args) >= 2:
                i = getInt(args[1])
            if i < 1:
                i = 1
            if i > 50:
                i = 50
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
                if obj.checkAttr('�����ۼӼ�', '��¾���'):
                        continue
                if obj.inUse:
                    continue
                n += 1
                if n < order:
                    continue
                if obj.checkAttr('�����ۼӼ�', '����������'):
                    if c == 0:
                        ob.sendLine('�� �� ������ ���� �� �����. ^^')
                        return
                    continue
                c += 1
                ob.remove(obj)
                if ob.env.getItemCount() < 50:
                    ob.env.insert(obj)
                    obj.drop()
                    if obj.isOneItem():
                        ONEITEM.drop(obj.index, ob['�̸�'])
                    nc = 0
                    try:
                        nc = nCnt[obj.get('�̸�')]
                    except:
                        nCnt[obj.get('�̸�')] = 0
                    nCnt[obj.get('�̸�')] = nc + 1
                else:
                    if obj.isOneItem():
                        ONEITEM.destroy(obj.index)
                    nc = 0
                    try:
                        nc = nFail[obj.get('�̸�')]
                    except:
                        nFail[obj.get('�̸�')] = 0
                    nFail[obj.get('�̸�')] = nc + 1
                
                #ob.sendLine('����� ' + obj.get('�̸�') + han_obj(obj.get('�̸�')) + ' �����ϴ�.')
            if c == 0:
                ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('����� [36m' + name + '[37m' + han_obj(name) + ' �����ϴ�.')
                        msg += '%s [36m%s[37m%s �����ϴ�.\r\n' % (ob.han_iga(), name, han_obj(name))
                    else:
                        ob.sendLine('����� [36m' + name + '[37m %d���� �����ϴ�.' % nc)
                        msg += '%s [36m%s[37m %d���� �����ϴ�.\r\n' % (ob.han_iga(), name, nc)
                for name in nFail:
                    nc = nFail[name]
                    if nc == 1:
                        ob.sendLine('����� [36m' + name + '[37m' + han_obj(name) + ' ������ �ٷ� �μ����ϴ�.')
                        msg += '%s [36m%s[37m%s ������ �ٷ� �μ����ϴ�.\r\n' % (ob.han_iga(), name, han_obj(name))
                    else:
                        ob.sendLine('����� [36m' + name + '[37m %d���� ������ �ٷ� �μ����ϴ�.' % nc)
                        msg += '%s [36m%s[37m %d���� ������ �ٷ� �μ����ϴ�.\r\n' % (ob.han_iga(), name, nc)
                ob.sendRoom(msg[:-2])
