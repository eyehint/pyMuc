# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        words = line.split(None, 1)
        if line == '' or len(words) < 2:
            ob.sendLine('�� ����: [���] [�̺�Ʈ] �̺�Ʈ����')
            return
            
        target = ob.env.findObjName(words[0])
        if target == None:
            ob.sendLine('�� �׷� ����� �����!')
            return
        if target.checkEvent(words[1]):
            ob.sendLine('�� �̹� �����Ǿ� �ֽ��ϴ�.')
            return
        target.setEvent(words[1])
        
        ob.sendLine('�� [%s] �̺�Ʈ�� �����Ǿ����ϴ�.' % words[1])
