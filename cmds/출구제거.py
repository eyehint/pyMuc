#-*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):

        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            ob.sendLine('�� ����: [�ⱸ] �ⱸ����')
            return

        exits = ob.env['�ⱸ'].splitlines()
        nexists = ''
        c = 0
        for ex in exits:
            x = ex.split(None, 1)
            if x[0][:-1] == line and x[0][-1] == '$': 
                c = 1
                continue
            elif x[0] == line:
                c = 1
                continue
            nexit = x[0] + ' ' + x[1]
            if nexists == '':
                nexists = nexit
            else: 
                nexists = nexists + '\r\n' + nexit
            
        ob.env['�ⱸ'] = nexists
        del nexists
        ob.env.init()

        if c == 1:
            ob.sendLine('�� �ⱸ�� ���ŵǾ����ϴ�.')
        else:
            ob.sendLine('�� �׷� �ⱸ�� �����ϴ�.')


