# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('☞ 사용법: [내용] 채널잡담([)')
            return
        if ob not in ob.adultCH:
            ob.sendLine('☞ 먼저 채널에 입장하세요.')
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

        buf = '[1;31m①⑨[0;37m ' + ob.getNameA() + ': %s' % line

        for ply in ob.adultCH:
            if ply.state != ACTIVE:
                continue
            if ply.checkConfig('외침거부'):
                continue
            if ply == ob:
                ply.sendLine(buf)
            else:
                ply.sendLine('\r\n' + buf)
                ply.lpPrompt()

    def checkConfig(self, ob, config):
        kl = ob['설정상태'].splitlines()
        for k in kl:
            if k.find(config) == 0:
                if len(k.split()) > 1 and k.split()[1] == '1':
                    return True
                break
        return False
