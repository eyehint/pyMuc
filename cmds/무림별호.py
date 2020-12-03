# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        line = line.strip()
        if len(line) == 0 or len(line.split()) > 1:
            ob.sendLine('�� ����: [��ȣ�̸�] ������ȣ')
            return
        
        if ob['������ȣ'] != '':
            ob.sendLine('�� �̹� ��ȣ�� ��������. ^^')
            return
            
        if ob.checkEvent('������ȣ����') == False:
            ob.sendLine('�� ������ ������ȣ�� ���� �� �����. ^^')
            return
        if len(line) < 3:
            ob.sendLine('�� ����Ͻ÷��� ��ȣ�� �ʹ� ª�ƿ�.')
            return
        if len(line) > 10:
            ob.sendLine('�� ����Ͻ÷��� ��ȣ�� �ʹ� ����.')
            return
            
        if line in NICKNAME.attr:
            ob.sendLine('�� �ٸ� �������� ������� ��ȣ�Դϴ�. ^^')
            return
        ob['������ȣ'] = line
        
        if ob.checkEvent('������ȣ ����'):
            ob['����'] = '����'
            buf = '[1m�� [[31m����[37m] '
        else:
            ob['����'] = '����'
            buf = '[1m�� [[32m����[37m] '
            
        NICKNAME[line] = ob['�̸�']
        NICKNAME.save()
        
        ob.delEvent('������ȣ����')
        ob.delEvent('������ȣ ����')
        ob.delEvent('������ȣ ����')
        
        msg = '[1m%s%s [1m�ڽ��� ��ȣ�� ��[33m%s[37m��%s Ī�ϱ� �����մϴ�.[0;37m' % ( buf, ob.han_iga(), line, han_uro(line))
        ob.channel.sendToAll(msg, ex = ob)
        ob.sendLine(msg + '\r\n')
        
        ob.makeHome()
        roomName = '����ڸ�:%s' % ob['�̸�']
        ob['��ȯ����'] = roomName
        ob.save()
        room = getRoom(roomName)
        if room == None:
            ob.sendLine('�� ����ڸ� ������ �����Ͽ����ϴ�.')
            return
        
        ob.enterRoom(room, '��ȯ', '��ȯ')
