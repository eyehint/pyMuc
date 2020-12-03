# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('�� ����: [���] ��')
            return
        obj = ob.env.findObjName(line)
        if is_mob(obj) == False and is_player(obj) == False:
            ob.sendLine('�ڽ��� ���¸� ��ź�� �մϴ�. @_@')
            return
        if obj == None or obj['������'] == 7:
            ob.sendLine('�� �׷� �񱳴���� �����. ^^')
            return
        if ob == obj:
            ob.sendLine('�ڽ��� ���¸� ��ź�� �մϴ�. @_@')
            return
        if ob.checkConfig('�񱳰ź�') or (is_player(obj) and obj.checkConfig('�񱳰ź�')):
            ob.sendLine('�� ������ �ºζ� �񹫸� ���ؼ� �� �� �ִ� �� ����')
            return
        
        mT, c1, c2 = ob.getAttackPoint(obj)
        uT, c1, c2 = obj.getAttackPoint(ob)
        if is_player(obj):
            mH = obj['�ְ�ü��'] / mT
        else:
            mH = obj['ü��'] / mT
        uH = ob['�ְ�ü��'] / uT
        ob.sendLine('������������������������������')
        ob.sendLine('�� [1m%s[0;37m%s�� ����' % ( obj['�̸�'] , han_wa(obj['�̸�']) ))
        ob.sendLine('������������������������������')
        ob.sendLine('�� ����� �·� ������%d' % uH)
        ob.sendLine('�� ����� �·� ������%d' % mH)
        ob.sendLine('�� ��  �� ���� �����%d' % (uH-mH))
        ob.sendLine('������������������������������')

