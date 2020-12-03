# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob.env.index != '낙양성:11':
            ob.sendLine('정보수집소에서 할 수 있습니다.')
            return
            
        if line == '':
            self.viewMemo(ob)
            #ob.sendLine('아직 쪽지기능을 사용할 수 없습니다.')
            return
        words = line.split(None, 1)
        if len(words) < 2:
            ob.sendLine('☞ 사용법: [이름] [제목] 쪽지')
            return
        found = False
        name = words[0]
        subject = words[1]
        for ply in ob.channel.players:
            if ply['이름'] == name:
                found = True
                break
        if found:
            ob.sendLine('접속중인 사용자에게는 보낼 수 없습니다.')
            return
            
        ply = Player()
        if ply.load(name) == False:
            ob.sendLine('존재하지않는 사용자입니다.')
            return
            
        if '메모:%s' % ob['이름'] in ply.memo:
            ob.sendLine('한번 보냈던 사용자에게는 다시 보낼 수 없습니다.')
            return
        ob._memo = {}
        ob._memo['제목'] = words[1]
        ob._memo['시간'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ob._memo['작성자'] = ob['이름']
        ob._memo['내용'] = ''
        ply.memo['메모:%s' % ob['이름']] = ob._memo
        ply.save(False)
        ob._memoWho = ply
        ob._memoBody = ''
        msg = '[%s]님에게 쪽지를 작성합니다. 끝내시려면 \'.\'를 치세요.\r\n분량 제한은 10줄입니다.\r\n:' % name
        ob.write(msg)
        ob.INTERACTIVE = 0
        ob.input_to(ob.write_memo)

        
    def viewMemo(self, ob):
        if len(ob.memo) == 0:
            ob.sendLine('도착한 쪽지가 없습니다.')
            return
        msg = '┌────────────────────────────────────┐\r\n'
        msg += '│◁                    무           림           첩                    ▷│\r\n'
        msg += '└────────────────────────────────────┘\r\n'
        for m in ob.memo:
            memo = ob.memo[m]
            msg += '[33m보 낸 이[37m : %s\r\n' % memo['작성자']
            msg += '[33m제    목[37m : %s\r\n' % memo['제목']
            msg += '[33m작성시각[37m : %s\r\n\r\n' % memo['시간']
            msg += '%s\r\n' % memo['내용']
            msg += ' ─────────────────────────────────────\r\n'
        ob.sendLine(msg[:-2])
        ob.memo = {}
