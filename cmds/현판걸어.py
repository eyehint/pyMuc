from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('☞ 사용법 : [방파이름] 현판걸어')
            return
        if len(line) > 10 or len(line) < 2:
            ob.sendLine('방파이름이 너무 길어요!.')
            return
        if len(line) < 2:
            ob.sendLine('방파이름이 너무 짧아요!.')
            return
        if ob.env.checkAttr('방파자리') == False:
            ob.sendLine('☞ 이곳엔 현판을 걸 수 없습니다.')
            return
        if ob.env['방파주인'] != '':
            ob.sendLine('☞ 이곳엔 현판을 걸 수 없습니다.')
            return
        if ob['소속'] != '':
            ob.sendLine('☞ 당신은 방파를 세울 수 없습니다.')
            return
        if ob['방파금지'] != '':
            ob.sendLine('☞ 당신은 방파를 세울 수 없습니다.')
            return
        if ob['레벨'] < 400:
            ob.sendLine('☞ 당신은 방파를 세울 수 없습니다.')
            return
        if ob['은전'] < MAIN_CONFIG['방파세울은전']:
            ob.sendLine('☞ 방파를 세우는데는 은전 10,000,000개 이상이 필요합니다.')
            return
            
        for guild in GUILD.attr:
            if GUILD.attr[guild]['이름'] == line:
                ob.sendLine('☞ 존재하는 방파이름입니다.')
                return
        g = {}
        g['이름'] = line
        g['방주이름'] = ob['이름']
        g['방파원수'] = 1
        g['방파맵'] = ob.env.index
        g['방주명칭'] = '방주'
        g['부방주명칭'] = '부방주'
        g['장로명칭'] = '장로'
        g['방파인명칭'] = '방파인'
        GUILD.attr[line] = g
        GUILD.save()
        ob['소속'] = line
        ob['직위'] = '방주'
        ob.env['방파주인'] = line
        ob.env.save()
        for enter in ob.env['방파입구'].splitlines():
            if enter.find(':') == -1:
                path = ob.env.zone + ':' + enter
            else:
                path = enter
            room = getRoom(path)
            if room == None:
                continue
            room['방파주인'] = line
            room.save()
            
        item = getItem('보관함').clone()
        ob.insert(item)
        ob['은전'] -= MAIN_CONFIG['방파세울은전']
        ob.sendLine('당신이 현판을 세우는데 은전 %d개를 사용합니다.' % MAIN_CONFIG['방파세울은전'])
        
        buf = MAIN_CONFIG['방파생성메세지머리']
        if ob['성격'] == '정파':
            buf += '[[1;32m%s[0;37m] [1;36m%s[37m%s 방파 『' % ( ob['무림별호'], ob['이름'], han_iga(ob['이름']) )
        elif ob['성격'] == '사파':
            buf += '[[1;31m%s[0;37m] [1;36m%s[37m%s 방파 『' % ( ob['무림별호'], ob['이름'], han_iga(ob['이름']) )
        else:
            buf += '[[1m%s[0m] [1;36m%s[37m%s 방파 『' % ( '무소속', ob['이름'], han_iga(ob['이름']) )
        buf += '%s』%s 창설했습니다.[0m' % (line, han_obj(line))
        buf += MAIN_CONFIG['방파생성메세지꼬리']
        ob.sendLine(buf)
        ob.channel.sendToAll(buf, ex = ob)

