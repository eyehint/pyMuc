# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('�� ����: [����] ��ħ(,)')
            return
        if len(line) > 160:
            ob.sendLine('�� �ʹ� ����. ^^')
            return
            
        if ob.checkConfig('��ħ�ź�'):
            ob.sendLine('�� ��ħ�ź��߿� ��ĥ �� �����. ^^')
            return
        if ob.act == ACT_REST:
            ob.sendLine('�� ��������߿� ��ġ�� �Ǹ� �Ⱑ ��Ʈ�����ϴ�.')
            return
        if ob.env.noComm():
            ob.sendLine('�� ������������ ��� ��ŵ� �Ұ����մϴ�.')
            return
        if ob['����'] == '����':
            type = '[1;36mâ����[0;37m'
        elif ob['����'] == '����':
            type = '[1;32m������[0;37m'
        else:
            type = '[32m�� ħ[37m'

        msg = time.strftime('[%H:%M] ', time.localtime()) + ob.getNameA() + '(%s) : %s' % (type, line)
        msg1 = ob.getNameA() + '(%s) : %s' % (type, line)
        Player.chatHistory.append(msg)
        if len(Player.chatHistory) > 22:
            Player.chatHistory.__delitem__(0)
        # ��� �α׸� ���Ϸ�!!!
        from client import Client
        for ply in Client.players:
            if ply.state != ACTIVE:
                continue
            if ply.checkConfig('��ħ�ź�'):
                continue
            if ply.checkConfig('���ð�����'):
                buf = msg
            else:
                buf = msg1
            if ply == ob:
                ply.sendLine(buf + ' [1;32m�ֹ�������~[0;37m')
            else:
                ply.sendLine('\r\n' + buf + ' [1;32m�ֹ�������~[0;37m')
                ply.lpPrompt()

    def checkConfig(self, ob, config):
        kl = ob['��������'].splitlines()
        for k in kl:
            if k.find(config) == 0:
                if len(k.split()) > 1 and k.split()[1] == '1':
                    return True
                break
        return False
