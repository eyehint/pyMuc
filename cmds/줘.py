# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        words = line.split()
        if len(words) < 2:
            ob.sendLine('�� ����: [���] [��ǰ] �ִ�')
            return
        if words[1] == '����':
            obj = ob.env.findObjName(words[0])
            if obj == None or is_player(obj) == False:
                ob.sendLine('�� ��ǰ�� �ǳ��� �������� ã�� �� �����. ^^')
                return
            if len(words) < 3:
                cnt = 1
            else:
                cnt = getInt(words[2])
                if cnt <= 0:
                    cnt = 1
            if ob['����'] == 0:
                ob.sendLine('�� ���� ���ڶ�׿�. ^^')
                return
            if ob['����'] < cnt:
                cnt = ob['����']
            ob['����'] -= cnt
            obj['����'] += cnt
            ob.sendLine('����� %s���� ���� %d���� �ݴϴ�.' % (obj.getNameA(), cnt))
            obj.sendLine('\r\n%s ��ſ��� ���� %d���� �ݴϴ�.' % (ob.han_iga(), cnt))
            obj.lpPrompt()
            ob.sendRoom('%s %s���� ���� %d���� �ݴϴ�.' % (ob.han_iga(), obj.getNameA(), cnt), ex = obj)
            return
        if words[1] == '����':
            obj = ob.env.findObjName(words[0])
            if obj == None or is_player(obj) == False:
                ob.sendLine('�� ��ǰ�� �ǳ��� �������� ã�� �� �����. ^^')
                return
            if len(words) < 3:
                cnt = 1
            else:
                cnt = getInt(words[2])
                if cnt <= 0:
                    cnt = 1
            if ob['����'] == '':
                ob['����'] = 0
            if ob['����'] == 0:
                ob.sendLine('�� ���� ���ڶ�׿�. ^^')
                return
            if ob['����'] < cnt:
                cnt = ob['����']
            ob['����'] -= cnt
            if obj['����'] == '':
                obj['����'] = 0
          
            obj['����'] += cnt
            ob.sendLine('����� %s���� ���� %d���� �ݴϴ�.' % (obj.getNameA(), cnt))
            obj.sendLine('\r\n%s ��ſ��� ���� %d���� �ݴϴ�.' % (ob.han_iga(), cnt))
            obj.lpPrompt()
            ob.sendRoom('%s %s���� ���� %d���� �ݴϴ�.' % (ob.han_iga(), obj.getNameA(), cnt), ex = obj)
            return
        name = words[1]
        
        order = getInt(name)
        if order != 0:
            for i in range( len(name) ):
                if name[i].isdigit() == False:
                    name = name[i:]
                    break
        else:
            order = 1
        #print order, name
        
        obj = ob.findObjName(name, order)
        if obj == None:
            ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            return
        name = obj['�̸�']
        target = ob.env.findObjName(words[0])
        if target == None or not is_player(target):
            ob.sendLine('�� ��ǰ�� �ǳ��� �������� ã�� �� �����. ^^')
            return
        if target == ob:
            ob.sendLine('����� [36m' + obj['�̸�'] + '[37m' + han_obj(obj['�̸�']) + ' ������ �峭�մϴ�. \'@_@\'')
            return
        i = 1
        c = 0
        if len(words) >= 3:
            i = getInt(words[2])
        if i < 1:
            i = 1
        if i > 50:
            i = 50
        if order != 1:
            i = 1
        objs = copy.copy(ob.objs)
        n = 0
        for obj in objs:
            if c >= i:
                break
            if not(name == obj.get('�̸�') or name in obj['�����̸�']):
                continue
            if obj.checkAttr('�����ۼӼ�', '��¾���'):
                continue
            if obj.inUse:
                continue
            n += 1
            if n < order:
                continue
            if obj.checkAttr('�����ۼӼ�', '�ټ�����'):
                if c == 0:
                    ob.sendLine('�� �� ������ �� �� �����. ^^')
                    return
                continue
            if target.getItemWeight() + obj['����'] > target.getStr() * 10:
                if c == 0:
                    ob.sendLine('[1m' + target['�̸�'] + '[0;37m' + han_iga(target['�̸�']) + \
                        ' ���ſ��� ���� ���մϴ�.')
                    target.sendLine('\r\n[1m' + ob['�̸�'] + '[0;37m' + han_iga(ob['�̸�']) + ' �ٷ��� ' + 
                        '[36m' + obj['�̸�'] + '[37m' + han_obj(obj['�̸�']) + ' ���ſ��� ���� ���մϴ�.')
                    target.lpPrompt()
                    return
                break
            if target.getItemCount() >= getInt(MAIN_CONFIG['����ھ����۰���']):
                if c == 0:
                    ob.sendLine('[1m' + target['�̸�'] + '[0;37m' + han_iga(target['�̸�']) + \
                        ' ���� �Ѱ�� ���� ���մϴ�.')
                    target.sendLine('\r\n[1m' + ob['�̸�'] + '[0;37m' + han_iga(ob['�̸�']) + ' �ٷ��� ' + \
                        '[36m' + obj['�̸�'] + '[37m' + han_obj(obj['�̸�']) + ' ���� �Ѱ�� ���� ���մϴ�.')
                    target.lpPrompt()
                    return
                break
            c += 1
            ob.remove(obj)
            target.insert(obj)
            if obj.isOneItem():
                ONEITEM.have(obj.index, target['�̸�'])

        if c == 0:
            ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
        elif c == 1:
            ob.sendLine('����� [1m' + target['�̸�'] + '[0;37m���� [36m' + name + '[37m' + han_obj(name) + ' �ݴϴ�.')
            target.sendLine('\r\n[1m' + ob['�̸�'] + '[0;37m' + han_iga(ob['�̸�']) + ' ��ſ��� [36m' + name + '[37m' + han_obj(name) + ' �ݴϴ�.')
            ob.sendRoom('%s %s���� [36m%s[37m%s �ݴϴ�.' % ( ob.han_iga(), target.getNameA(), name, han_obj(name)), ex = target)
            target.lpPrompt()
        else:
            ob.sendLine('����� [1m' + target['�̸�'] + '[0;37m���� [36m' + name + '[37m' + ' %d���� �ݴϴ�.' % c)
            target.sendLine('\r\n[1m' + ob['�̸�'] + '[0;37m' + han_iga(ob['�̸�']) + ' ��ſ��� [36m' + name + '[37m' + ' %d���� �ݴϴ�.' % c)
            target.lpPrompt()
            ob.sendRoom('%s %s���� [36m%s[37m %d���� �ݴϴ�.' % ( ob.han_iga(), target.getNameA(), name, c), ex = target)


