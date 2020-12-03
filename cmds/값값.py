# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        ob.sendLine('%d' % time.time())
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        
        words = line.split(',', 2)
        if line == '' or len(words) < 3:
            ob.sendLine('�� ����: [���],[Ű],[��] ������')
            return
        #ob.sendLine('�� �������Դϴ�.')
        #return
        if len(words[2]) > 20:
            ob.sendLine('�� �ʹ� ����!')
            return
        target = ob.env.findObjName(words[0])

        if target == None:
            ob.sendLine('�� �׷� ����� �����!')
            return
        """    
        if ob['�����ڵ��'] < 2000:
            if words[1] not in target.attr:
                ob.sendLine('�� �ش� Ű�� �����ϴ�.')
                return
        """
        if words[1] in target.attr:
            t = type(target[words[1]])
            try:
                v = t(words[2])
            except:
                ob.sendLine('�� �߸��� ���Դϴ�.')
                return
        else:
            try:
                v = int(words[2])
            except:
                v = words[2]
        target[words[1]] = v
        ob.sendLine('�� ���� �����Ǿ����ϴ�.')
        

