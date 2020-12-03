# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('�� ����: [����] ä�����([)')
            return
        if ob not in ob.adultCH:
            ob.sendLine('�� ���� ä�ο� �����ϼ���.')
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

        buf = '[1;31m���[0;37m ' + ob.getNameA() + ': %s' % line

        for ply in ob.adultCH:
            if ply.state != ACTIVE:
                continue
            if ply.checkConfig('��ħ�ź�'):
                continue
            if ply == ob:
                ply.sendLine(buf)
            else:
                ply.sendLine('\r\n' + buf)
                ply.lpPrompt()

    def checkConfig(self, ob, config):
        kl = ob['��������'].splitlines()
        for k in kl:
            if k.find(config) == 0:
                if len(k.split()) > 1 and k.split()[1] == '1':
                    return True
                break
        return False
