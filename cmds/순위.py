# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    level = 1000
    def cmd(self, ob, line):
        #if getInt(ob['�����ڵ��']) < 1000:
        #    ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
        #    return
        if line == '':
            ob.sendLine('�� ����: [Ư��ġ] ����')
            return
        
        if getInt(ob['�����ڵ��']) < 1000:
            if line not in ['��', '����', '����', 'ü��', '����', '��ø', '����', '����', 'ȸ��', '�ʻ�', '��', '����']:
                ob.sendLine('�� ����: [Ư��ġ] ����')
                return
        if line == '����':
            line = '�ְ���'
        if line == 'ü��':
            line = '�ְ�ü��'
        if line == '��ø':
            line = '��ø��'

        if ob['����'] < 100000:
            ob.sendLine('�� ������ �����ؿ�.')
            return

        ob['����'] = ob['����'] - 100000
        l = []
        for c in ob.channel.players:
            if c['�̸�'] != '':
                if getInt(c['�����ڵ��']) != 0:
                    continue
                v = c[line]
                if v == '' or v == 0:
                    continue
                l.append((c['�̸�'], v))
            
        l.sort(reverse=True,key=lambda tup: tup[1])
        msg = ''
        cnt = 0
        for c in l:
            cnt += 1
            if getInt(ob['�����ڵ��']) >= 1000:
                msg += '%10s %-13d  ' % (c[0], c[1])
                if cnt % 3 == 0:
                    msg += '\r\n'
            else:
                msg += '[%02d] %-10s ' % (cnt, c[0]) 
                if cnt % 5 == 0:
                    msg += '\r\n'

            if cnt == 30:
                break
        ob.sendLine(msg)

