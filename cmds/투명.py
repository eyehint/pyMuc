# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        ob.sendLine('%d' % time.time())
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        
        if ob['�������'] == 0:
            ob['�������'] = 1
            ob.sendLine('�� ������°� �Ǿ����ϴ�')
        else:
            ob['�������'] = 0
            ob.sendLine('�� ������°� �����Ǿ����ϴ�')
        """
        from client import Client
        for ply in Client.players:
            if ply.state != ACTIVE:
                continue
        """
        """
        Player.CFG = ['�ڵ�����', '�񱳰ź�', '���˰ź�', '����ź�', '�����ź�', 
    '��ħ�ź�', '���ĸ��ź�', '��������', '�������', '��ħ������',
    '��ھȽðź�', '����ھȽðź�', '�����Ը޼����ź�', 
    'Ÿ��������°ź�', '�ڵ���������', '�����ź�', '���ø��', '���ð�����']
        
        """

