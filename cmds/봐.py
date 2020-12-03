from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):

    def view(self, obj, ob):
        p = int(obj['보관수량'])
        pm = obj['보관증가은전']
        pp = obj['보관최대수량']
        
        ob.sendLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        buf = '◁ %s의 %s ▷' % (obj['주인'], obj['이름'])
        ob.sendLine('[1m[44m[37m%-78s[0m[40m[37m' % buf)
        ob.sendLine('───────────────────────────────────────')
        c = 0
        msg = ''
        for item in obj.objs:
            c += 1
            s = item['이름'] + ' ' + item.getOptionStr()
            s = '[%4d] %s' % (c, s)
            s1 = stripANSI(s)
            space = ' ' * (38 - len(s1))
            msg += '%-38s' % (s + space)
            #msg += '·%-24s' % (s + space)
            #msg += '[1;36m·[0;36m%-38s[0;37m  ' % (item['이름'] + ' ' + item.getOptionStr())
            if c % 2 == 0:
                msg += '\r\n'
        if msg != '':
            ob.sendLine(msg)

        if c == 0:
            ob.sendLine('☞ 아무것도 없습니다.')

        if obj['보관수량'] == obj['보관최대수량']:
            buf = '◆ 수량 (%d/%d)' % ( len(obj.objs), obj['보관수량'])
        else:
            buf = '◆ 수량 (%d/%d)  ◆ 최대수량 (%d)  ◆ 확장에 필요한 은전 (%d/%d)' % ( len(obj.objs), obj['보관수량'], \
            obj['보관최대수량'], getInt(obj['은전']), obj['보관증가은전'])
        ob.sendLine('───────────────────────────────────────')
        ob.sendLine('[0m[47m[30m%-78s[0m[40m[37m' % buf)
        ob.sendLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.viewMapData()
            return
        if ob.env == None:
            print ob['이름']
            return

        words = line.split()
        if line == '호위' or (len(words) > 1 and words[1] == '호위'):
            ob.do_command(line, True)
            return
        name, order = getNameOrder(line)

        
        if line == '나':
            obj = ob
        else:
            obj = ob.findObjInven(name, order)

        if obj == None:
            obj = ob.env.findObjName(line)
            if obj == None:
                ob.sendLine('☞ 당신의 안광으로는 그런것을 볼수 없다네')
                return
        if getInt(ob['관리자등급']) >= 1000 and is_player(obj) == False:
            ob.sendLine('Index : %s' % obj.index)
        if (line == '무기고' or line == '화초장' or line == '한옥장') and is_box(obj):
            self.view(obj, ob)
        else:
            obj.view(ob)
        if is_player(obj) and obj != ob:
            obj.sendLine('\r\n%s 당신을 살펴봅니다.' % ob.han_iga())
            obj.lpPrompt()
