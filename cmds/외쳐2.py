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
        if ob['성격'] == '선인':
            type = '[1;36m창룡후[0;37m'
        elif ob['성격'] == '기인':
            type = '[1;32m사자후[0;37m'
        else:
            type = '[32m외 침[37m'

        msg = time.strftime('[%H:%M] ', time.localtime()) + ob.getNameA() + '(%s) : %s' % (type, line)
        msg1 = ob.getNameA() + '(%s) : %s' % (type, line)
        Player.chatHistory.append(msg)
        if len(Player.chatHistory) > 22:
            Player.chatHistory.__delitem__(0)
        # 잡담 로그를 파일로!!!
        from client import Client
        for ply in Client.players:
            if ply.state != ACTIVE:
                continue
            if ply.checkConfig('외침거부'):
                continue
            if ply.checkConfig('잡담시간보기'):
                buf = msg
            else:
                buf = msg1
            if ply == ob:
                ply.sendLine(buf + ' [1;32m밍밍이지렁~[0;37m')
            else:
                ply.sendLine('\r\n' + buf + ' [1;32m밍밍이지렁~[0;37m')
                ply.lpPrompt()

    def checkConfig(self, ob, config):
        kl = ob['설정상태'].splitlines()
        for k in kl:
            if k.find(config) == 0:
                if len(k.split()) > 1 and k.split()[1] == '1':
                    return True
                break
        return False
