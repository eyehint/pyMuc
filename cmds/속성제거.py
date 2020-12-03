# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        words = line.split()
        if line == '' or len(words) < 3:
            ob.sendLine('�� ����: [���] [Ű] [��] �Ӽ�����')
            return
        words = line.split(None, 3)
        target = ob.env.findObjName(words[0])
        if target == None:
            ob.sendLine('�� �׷� ����� �����!')
            return
         
        if words[1] not in target.attr:
            ob.sendLine('�� Ű�� �����ϴ�.')
            return
        else:
            if target.checkAttr(words[1], words[2]) == False:
                ob.sendLine('�� �Ӽ��� �����ϴ�.')
                return
                
            target.delAttr(words[1], words[2])
            ob.sendLine('�� �Ӽ��� ���� �Ǿ����ϴ�.')
        
