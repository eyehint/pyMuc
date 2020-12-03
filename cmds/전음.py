# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        words = line.split()
        if len(line) == 0 or len(words) < 2:
            ob.sendLine('�� ����: [���] [����] ����(/)')
            return
        found = False
        for ply in ob.channel.players:
            if ply['�������'] == 1:
                continue
            if ply['�̸�'] == words[0] and ply.state == ACTIVE:
                found = True
                break
        if found == False:
            ply = None
            
        if ply == None:
            ob.sendLine('�� ������ ���޵ɸ��� ��밡 �����. ^^')
            return
        if not is_player(ply):
            ob.sendLine('�� ������ ���޵ɸ��� ��밡 �����. ^^')
            return
        if ob.checkConfig('�����ź�') or ply.checkConfig('�����ź�'):
            ob.sendLine('�� ���� �ź����̿���. ^^')
            return
        if ob.env.noComm():
            ob.sendLine('�� ������������ ��� ��ŵ� �Ұ����մϴ�.')
            return
        msg = ''
        for i in range(1, len(words)):
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
