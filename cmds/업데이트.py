# -*- coding: euc-kr -*-

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            ob.sendLine('* ��ɾ�, ������ȣ, ����, ����, ǥ��, �����, ���μ���, ��ũ��Ʈ �߿� �����ϼ���')
        elif line == '��ɾ�':
            init_commands()
            ob.sendLine('* ��ɾ ������Ʈ �Ǿ����ϴ�.')
        elif line == '������ȣ':
            NICKNAME.load()
            ob.sendLine('* ������ȣ�� ������Ʈ �Ǿ����ϴ�.')
        elif line == '����':
            HELP.load()
            ob.sendLine('* ������ ������Ʈ �Ǿ����ϴ�.')
        elif line == '����':
            MUGONG.load()
            ob.sendLine('* ������ ������Ʈ �Ǿ����ϴ�.')
        elif line == 'ǥ��':
            EMOTION.load()
            ob.sendLine('* ǥ���� ������Ʈ �Ǿ����ϴ�.')
        elif line == '�����':
            DOUMI.load()
            ob.sendLine('* ����̰� ������Ʈ �Ǿ����ϴ�.')
        elif line == '���μ���':
            MAIN_CONFIG.load()
            ob.sendLine('* ���μ����� ������Ʈ �Ǿ����ϴ�.')
        elif line == '��ũ��Ʈ':
            SCRIPT.load()
            ob.sendLine('* ��ũ��Ʈ�� ������Ʈ �Ǿ����ϴ�.')
