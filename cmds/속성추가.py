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
            ob.sendLine('�� ����: [���] [Ű] [��] Ű������')
            return
        words = line.split(None, 3)
        target = ob.env.findObjName(words[0])
        if target == None:
            ob.sendLine('�� �׷� ����� �����!')
            return
        try:
            v = long(words[2])
        except:
            v = words[2]
         
        if words[1] not in target.attr:
            target[words[1]] = v
        else:
            try:
                target[words[1]] += '\r\n' + words[2]
            except:
                ob.sendLine('�� �Ӽ��߰��� �����߽��ϴ�.')
                return
        ob.sendLine('�� �Ӽ��� �߰� �Ǿ����ϴ�.')
        