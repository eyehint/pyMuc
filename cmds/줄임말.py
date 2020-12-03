# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            if len(ob.alias) == 0:
                ob.sendLine('�� ���Ӹ��� �����Ǿ� ���� �ʾƿ�. ^^')
                return
            ob.sendLine('������������������������������������������������������������������������������')
            ob.sendLine('[47m[30m�� ���Ӹ� ��                                                                  [40m[37m')
            ob.sendLine('������������������������������������������������������������������������������')
            msg = ''
            for key in ob.alias:
                msg += '[%s] %s\r\n' % (key, ob.alias[key])
            ob.write(msg)
            ob.sendLine('������������������������������������������������������������������������������')
            return

        wlist = line.split(None, 1)
        key = wlist[0]
        #�μ��� �ϳ��� ���Ӹ� ����
        if len(wlist) == 1:
            if ob.delAlias(key):
                ob.sendLine('�� ���Ӹ��� �����Ͽ����. ^^')
            return
        
        data = wlist[1].strip()

        wlist = data.split(';')
        if key in wlist:
            ob.sendLine('�� ��ø�� ���Ӹ��� ����� �� �����. ^^')
            return
        for word in wlist:
            if word in ob.alias:
                ob.sendLine('�� ��ø�� ���Ӹ��� ����� �� �����. ^^')
                return
        if len(ob.alias) >= 100:
            ob.sendLine('�� ���Ӹ��� �ʹ� ���ƿ�. ^^')
            return
            
        
        if ob.setAlias(key, data):
            ob.sendLine('�� ���Ӹ��� �����Ͽ����. ^^')
        

