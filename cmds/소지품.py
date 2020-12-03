# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        target = ob
        if line != '' and getInt(ob['�����ڵ��']) >= 1000:
            target = ob.env.findObjName(line)
            if target == None or is_player(target) == False:
                ob.sendLine('�� ����� �ȱ����δ� �׷����� ���� ���ٳ�')
                return
        ob.sendLine('����������������������������������')
        ob.sendLine('[0m[44m[1m[37m  ��     ��     ��     ǰ     ��  [0m[37m[40m')
        ob.sendLine('����������������������������������')
        if target.getInvenItemCount() == 0:
            ob.sendLine('[36m�� �ƹ��͵� �����ϴ�.[37m')
        else:
            nStr = {} # { ' ': 1, ' ':2,  ... }
            for obj in target.objs:
                if obj.inUse:
                    continue

                if obj.checkAttr('�����ۼӼ�', '��¾���') and getInt(ob['�����ڵ��']) < 1000:
                    continue
                c = 0
                try:
                    c = nStr[obj.get('�̸�')]
                except:
                    nStr[obj.get('�̸�')] = 0
                nStr[obj.get('�̸�')] = c + 1
                    
            for iName in nStr:
                c = nStr[iName]
                if c == 1:
                    ob.sendLine( '[36m' + iName + '[37m')
                else:
                    ob.sendLine( '[36m' + iName + ' [36m%d��[37m' % c)
            
        ob.sendLine('����������������������������������')
        ob.sendLine('[0m[47m[30m�� ���� : %20d �� [0m[37m[40m' % target.get('����'))
        if target['����'] == '':
            target['����'] = 0
        if target['����'] > 0:
            ob.sendLine('[0m[43m[30m�� ���� : %20d �� [0m[37m[40m' % target.get('����'))
        ob.sendLine('����������������������������������')
