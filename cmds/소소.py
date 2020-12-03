from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        target = ob
        if line != '' and getInt(ob['관리자등급']) >= 1000:
            target = ob.env.findObjName(line)
            if target == None or is_player(target) == False:
                ob.sendLine('☞ 당신의 안광으로는 그런것을 볼수 없다네')
                return
        ob.sendLine('━━━━━━━━━━━━━━━━━')
        ob.sendLine('[0m[44m[1m[37m  ◁     소     지     품     ▷  [0m[37m[40m')
        ob.sendLine('─────────────────')
        if target.getInvenItemCount() == 0:
            ob.sendLine('[36m☞ 아무것도 없습니다.[37m')
        else:
            nStr = {} # { ' ': 1, ' ':2,  ... }
            for obj in target.objs:
                if obj.inUse:
                    continue

                if obj.checkAttr('아이템속성', '출력안함') and getInt(ob['관리자등급']) < 1000:
                    continue
                c = 0
                try:
                    c = nStr[obj.get('이름')]
                except:
                    nStr[obj.get('이름')] = 0
                nStr[obj.get('이름')] = c + 1
                    
            for iName in nStr:
                c = nStr[iName]
                if c == 1:
                    ob.sendLine( '[36m' + iName + '[37m')
                else:
                    ob.sendLine( '[36m' + iName + ' [36m%d개[37m' % c)
            
        ob.sendLine('─────────────────')
        ob.sendLine('[0m[47m[30m▶ 은전 : %20d 개 [0m[37m[40m' % target.get('은전'))
        if ob['금전'] == '':
            ob['금전'] = 0
        if ob['금전'] > 0:
            ob.sendLine('[0m[47m[30m▶ 금전 : %20d 개 [0m[37m[40m' % ob['금전'])
        ob.sendLine('─────────────────')
