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

        type = '[1;34mtwitter[0;37m'

        timemsg = time.strftime('[%H:%M] ', time.localtime())
        msg = ob.getNameA() + '(%s) : %s' % (type, line)

        m1 = self.ANSI(msg, True)
        m2 = self.ANSI(msg, False)

        Player.chatHistory.append(timemsg + m1 + '[0;37m')
        if len(Player.chatHistory) > 24:
            Player.chatHistory.__delitem__(0)

        # ��� �α׸� ���Ϸ�!!!
        from client import Client
        for ply in Client.players:
            if ply.state != ACTIVE:
                continue
            if ply.checkConfig('��ħ�ź�'):
                continue
            if ply.checkConfig('���ð�����'):
                if ply.checkConfig('����ھȽðź�'):
                    buf = timemsg + m2
                else:
                    buf = timemsg + m1
            else:
                if ply.checkConfig('����ھȽðź�'):
                    buf = m2
                else:
                    buf = m1
            if ply == ob:
                ply.sendLine(buf + '[0;37;40m')
            else:
                ply.sendLine('\r\n' + buf + '[0;37;40m')
                ply.lpPrompt()

        _content = unicode(stripANSI(m2), 'euc-kr').encode('utf-8')
        queue.put(_content)

    def checkConfig(self, ob, config):
        kl = ob['��������'].splitlines()
        for k in kl:
            if k.find(config) == 0:
                if len(k.split()) > 1 and k.split()[1] == '1':
                    return True
                break
        return False

    def ANSI(self, msg, conv):
        buf = msg
        if conv == True:
            buf = buf.replace('{��}', '[1m')
            buf = buf.replace('{��}', '[0m')
            buf = buf.replace('{��}', '[30m')
            buf = buf.replace('{��}', '[31m')
            buf = buf.replace('{��}', '[32m')
            buf = buf.replace('{��}', '[33m')
            buf = buf.replace('{��}', '[34m')
            buf = buf.replace('{��}', '[35m')
            buf = buf.replace('{��}', '[36m')
            buf = buf.replace('{��}', '[37m')
            buf = buf.replace('{���}', '[40m')
            buf = buf.replace('{�軡}', '[41m')
            buf = buf.replace('{����}', '[42m')
            buf = buf.replace('{���}', '[43m')
            buf = buf.replace('{����}', '[44m')
            buf = buf.replace('{����}', '[45m')
            buf = buf.replace('{����}', '[46m')
            buf = buf.replace('{����}', '[47m')
        else:
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{���}', '')
            buf = buf.replace('{�軡}', '')
            buf = buf.replace('{����}', '')
            buf = buf.replace('{���}', '')
            buf = buf.replace('{����}', '')
            buf = buf.replace('{����}', '')
            buf = buf.replace('{����}', '')
            buf = buf.replace('{����}', '')
        return buf
