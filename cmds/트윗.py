# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('☞ 사용법: [내용] 외침(,)')
            return
        if len(line) > 160:
            ob.sendLine('☞ 너무 길어요. ^^')
            return
            
        if ob.checkConfig('외침거부'):
            ob.sendLine('☞ 외침거부중엔 외칠 수 없어요. ^^')
            return
        if ob.act == ACT_REST:
            ob.sendLine('☞ 운기조식중에 외치게 되면 기가 흐트러집니다.')
            return
        if ob.env.noComm():
            ob.sendLine('☞ 이지역에서는 어떠한 통신도 불가능합니다.')
            return

        type = '[1;34mtwitter[0;37m'

        timemsg = time.strftime('[%H:%M] ', time.localtime())
        msg = ob.getNameA() + '(%s) : %s' % (type, line)

        m1 = self.ANSI(msg, True)
        m2 = self.ANSI(msg, False)

        Player.chatHistory.append(timemsg + m1 + '[0;37m')
        if len(Player.chatHistory) > 24:
            Player.chatHistory.__delitem__(0)

        # 잡담 로그를 파일로!!!
        from client import Client
        for ply in Client.players:
            if ply.state != ACTIVE:
                continue
            if ply.checkConfig('외침거부'):
                continue
            if ply.checkConfig('잡담시간보기'):
                if ply.checkConfig('사용자안시거부'):
                    buf = timemsg + m2
                else:
                    buf = timemsg + m1
            else:
                if ply.checkConfig('사용자안시거부'):
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
        kl = ob['설정상태'].splitlines()
        for k in kl:
            if k.find(config) == 0:
                if len(k.split()) > 1 and k.split()[1] == '1':
                    return True
                break
        return False

    def ANSI(self, msg, conv):
        buf = msg
        if conv == True:
            buf = buf.replace('{밝}', '[1m')
            buf = buf.replace('{어}', '[0m')
            buf = buf.replace('{검}', '[30m')
            buf = buf.replace('{빨}', '[31m')
            buf = buf.replace('{초}', '[32m')
            buf = buf.replace('{노}', '[33m')
            buf = buf.replace('{파}', '[34m')
            buf = buf.replace('{자}', '[35m')
            buf = buf.replace('{하}', '[36m')
            buf = buf.replace('{흰}', '[37m')
            buf = buf.replace('{배검}', '[40m')
            buf = buf.replace('{배빨}', '[41m')
            buf = buf.replace('{배초}', '[42m')
            buf = buf.replace('{배노}', '[43m')
            buf = buf.replace('{배파}', '[44m')
            buf = buf.replace('{배자}', '[45m')
            buf = buf.replace('{배하}', '[46m')
            buf = buf.replace('{배흰}', '[47m')
        else:
            buf = buf.replace('{밝}', '')
            buf = buf.replace('{어}', '')
            buf = buf.replace('{검}', '')
            buf = buf.replace('{빨}', '')
            buf = buf.replace('{초}', '')
            buf = buf.replace('{노}', '')
            buf = buf.replace('{파}', '')
            buf = buf.replace('{자}', '')
            buf = buf.replace('{하}', '')
            buf = buf.replace('{흰}', '')
            buf = buf.replace('{배검}', '')
            buf = buf.replace('{배빨}', '')
            buf = buf.replace('{배초}', '')
            buf = buf.replace('{배노}', '')
            buf = buf.replace('{배파}', '')
            buf = buf.replace('{배자}', '')
            buf = buf.replace('{배하}', '')
            buf = buf.replace('{배흰}', '')
        return buf
