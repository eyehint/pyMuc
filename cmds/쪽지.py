# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob.env.index != '���缺:11':
            ob.sendLine('���������ҿ��� �� �� �ֽ��ϴ�.')
            return
            
        if line == '':
            self.viewMemo(ob)
            #ob.sendLine('���� ��������� ����� �� �����ϴ�.')
            return
        words = line.split(None, 1)
        if len(words) < 2:
            ob.sendLine('�� ����: [�̸�] [����] ����')
            return
        found = False
        name = words[0]
        subject = words[1]
        for ply in ob.channel.players:
            if ply['�̸�'] == name:
                found = True
                break
        if found:
            ob.sendLine('�������� ����ڿ��Դ� ���� �� �����ϴ�.')
            return
            
        ply = Player()
        if ply.load(name) == False:
            ob.sendLine('���������ʴ� ������Դϴ�.')
            return
            
        if '�޸�:%s' % ob['�̸�'] in ply.memo:
            ob.sendLine('�ѹ� ���´� ����ڿ��Դ� �ٽ� ���� �� �����ϴ�.')
            return
        ob._memo = {}
        ob._memo['����'] = words[1]
        ob._memo['�ð�'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ob._memo['�ۼ���'] = ob['�̸�']
        ob._memo['����'] = ''
        ply.memo['�޸�:%s' % ob['�̸�']] = ob._memo
        ply.save(False)
        ob._memoWho = ply
        ob._memoBody = ''
        msg = '[%s]�Կ��� ������ �ۼ��մϴ�. �����÷��� \'.\'�� ġ����.\r\n�з� ������ 10���Դϴ�.\r\n:' % name
        ob.write(msg)
        ob.INTERACTIVE = 0
        ob.input_to(ob.write_memo)

        
    def viewMemo(self, ob):
        if len(ob.memo) == 0:
            ob.sendLine('������ ������ �����ϴ�.')
            return
        msg = '����������������������������������������������������������������������������\r\n'
        msg += '����                    ��           ��           ø                    ����\r\n'
        msg += '����������������������������������������������������������������������������\r\n'
        for m in ob.memo:
            memo = ob.memo[m]
            msg += '[33m�� �� ��[37m : %s\r\n' % memo['�ۼ���']
            msg += '[33m��    ��[37m : %s\r\n' % memo['����']
            msg += '[33m�ۼ��ð�[37m : %s\r\n\r\n' % memo['�ð�']
            msg += '%s\r\n' % memo['����']
            msg += ' ��������������������������������������������������������������������������\r\n'
        ob.sendLine(msg[:-2])
        ob.memo = {}
