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
        
        ob.sendLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        buf = ' [1m[32mЖ [37m%s[0;37m의 무공집결 상태 [1m[32mЖ[0m[37m' % target['이름']
        ob.sendLine(buf)
        
        if len(target.skills) == 0:
            ob.sendLine('──────────────────────────────')
            ob.sendLine(MAIN_CONFIG['무공시전없음'])
            ob.sendLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
            return
        ob.sendLine('────────┬──────┬──────────────')
        for s in target.skills:
            inc = 1
            if s.name in target.skillMap:
                inc = target.skillMap[s.name][0]
            n = s['방어시간'] + s['방어시간증가치'] * (inc - 1)
            t = s.start_time
            cnt = len(target.strBar)
            a = t * 10 / n
            if a < 0:
                a = 0
            if a >= cnt:
                a = cnt - 1
            buf = '%5dː%s' % (t, target.strBar[a])
            ob.sendLine('[1m[40m[36m·[0m[40m[37m%-14s│%-12s│ %s' % (s.name, s['방어상태출력'], buf)) 
        ob.sendLine('━━━━━━━━┷━━━━━━┷━━━━━━━━━━━━━━')
