# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob['�Ҽ�'] == '':
            ob.sendLine('�� ����� �Ҽ��� �����ϴ�.')
            return
        if ob['����'] != '����':
            ob.sendLine('�� ������ ���ָ��� �� �� �ֽ��ϴ�.')
            return
        words = line.split()
        if len(words) != 2:
            ob.sendLine('�� ���� : [���] [������ȣ] ���ĺ�ȣ')
            return
            
        obj = ob.env.findObjName(words[0])
        if obj == None  or is_player(obj) == False:
            ob.sendLine('�� �̰��� �׷� �������� �����ϴ�.')
            return
        if obj['�Ҽ�'] != ob['�Ҽ�']:
            ob.sendLine('�� ����� �Ҽ��� �ƴմϴ�.')
            return
        if obj == ob:
            buf3 = '�ڽ�'
        else:
            buf3 = obj['�̸�']
        if len(words[1]) > 10:
            ob.sendLine('�� ����Ͻ÷��� ��ȣ�� �ʹ� ����.')
            return
            
        obj['���ĺ�ȣ'] = words[1]
        ob.sendLine('����� [1m%s[0;37m�� ���ĺ�ȣ�� ��[1;32m%s[0;37m��%s ���� �����մϴ�.' % (buf3, words[1], han_uro(words[1])))
        ob.sendGroup('%s [1m%s[0;37m�� ���ĺ�ȣ�� ��[1;32m%s[0;37m��%s ���� �����մϴ�.' % (ob.han_iga(), buf3, words[1], han_uro(words[1])), prompt = True, ex = ob)
        
