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
        hidden = 0
        for ex in exits:
            x = ex.split(None, 1)

            #if x[0][:len(x[0])-1] == line and x[0][-1] == '$': 
            if x[0][:-1] == line and x[0][-1] == '$': 
                #exit = x[0][:len(x[0])-1]
                exit = x[0][:-1]
                hidden = 1
            elif x[0] == line:
                exit = x[0] + '$'
                hidden = 2
            else:
                exit = x[0]

            nexit = exit + ' ' + x[1]

            if nexists == '':
                nexists = nexit
            else: 
                nexists = nexists + '\r\n' + nexit
            
        ob.env['�ⱸ'] = nexists
        del nexists
        ob.env.save()
        ob.env.init()

        if hidden == 2:
            ob.sendLine('�� �ⱸ�� ���������ϴ�.')
        elif hidden == 1:
            ob.sendLine('�� �ⱸ�� �巯�����ϴ�.')
        else:
            ob.sendLine('�� �׷� �ⱸ�� �����ϴ�.')


