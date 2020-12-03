# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            if len(ob.autoMoveList) == 0:
                ob.sendLine('�� ����: [���������Ӹ�] �ڵ����')
                return
            else:
                ob.autoMoveList = []
                ob.sendLine('�� �ڵ���ΰ� �����Ǿ����ϴ�.')
                return

            msg = '['
            for path in ob.autoMoveList:
                msg += '%s, ' % path
            msg = msg[:-2] + ']'
            ob.write(msg)
            return
        
        if line not in ob.alias:
            ob.sendLine('�� �ش� ���Ӹ��� �����. ^^')
            return
        ob.autoMoveList = ob.alias[line].split(';') 
        ob.sendLine('�� �ڵ���θ� �����Ͽ����. ^^')
        next = ob.autoMoveList.pop(0)
        ob.do_command(next)
        

