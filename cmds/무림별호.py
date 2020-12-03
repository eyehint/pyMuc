from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        line = line.strip()
        if len(line) == 0 or len(line.split()) > 1:
            ob.sendLine('☞ 사용법: [별호이름] 무림별호')
            return
        
        if ob['무림별호'] != '':
            ob.sendLine('☞ 이미 별호를 만들었어요. ^^')
            return
            
        if ob.checkEvent('무림별호설정') == False:
            ob.sendLine('☞ 아직은 무림별호를 받을 수 없어요. ^^')
            return
        if len(line) < 3:
            ob.sendLine('☞ 사용하시려는 별호가 너무 짧아요.')
            return
        if len(line) > 10:
            ob.sendLine('☞ 사용하시려는 별호가 너무 길어요.')
            return
            
        if line in NICKNAME.attr:
            ob.sendLine('☞ 다른 무림인이 사용중인 별호입니다. ^^')
            return
        ob['무림별호'] = line
        
        if ob.checkEvent('무림별호 사파'):
            ob['성격'] = '사파'
            buf = '[1m☞ [[31m사파[37m] '
        else:
            ob['성격'] = '정파'
            buf = '[1m☞ [[32m정파[37m] '
            
        NICKNAME[line] = ob['이름']
        NICKNAME.save()
        
        ob.delEvent('무림별호설정')
        ob.delEvent('무림별호 사파')
        ob.delEvent('무림별호 정파')
        
        msg = '[1m%s%s [1m자신의 별호를 『[33m%s[37m』%s 칭하기 시작합니다.[0;37m' % ( buf, ob.han_iga(), line, han_uro(line))
        ob.channel.sendToAll(msg, ex = ob)
        ob.sendLine(msg + '\r\n')
        
        ob.makeHome()
        roomName = '사용자맵:%s' % ob['이름']
        ob['귀환지맵'] = roomName
        ob.save()
        room = getRoom(roomName)
        if room == None:
            ob.sendLine('☞ 사용자맵 생성에 실패하였습니다.')
            return
        
        ob.enterRoom(room, '귀환', '귀환')
