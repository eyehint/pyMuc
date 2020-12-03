# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('�� ���� : [�����̸�] ���ǰɾ�')
            return
        if len(line) > 10 or len(line) < 2:
            ob.sendLine('�����̸��� �ʹ� ����!.')
            return
        if len(line) < 2:
            ob.sendLine('�����̸��� �ʹ� ª�ƿ�!.')
            return
        if ob.env.checkAttr('�����ڸ�') == False:
            ob.sendLine('�� �̰��� ������ �� �� �����ϴ�.')
            return
        if ob.env['��������'] != '':
            ob.sendLine('�� �̰��� ������ �� �� �����ϴ�.')
            return
        if ob['�Ҽ�'] != '':
            ob.sendLine('�� ����� ���ĸ� ���� �� �����ϴ�.')
            return
        if ob['���ı���'] != '':
            ob.sendLine('�� ����� ���ĸ� ���� �� �����ϴ�.')
            return
        if ob['����'] < 400:
            ob.sendLine('�� ����� ���ĸ� ���� �� �����ϴ�.')
            return
        if ob['����'] < MAIN_CONFIG['���ļ�������']:
            ob.sendLine('�� ���ĸ� ����µ��� ���� 10,000,000�� �̻��� �ʿ��մϴ�.')
            return
            
        for guild in GUILD.attr:
            if GUILD.attr[guild]['�̸�'] == line:
                ob.sendLine('�� �����ϴ� �����̸��Դϴ�.')
                return
        g = {}
        g['�̸�'] = line
        g['�����̸�'] = ob['�̸�']
        g['���Ŀ���'] = 1
        g['���ĸ�'] = ob.env.index
        g['���ָ�Ī'] = '����'
        g['�ι��ָ�Ī'] = '�ι���'
        g['��θ�Ī'] = '���'
        g['�����θ�Ī'] = '������'
        GUILD.attr[line] = g
        GUILD.save()
        ob['�Ҽ�'] = line
        ob['����'] = '����'
        ob.env['��������'] = line
        ob.env.save()
        for enter in ob.env['�����Ա�'].splitlines():
            if enter.find(':') == -1:
                path = ob.env.zone + ':' + enter
            else:
                path = enter
            room = getRoom(path)
            if room == None:
                continue
            room['��������'] = line
            room.save()
            
        item = getItem('������').clone()
        ob.insert(item)
        ob['����'] -= MAIN_CONFIG['���ļ�������']
        ob.sendLine('����� ������ ����µ� ���� %d���� ����մϴ�.' % MAIN_CONFIG['���ļ�������'])
        
        buf = MAIN_CONFIG['���Ļ����޼����Ӹ�']
        if ob['����'] == '����':
            buf += '[[1;32m%s[0;37m] [1;36m%s[37m%s ���� ��' % ( ob['������ȣ'], ob['�̸�'], han_iga(ob['�̸�']) )
        elif ob['����'] == '����':
            buf += '[[1;31m%s[0;37m] [1;36m%s[37m%s ���� ��' % ( ob['������ȣ'], ob['�̸�'], han_iga(ob['�̸�']) )
        else:
            buf += '[[1m%s[0m] [1;36m%s[37m%s ���� ��' % ( '���Ҽ�', ob['�̸�'], han_iga(ob['�̸�']) )
        buf += '%s��%s â���߽��ϴ�.[0m' % (line, han_obj(line))
        buf += MAIN_CONFIG['���Ļ����޼�������']
        ob.sendLine(buf)
        ob.channel.sendToAll(buf, ex = ob)

