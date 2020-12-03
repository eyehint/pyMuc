# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        mode = False
        msg = ''
        cnt = 0
        if line == '방' or line == '방파':
            if ob['소속'] == '':
                ob.sendLine('☞ 당신은 소속이 없습니다.')
                return
            mode = True
        
        for c in ob.channel.players:
            if c['투명상태'] == 1:
                continue
            if c['이름'] != '' and c.state == ACTIVE:
                if mode and c['소속'] != ob['소속']:
                    continue
                nick = c['무림별호']
                
                if nick == '':
                    buf = '[[0;37m%s[0;37m]' % '무명객'
                else:
                    bright = 1
                    if c['레벨초기화'] != '':
                       bright = 0

                    if c['성격'] == '정파':
                        buf = '[[%d;32m%s[0;37m]' % (bright, nick)
                    elif c['성격'] == '기인':
                        buf = '[[%d;33m%s[0;37m]' % (bright, nick)
                    elif c['성격'] == '선인':
                        buf = '[[%d;36m%s[0;37m]' % (bright, nick)
                    else:
                        buf = '<[%d;31m%s[0;37m>' % (bright, nick)
                    
                msg += '  %-26s %-10s' % (buf, c['이름'])
                cnt += 1
                if cnt % 3 == 0:
                    msg += '\r\n'
        if cnt % 3 == 0:
            msg = msg[:-2]
        ob.sendLine('┌─────────────────────────────────────┐')
        ob.sendLine('│[7m%-74s[0;37m│' % ' ◁     무       림       크       래       프       트      １-１     ▷');
        ob.sendLine('└─────────────────────────────────────┘')
        ob.sendLine(msg);
        ob.sendLine(' ──────────────────────────────────────')
        if mode:
            ob.sendLine(' ★ 총 %d명의 [1m【[36m%s[37m】[0;37m파 무림인이 활동하고 있습니다.' % (cnt, ob['소속']))
        else:
            ob.sendLine(' ★ 총 %d명의 무림인이 활동하고 있습니다.' % cnt)

