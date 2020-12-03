# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('�� ����: [������ �̸�] ����')
            return
        msg = ''
        if line == '���' or line == '����':
            cnt = 0
            i = 0
            for obj in ob.objs:
                if obj.inUse:
                    obj.inUse = False
                    ob.armor -= getInt(obj['����'])
                    ob.attpower -= getInt(obj['���ݷ�'])
                    option = obj.getOption()
                    if option != None:
                        for op in option:
                            if op == '��':
                                ob._str -= option[op]
                            elif op == '��ø��':
                                ob._dex -= option[op]
                            elif op == '����':
                                ob._arm -= option[op]
                            elif op == 'ü��':
                                ob._maxhp -= option[op]
                            elif op == '����':
                                ob._maxmp -= option[op]
                            elif op == '�ʻ�':
                                ob._critical -= option[op]
                            elif op == '��':
                                 ob._criticalChance -= option[op]
                            elif op == 'ȸ��':
                                ob._miss -= option[op]
                            elif op == '����':
                                ob._hit -= option[op]
                            elif op == '����ġ':
                                ob._exp -= option[op]
                            elif op == '�����߰�':
                                ob._magicChance -= option[op]
                    if obj['����'] == '����':
                        ob.weaponItem = None
                    ob.sendLine('����� [36m' + obj.get('�̸�') + '[37m' + han_obj(obj.getStrip('�̸�')) + ' �������� �մϴ�.')
                    #ob.sendRoom('%s %s �������� �մϴ�.' % (ob.han_iga(), obj.han_obj()))
                    msg += '%s %s �������� �մϴ�.\r\n' % (ob.han_iga(), obj.han_obj())
                    cnt = cnt + 1
                   
            if cnt == 0:
                ob.sendLine('�� �������� ��� �����.')
                return
            else:
                ob.sendRoom(msg[:-2])
        else:
            item = ob.findObjInUse(line)

            if item == None:
                ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
                return
            if item.inUse == False:
                ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
                return

            item.inUse = False
            ob.armor -= getInt(item['����'])
            ob.attpower -= getInt(item['���ݷ�'])
            option = item.getOption()
            if option != None:
                for op in option:
                    if op == '��':
                        ob._str -= option[op]
                    elif op == '��ø��':
                        ob._dex -= option[op]
                    elif op == '����':
                        ob._arm -= option[op]
                    elif op == 'ü��':
                        ob._maxhp -= option[op]
                    elif op == '����':
                        ob._maxmp -= option[op]
                    elif op == '�ʻ�':
                        ob._critical -= option[op]
                    elif op == '��':
                         ob._criticalChance -= option[op]
                    elif op == 'ȸ��':
                        ob._miss -= option[op]
                    elif op == '����':
                        ob._hit -= option[op]
                    elif op == '����ġ':
                        ob._exp -= option[op]
                    elif op == '�����߰�':
                        ob._magicChance -= option[op]
            if item['����'] == '����':
                    ob.weaponItem = None
            ob.sendLine('����� [36m' + item.get('�̸�') + '[37m' + han_obj(item.getStrip('�̸�')) + ' �������� �մϴ�.')
            ob.sendRoom('%s %s �������� �մϴ�.' % (ob.han_iga(), item.han_obj()))

