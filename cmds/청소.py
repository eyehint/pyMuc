# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
            
        import gc
        gc.enable()
        cnt = gc.collect(1)
        ob.sendLine('* û�����Դϴ�. %d' % cnt)
