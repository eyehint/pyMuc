# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('�� ����: [������ �̸�] �Ծ�')
            return
        if ob.act == ACT_REST:
            ob.sendLine('�� ���� �� �ִ� ��Ȳ�� �ƴϳ׿�. ^_^')
            return
        name, order = getNameOrder(line)
        item = ob.findObjInven(name, order)
        if item == None:
            ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            return
        if item['�ɼ�'] != None:
            ob.sendLine(item['�ɼ�'])
            del item['�����ۼӼ�']
            del item['�ɼ�']
            return
