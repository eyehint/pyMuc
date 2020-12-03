# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        
        words = line.split()
        if line == '' or len(words) < 3:
            ob.sendLine('�� ����: [���] [Ű] [��] �ɼ���')
            return
        name, order = getNameOrder(words[0])
        item = ob.findObjInven(name, order)
        if item == None:
            ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            return
        option = item.getOption() 
        if option == None:
            option = {}
        option[words[1]] = int(words[2])

        item.setOption(option)
        ob.sendLine('�� �����Ǿ����ϴ�.')
        #n = stripANSI(item['�̸�'])
        item['�̸�'] = '[1;34m' + item['�̸�'] + '[0;37m'

        
