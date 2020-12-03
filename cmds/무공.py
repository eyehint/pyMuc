from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line != '' and getInt(ob['관리자등급']) >= 1000:
            target = ob.env.findObjName(line)
            if target == None or is_item(target):
                ob.sendLine('☞ 당신의 안광으로는 그런것을 볼수 없다네')
                return
        else:
            target = ob
        
        ob.sendLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        if target == ob:
            buf = '◁ 당신의 무공 ▷'
        else:
            buf = '◁ %s의 무공 ▷' % target['이름']
        ob.sendLine('[0m[47m[30m%-78s[0m[40m[37m' % buf)
        ob.sendLine('───────────────────────────────────────')
        ob.sendLine('[1m[40m[32m▷ 일반무공[0m[40m[37m')
        msg = ''
        if len(target.skillList) == 0:
            ob.sendLine('☞ 깨우친 무공이 없습니다.')
        else:
            c = 0
            for m in target.skillList:
                if m not in target.skillMap:
                    s = 1
                else:
                    s = target.skillMap[m][0]
                buf = '%s(%d성)' % (m, s)
                msg += ' ◇ %-20s ' % buf
                c += 1
                if c % 3 == 0:
                    msg += '\r\n'
            if c % 3 == 0:
                msg = msg[:-2]
            ob.sendLine(msg)
        ob.sendLine('───────────────────────────────────────')
        
        ob.sendLine('[1m[40m[32m▷ 비전[0m[40m[37m')
        buf = target['비전수련']
        lines = target['비전이름'].splitlines()
        if buf == '' and len(lines) == 0:
            ob.sendLine('☞ 오의를 깨우친 무공이 없습니다.')
        else:
            if buf != '':
                msg = '[1m[33m%s[0m[40m[37m(수련중)\r\n' % buf
            else:
                msg = ''
            c = 0
            for m in lines:
                msg += ' ◇ %-20s ' % m
                c += 1
                if c % 3 == 0:
                    msg += '\r\n'
            if c % 3 == 0:
                msg = msg[:-2]
            ob.sendLine(msg)
        ob.sendLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        