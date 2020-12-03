# -*- coding: euc-kr -*-

from objs.cmd import Command
from include.ansi import *

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            c = 0
            for obj in ob.env.objs:
                if is_mob(obj) == False:
                    continue
                if obj.act == ACT_DEATH or obj.act == ACT_REGEN:
                    c += 1
                    obj.doRegen()
            if c != 0:
                #ob.sendLine('�� �����Ǿ����ϴ�.')
                ob.env.printPrompt(ex = ob['�̸�'])
                ob.sendLine('\r\n\r\n�� �����Ǿ����ϴ�.')
            else:
                ob.sendLine('�� ������ ���� �����!!')
            return
        obj = ob.env.findObjName(line)
        if obj == None or is_item(obj) or is_player(obj):
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if obj.act != ACT_DEATH:
            ob.sendLine('�� ��ü�� �����մϴ�. *^_^*')
            return
        obj.doRegen()
        ob.env.printPrompt(ex = ob['�̸�'])
        
 