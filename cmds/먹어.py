# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('�� ����: [������ �̸�] �Ծ�')
            return
        if ob.act == ACT_REST:
            ob.sendLine('�� ���� �� �ִ� ��Ȳ�� �ƴϳ׿�. ^_^')
            return
        name, order = getNameOrder(line)
        item = ob.findObjInven(name, order)
        if item == None:
            ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            return
        if item['����'] != '�Դ°�':
            ob.sendLine('�� ���� �� �ִ°��� �ƴϿ���. ^_^')
            return
        
        maxHp = ob.getMaxHp()
        maxMp = ob.getMaxMp()
        
        hp = getInt(item['ü��'])
        mp = getInt(item['����'])
        if ob['ü��'] + hp > maxHp:
            ob['ü��'] = maxHp
        else:
            ob['ü��'] += hp
        if ob['����'] + mp > maxMp:
            ob['����'] = maxMp
        else:
            ob['����'] += mp
        
        maxmp = getInt(item['��������'])
        if maxmp != 0:
            if item.checkAttr('�����ۼӼ�', '�����������') == False:
                if ob.checkAttr('�������������۸���Ʈ', item['�̸�']):
                    maxmp = 0
                else:
                    ob.setAttr('�������������۸���Ʈ', item['�̸�'])
                    ob['�ְ���'] += maxmp
            else:
                ob['�ְ���'] += maxmp
        msg = item['��뽺ũ��']
        msg = msg.replace('$������$', item.getNameA())
        ob.remove(item)
        del item
        ob.sendLine('����� %s' % msg)
        
        roomMsg = '%s %s' % ( ob.han_iga(), msg)
        if maxmp > 0:
            ob.sendLine('\r\n[1m����� ������ ȸ������ ����ġ�� �������� �Ͼ� ���Ⱑ �ɵ��ϴ�.[0;37m ([1;36m+%d[0;37m)' % maxmp)
            roomMsg += '\r\n\r\n[1m%s�� ������ ȸ������ ����ġ�� �������� �Ͼ� ���Ⱑ �ɵ��ϴ�.[0;37m ([1;36m+%d[0;37m)' % (ob.getNameA() ,maxmp)
        elif maxmp < 0:
            ob.sendLine('\r\n[1m����� ������ ���� �䵿�� �Ͼ�� ������ �������� �����մϴ�.[0;37m ([1;31m%d[0;37m)' % maxmp)
            roomMsg += '\r\n\r\n[1m%s�� ������ ���� �䵿�� �Ͼ�� ������ �������� �����մϴ�.[0;37m ([1;31m%d[0;37m)' % (ob.getNameA() ,maxmp)
        ob.sendFightScriptRoom(roomMsg)

        if '���Ӻ���' not in ob.alias:
            return
        if ob.alias['���Ӻ���'] != '�ѱ�':
            return
        if hp == 0:
            return
        if 'ü��' not in ob.alias or 'ü�¾�' not in ob.alias:
            return
        if ob.getHp() < getInt(ob.alias['ü��']):
            #print ob.getHp()
            ob.do_command('%s �Ծ�' % line)
