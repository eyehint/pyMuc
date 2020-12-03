# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
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
        if is_item(target):
            msg = '[����������]\n\n'
        elif is_mob(target):
            msg = '[������]\n\n'
        elif line == '':
            msg = '[������]\r\n'
        else:
            ob.sendLine('�� ������ �� �����!')
            return
        l = target.attr.keys()
        l.sort()
        for at in l:
            msg += '#%s\n' % at
            for m in str(target.attr[at]).splitlines():
                msg += ':%s\n' % m
            msg += '\n'

        try:
            f = open(target.path, 'w')
        except:
            ob.sendLine('* ���� ���⸦ �����Ͽ����ϴ�.')
            return False
        f.write(msg)
        f.close()
       
        ob.sendLine('* %s ����Ǿ����ϴ�.' % target.path)
        
