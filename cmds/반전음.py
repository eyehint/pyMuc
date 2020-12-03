# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('�� ����: [����] ������(:)')
            return
        words = line.split()
        if ob._talker == None:
            ob.sendLine('�� ������ ���޵ɸ��� ��밡 �����. ^^')
            return
        if ob._talker not in ob.channel.players:
            ob._talker = None
            ob.sendLine('�� ������ ���޵ɸ��� ��밡 �����. ^^')
            return
        ply = ob._talker

        if ob.checkConfig('�����ź�') or ply.checkConfig('�����ź�'):
            ob.sendLine('�� ���� �ź����̿���. ^^')
            return
        if ob.env.noComm():
            ob.sendLine('�� ������������ ��� ��ŵ� �Ұ����մϴ�.')
            return
        msg = ''
        for i in range(0, len(words)):
            msg += words[i] + ' ' 
        msg1 = '[[1m[36m����[0m[37m] %s���� ���� : %s' % (ply['�̸�'], msg)
        msg2 = '[[1m[36m����[0m[37m] %s : %s' % (ob['�̸�'], msg)

        ob.sendLine(msg1)
        ply._talker = ob
        ply.sendLine('\r\n' + msg2)
        ply.talkHistory.append(msg2)
        if len(ply.talkHistory) > 22:
            ply.talkHistory.__delitem__(0)
        ply.lpPrompt()
