# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        words = line.split()
        if line == '':
            target = ob.env
        else:
            target = ob.env.findObjName(line)
        if target == None:
            target = ob.findObjName(line)
            if target == None:
                ob.sendLine('�� �׷� ����� �����!')
                return
        msg = ''
        l = target.attr.keys()
        l.sort()
        for at in l:
            msg += '#%s\r\n' % at
            for m in str(target.attr[at]).splitlines():
                msg += ':%s\r\n' % m
            msg += '\r\n'
            
        ob.sendLine(msg)
        