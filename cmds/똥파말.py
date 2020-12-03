# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob['�Ҽ�'] == '':
            ob.sendLine('�� ����� �Ҽ��� �����ϴ�.')
            return
        if line == '':
            ob.sendLine('�� ���� : [����] ���ĸ�(])')
            return
        if ob.checkConfig('���ĸ��ź�'):
            ob.sendLine('�� ���ĸ� �ź��� �̿���. *^^*')
            return
        try:    
            fp = open('data/log/group/' + ob['�Ҽ�'], 'a')
        except:
            pass
        fp.write(time.strftime('[%Y-%m-%d %H:%M:%S] ', time.localtime()) + '%-10s' % ob['�̸�'] + ': ' + line + '\n')
        fp.close()
        ob.sendGroup(line, prompt = True)
        
