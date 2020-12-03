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
                #ob.objs.remove(ob.objs[i])
                #obj.move_object(ob.env)
                if obj.inUse:
                    continue
                if obj.get('����') != '��' and obj.get('����') != '����':
                    continue
                if ob.checkArmed(obj.get('����')):
                    continue
                if obj.checkAttr('�����ۼӼ�', '�ü�õ����'):
                    if self.checkSuk(ob, 1000) == False:
                        continue
                if obj.checkAttr('�����ۼӼ�', '�ü���õ����'):
                    if self.checkSuk(ob, 2000) == False:
                        continue
                ob.armor += getInt(obj['����'])
                ob.attpower += getInt(obj['���ݷ�'])
                option = obj.getOption()
                if option != None:
                    for op in option:
                        if op == '��':
                            ob._str += option[op]
                        elif op == '��ø��':
                            ob._dex += option[op]
                        elif op == '����':
                            ob._arm += option[op]
                        elif op == 'ü��':
                            ob._maxhp += option[op]
                        elif op == '����':
                            ob._maxmp += option[op]
                        elif op == '�ʻ�':
                            ob._critical += option[op]
                        elif op == '��':
                            ob._criticalChance += option[op]
                        elif op == 'ȸ��':
                            ob._miss += option[op]
                        elif op == '����':
                            ob._hit += option[op]
                        elif op == '����ġ':
                            ob._exp += option[op]
                        elif op == '�����߰�':
                            ob._magicChance += option[op]

                if obj['����'] == '����':
                    ob.weaponItem = obj
                s = obj.getUseScript()
                if s == '':
                    ob.sendLine('����� [36m' + obj.get('�̸�') + '[37m' + han_obj(obj.get('�̸�')) + ' �����մϴ�.')
                    #ob.sendRoom('%s %s �����մϴ�.' % (ob.han_iga(), obj.han_obj()))
                    msg += '%s %s �����մϴ�.\r\n' % (ob.han_iga(), obj.han_obj())
                else:
                    ob.sendLine('����� ' + s)
                    #ob.sendRoom('%s %s' % (ob.han_iga(),s))
                    msg += '%s %s\r\n' % (ob.han_iga(),s)
                    
                obj.inUse = True
                cnt = cnt + 1
                   
            if cnt == 0:
                ob.sendLine('�� ���̻� ������ ��� �����.')
            else:
                ob.sendRoom(msg[:-2])
        else:
            name, order = getNameOrder(line)
            item = ob.findObjInven(name, order)
            if item == None or item.inUse:
                ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
                return

            if item.get('����') != '��' and item.get('����') != '����':
                ob.sendLine('�� ������ �� �ִ°��� �ƴϿ���.')
                return
                
            if item.checkAttr('�����ۼӼ�', '�ü�õ����'):
                if self.checkSuk(ob, 1000) == False:
                    ob.sendLine('�� ����� �ɷ����δ� ������ �Ұ����ؿ�.')
                    return

            if item.checkAttr('�����ۼӼ�', '�ü���õ����'):
                if self.checkSuk(ob, 2000) == False:
                    ob.sendLine('�� ����� �ɷ����δ� ������ �Ұ����ؿ�.')
                    return
    
            # check if already wear same place
            if ob.checkArmed(item.get('����')):
                ob.sendLine('�� �� �̻� ������ �Ұ����ؿ�.')
                return
            item.inUse = True
            ob.armor += getInt(item['����'])
            ob.attpower += getInt(item['���ݷ�'])
            option = item.getOption()
            if option != None:
                for op in option:
                    if op == '��':
                        ob._str += option[op]
                    elif op == '��ø��':
                        ob._dex += option[op]
                    elif op == '����':
                        ob._arm += option[op]
                    elif op == 'ü��':
                        ob._maxhp += option[op]
                    elif op == '����':
                        ob._maxmp += option[op]
                    elif op == '�ʻ�':
                        ob._critical += option[op]
                    elif op == '��':
                        ob._criticalChance += option[op]
                    elif op == 'ȸ��':
                        ob._miss += option[op]
                    elif op == '����':
                        ob._hit += option[op]
                    elif op == '����ġ':
                        ob._exp += option[op]
                    elif op == '�����߰�':
                        ob._magicChance += option[op]
            if item['����'] == '����':
                ob.weaponItem = item
            s = item.getUseScript()
            if s == '':
                ob.sendLine('����� [36m' + item.get('�̸�') + '[37m' + han_obj(item.get('�̸�')) + ' �����մϴ�.')
                ob.sendRoom('%s %s �����մϴ�.' % (ob.han_iga(), item.han_obj()))
            else:
                ob.sendLine('����� ' + s)
                ob.sendRoom('%s %s' % (ob.han_iga(),s))
            return
        

    def checkSuk(self, ob, min):
        if ob['1 ���õ�'] >= min and ob['2 ���õ�'] >= min and ob['3 ���õ�'] >= min and ob['4 ���õ�'] >= min and ob['5 ���õ�'] >= min:
            return True
        return False
