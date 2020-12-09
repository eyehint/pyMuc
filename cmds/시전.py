from objs.cmd import Command

class CmdObj(Command):
    def cool1(self, ob, name):
        ob.cooltime[name] = 2
        if name == '능파미보':
            if ob.act != ACT_DEATH:
                ob.sendLine('\n당신이 펼쳐놓은 [1;36m凌波微步[;37m의 신법을 멈춥니다.')
            ob._miss -= 350
        elif name == '역근경':
            if ob.act != ACT_DEATH:
                ob._str -= 500
                ob._arm -= 500
                ob._maxhp -= 50
                ob.sendLine('\n당신이 펼쳐낸 [1;33m易筋經[0;37m의 모든 [1;32m運氣行功[0;37m [1;31m要訣[0;37m을 거두어 들입니다.')
            if ob['체력'] > ob.getMaxHp():
                ob['체력'] = ob.getMaxHp()

        reactor.callLater(5, self.cool2, ob, name)
        return

    def cool2(self, ob, name):
        ob.cooltime[name] = 0
        return

    def cmd(self, ob, line):
        from objs.skill import MUGONG
        if ob.act == ACT_REST:
            ob.sendLine('☞ 운기조식중엔 무공을 사용할 수 없습니다.')
            return

        if len(line) == 0:
            ob.sendLine('☞ 사용법: [대상|무공이름] 시전')
            return

        words = line.split()
        l = len(words)
        if l == 1:
            mName = line
            tName = ''
            if ob.act == ACT_FIGHT and len(ob.target) > 0:
                mob = ob.target[0]
        else:
            mName = words[1]
            if words[0] == '.':
                words[0] = '1'
            mob = ob.env.findObjName(words[0])
            if mob == None:
                ob.sendLine('☞ 그런 상대가 없습니다.')
                return
            if is_player(mob) == False and is_mob(mob) == False:
                ob.sendLine('☞ 그런 상대가 없습니다.')
                return
            if mob.act == ACT_DEATH:
                ob.sendLine('☞ 그런 상대가 없습니다.')
                return
            if mob['이름'] != '똥파리' and len(mob.target) != 0 and ob not in mob.target:
                ob.sendLine('☞ 그런 상대가 없습니다.')
                return
            #if mob['몹종류'] == 5:
            #    ob.sendLine('☞ 강호에는 공격할 수 있는것과 없는것이 있지!')
            #    return
        """
        if line in [ '능파미보', '역근경']:
            try:
                cool = ob.cooltime
                if line in cool:
                    c = cool[line]
                else:
                    c = 0
                    cool[line] = 0
            except:
                ob.cooltime = {}
                cool = ob.cooltime
                cool[line] = 0
                c = 0
            for c1 in cool:
                if cool[c1] == 1:
                    ob.sendLine('[1;37m당신의 내가진기가 흩어지며 기의 순환이 멈추어 버립니다.[0;37m')
                    return
            if c != 0:
                ob.sendLine('[1;37m당신의 내가진기가 흩어지며 기의 순환이 멈추어 버립니다.[0;37m')
                return
            if ob['내공'] < 1000:
                ob.sendLine('[1;37m당신의 내가진기가 흩어지며 기의 순환이 멈추어 버립니다.[0;37m')
                return

            ob['내공'] -= 1000

            from twisted.internet import reactor
            if line == '능파미보':
                ob._miss += 350
                ob.sendLine('당신이 발걸음을 [1;37m交叉[0;37m하며 [1;36m凌波微步[;37m를 재빨리 펼쳐냅니다.')
                reactor.callLater(2, self.cool1, ob, line)
            elif line == '역근경':
                ob._arm += 500
                ob._maxhp += 50
                ob._str += 500
                ob.sendLine('당신이 [1;33m易筋經[0;37m의 모든 [1;32m運氣行功[0;37m [1;31m要訣[0;37m을 펼쳐냅니다.')
                reactor.callLater(3, self.cool1, ob, line)

            ob.cooltime[line] = 1
            return
        """
        s = None
        if mName in ob.skillList:
            s = MUGONG[mName]
        else:
            for sName in ob.skillList:
                if sName.find(mName) == 0:
                    s = MUGONG[sName]
                    break
        if s == None:
            ob.sendLine('☞ 그런 무공을 습득한 적이 없습니다.')
            return
        if s == '':
            ob.sendLine('☞ 아직 사용할 수 없는 무공입니다.')
            return
        
        if s['종류'] == '전투':
            if l == 1 and ob.act == ACT_STAND:
                ob.sendLine('☞ 무공을 펼칠 수 있는 상대가 필요합니다.')
                return
            if is_item(mob) or is_box(mob):
                ob.sendLine('☞ 강호에는 공격할 수 있는것과 없는것이 있지!')
                return
            if ob.skill != None:
                ob.sendLine('[1;37m당신의 내가진기가 흩어지며 기의 순환이 멈추어 버립니다.[0;37m')
                return
            if ob.act == ACT_FIGHT and mob not in ob.target:
                ob.sendLine('☞ 현재의 비무에 신경을 집중하세요. @_@')
                return
            if is_player(mob) and ob.env.checkAttr('사용자전투금지'):
                ob.sendLine('☞ 지금은 [1m[31m살겁[0m[37m[40m을 일으키기에 부적합한 상황 이라네')
                return
            # 사용자 전투 지원시 삭제
            if is_player(mob):
                ob.sendLine('☞ 강호에는 공격할 수 있는것과 없는것이 있지!')
                return
            if mob not in ob.target and mob['몹종류'] != 1:
                ob.sendLine('☞ 강호에는 공격할 수 있는것과 없는것이 있지!')
                return
            if ob.getMp() < s.mp or ob['체력'] <  (ob['최고체력'] * s.hp) / 100 or ob['체력'] < (ob['최고체력'] * s.maxhp) / 100:
                ob.sendLine('[1;37m당신이 내공진기를 끌어 모으지만 기가 흩어져 버립니다.[0;37m')
                return
            ob['내공'] -= s.mp
            ob['체력'] -=  (ob['최고체력'] * s.hp) / 100
            ob.getSkill(s.name)
            ob.skill.init()
            
            buf1, buf2, buf3 = ob.makeFightScript(s['무공스크립'], mob)
            ob.sendLine(buf1)
            ob.addStr(s.bonus, False)
            if ob.act == ACT_STAND:
                ob.sendRoom(buf3, noPrompt = True)
            else:
                ob.sendRoomFightScript(buf3)
            if mob not in ob.target:
                ob.setFight(mob)
            if ob.getDex() >= 4200:
                ob._advance = True
                ob.doFight(True)
        else:
            if l == 1:
                mob = ob
            attr = s['속성']
            if '자신금지' in attr and mob == ob:
                ob.sendLine('☞ 자신에게 사용할 수 없는 무공입니다. ^^')
                return
            if '타인금지' in attr and mob != ob:
                ob.sendLine('☞ 자신만 사용할 수 있는 무공입니다. ^^')
                return
            if is_item(mob) or is_box(mob):
                ob.sendLine('☞ 강호에는 공격할 수 있는것과 없는것이 있지!')
                return
            for ss in mob.skills:
                # 같은 무공 혹은 같은 계열의 무공을 두번이상 사용할수 없다. 속성에서 계열금지를 가져온뒤 비교필요
                if s.name == ss.name or s['계열'] == ss.getAntiType():
                    ob.sendLine('[1m당신이 내공진기를 끌어 모으지만 기가 흩어져 버립니다.[0;37m')
                    return
            for ss in ob.skills:
                # 같은 무공 혹은 같은 계열의 무공을 두번이상 사용할수 없다. 속성에서 계열금지를 가져온뒤 비교필요
                if s.name == ss.name or s['계열'] == ss.getAntiType():
                    ob.sendLine('[1m당신이 내공진기를 끌어 모으지만 기가 흩어져 버립니다.[0;37m')
                    return
            if ob.getMp() < s.mp:
                ob.sendLine('[1m당신이 내공진기를 끌어 모으지만 기가 흩어져 버립니다.[0;37m')
                return
            if  ob['체력'] < (ob['최고체력'] * s.hp) / 100 or ob['체력'] < (ob['최고체력'] * s.maxhp) / 100:
                ob.sendLine('[1m당신의 내공진기가 흩어지며 기의 순환이 멈추어 버립니다.[0;37m')
                return
            ob['내공'] -= s.mp
            ob['체력'] -= (ob['최고체력'] * s.hp) / 100
            s = copy.copy(s)
            ob.skillUp(s)
            t = ob.skillMap[s.name][0]
            
            mob._str += s._str
            mob._dex += s._dex
            mob._arm += s._arm
            against = ''
            for at in attr:
                if at.find('상대무공') == 0:
                    aName = at[9:]
                    against = MUGONG[aName].clone()
                    break
            
            if against != '':
                chance = ob.getAttackChance(mob)

                if s['계열'] == '내공흡수' and mob.getMp() > 0:
                    if chance >= randint(0, 100):
                        try:
                            plus = mob.mp * against._mp / 100 * -1
                            if plus + ob['내공'] > ob['최고내공']:
                                plus = ob['최고내공'] - ob['내공']
                            ob['내공'] += plus
                            mob.mp -= plus
                        except:
                            plus = mob['내공'] * against._mp / 100 * -1
                            if plus + ob['내공'] > ob['최고내공']:
                                plus = ob['최고내공'] - ob['내공']
                            ob['내공'] += plus
                            mob['내공'] -= plus
                elif s['계열'] == '내공감소':    
                    mob._mp += against._mp
                    mob._maxmp += against._maxmp
                    mob.skills.append(against)
                    if is_mob(mob):
                        against.end_time = time.time() + against['방어시간'] + against['방어시간증가치'] * (t - 1)
                    else:
                        against.start_time = against['방어시간'] + against['방어시간증가치'] * (t - 1)
                ob.skills.append(s)
            else:
                mob.skills.append(s)
                
            
            
            if is_mob(mob):
                s.end_time = time.time() + s['방어시간'] + s['방어시간증가치'] * (t - 1)
            s.start_time = s['방어시간'] + s['방어시간증가치'] * (t - 1)
            buf1, buf2, buf3 = ob.makeFightScript(s['무공스크립'], mob)
            try:
                ob.sendLine(buf1 + ' ([1;36m+ %d[0;37m)' % plus)
            except:
                ob.sendLine(buf1)

#if mob != ob:
#                mob.sendLine(buf2)
#                mob.lpPrompt()
                
            if mob != ob and is_player(mob):
                mob.sendLine('\r\n' + buf2)
                mob.lpPrompt()
                ob.sendFightScriptRoom(buf3, ex = mob)
            else:
                ob.sendFightScriptRoom(buf3)
