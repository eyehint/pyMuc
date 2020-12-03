# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    level = 1000
    def cmd(self, ob, line):
        #if getInt(ob['�����ڵ��']) < 1000:
        #    ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
        #    return
        words = line.split()

        if line == '' or len(words) < 2:
            ob.sendLine('�� ����: [������] [Ư��ġ] ����')
            return

        w = words[0]

        obj = ob.env.findObjName(line)
        if obj == None:
            ob.sendLine('�� ����� �ȱ����δ� �׷����� ���� ���ٳ�')
            return

        if is_box(obj) == False:
            ob.sendLine('�� ����� �ȱ����δ� �׷����� ���� ���ٳ�')
            return
         
        self.k = words[1]
        if self.k not in ['��', '��ø��', '����', '����', 'ȸ��', '�ʻ�', '��', '����', 'ü��', '����', '�̸�']:
            ob.sendLine('�� ��|��ø��|����|����|ȸ��|�ʻ�|��|����|ü��|����|�̸� �� �����մϴ�.')
            return

        if ob['����'] < 100000:
            ob.sendLine('�� ������ �����ؿ�.')
            return

        #obj.objs.sort(reverse=True, key=self.getOp)
        if self.k == '�̸�':
            obj.objs.sort(key=lambda item: (item['�̸�'], item['�̸�']))
        else:
            obj.objs.sort(key=lambda item: (self.getOp(item), item['�̸�']))
        ob.sendLine('�� ���ĵǾ����ϴ�.')
        ob['����'] = ob['����'] - 100000
        return
            

    def getOp(self, obj):
        op = obj.getOption()
        if op == None:
            return 0
        if self.k not in op:
            return 0
        return op[self.k]

