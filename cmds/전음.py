from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        words = line.split()
        if len(line) == 0 or len(words) < 2:
            ob.sendLine('☞ 사용법: [대상] [내용] 전음(/)')
            return
        found = False
        for ply in ob.channel.players:
            if ply['투명상태'] == 1:
                continue
            if ply['이름'] == words[0] and ply.state == ACTIVE:
                found = True
                break
        if found == False:
            ply = None
            
        if ply == None:
            ob.sendLine('☞ 전음이 전달될만한 상대가 없어요. ^^')
            return
        if not is_player(ply):
            ob.sendLine('☞ 전음이 전달될만한 상대가 없어요. ^^')
            return
        if ob.checkConfig('전음거부') or ply.checkConfig('전음거부'):
            ob.sendLine('☞ 전음 거부중이에요. ^^')
            return
        if ob.env.noComm():
            ob.sendLine('☞ 이지역에서는 어떠한 통신도 불가능합니다.')
            return
        msg = ''
        for i in range(1, len(words)):
            msg += words[i] + ' ' 
        msg1 = '[[1m[36m전음[0m[37m] %s에게 보냄 : %s' % (ply['이름'], msg)
        msg2 = '[[1m[36m전음[0m[37m] %s : %s' % (ob['이름'], msg)

        ob.sendLine(msg1)
        ply._talker = ob
        ply.sendLine('\r\n' + msg2)
        ply.talkHistory.append(msg2)
        if len(ply.talkHistory) > 22:
            ply.talkHistory.__delitem__(0)
        ply.lpPrompt()
