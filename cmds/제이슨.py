# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        import json
        j = json.dumps(ob.attr, sort_keys=True, indent=4, \
            separators=(',', ': '), encoding='euc-kr')
        j1 = j.decode('euc-kr')
        print j1
        print j
        #ob.sendLine(j1)

