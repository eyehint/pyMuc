# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('☞ 사용법: [아이템 이름] 먹어')
            return
        if ob.act == ACT_REST:
            ob.sendLine('☞ 먹을 수 있는 상황이 아니네요. ^_^')
            return
        name, order = getNameOrder(line)
        item = ob.findObjInven(name, order)
        if item == None:
            ob.sendLine('☞ 그런 아이템이 소지품에 없어요.')
            return
        if item['종류'] != '먹는것':
            ob.sendLine('☞ 먹을 수 있는것이 아니에요. ^_^')
            return
        
        maxHp = ob.getMaxHp()
        maxMp = ob.getMaxMp()
        
        hp = getInt(item['체력'])
        mp = getInt(item['내공'])
        if ob['체력'] + hp > maxHp:
            ob['체력'] = maxHp
        else:
            ob['체력'] += hp
        if ob['내공'] + mp > maxMp:
            ob['내공'] = maxMp
        else:
            ob['내공'] += mp
        
        maxmp = getInt(item['내공증진'])
        if maxmp != 0:
            if item.checkAttr('아이템속성', '내공계속증진') == False:
                if ob.checkAttr('내공증진아이템리스트', item['이름']):
                    maxmp = 0
                else:
                    ob.setAttr('내공증진아이템리스트', item['이름'])
                    ob['최고내공'] += maxmp
            else:
                ob['최고내공'] += maxmp
        msg = item['사용스크립']
        msg = msg.replace('$아이템$', item.getNameA())
        ob.remove(item)
        del item
        ob.sendLine('당신이 %s' % msg)
        
        roomMsg = '%s %s' % ( ob.han_iga(), msg)
        if maxmp > 0:
            ob.sendLine('\r\n[1m당신의 단전에 회오리가 몰아치며 몸주위에 하얀 진기가 맴돕니다.[0;37m ([1;36m+%d[0;37m)' % maxmp)
            roomMsg += '\r\n\r\n[1m%s의 단전에 회오리가 몰아치며 몸주위에 하얀 진기가 맴돕니다.[0;37m ([1;36m+%d[0;37m)' % (ob.getNameA() ,maxmp)
        elif maxmp < 0:
            ob.sendLine('\r\n[1m당신의 단전에 심한 요동이 일어나며 고통이 몰려오기 시작합니다.[0;37m ([1;31m%d[0;37m)' % maxmp)
            roomMsg += '\r\n\r\n[1m%s의 단전에 심한 요동이 일어나며 고통이 몰려오기 시작합니다.[0;37m ([1;31m%d[0;37m)' % (ob.getNameA() ,maxmp)
        ob.sendFightScriptRoom(roomMsg)

        if '연속복용' not in ob.alias:
            return
        if ob.alias['연속복용'] != '켜기':
            return
        if hp == 0:
            return
        if '체력' not in ob.alias or '체력약' not in ob.alias:
            return
        if ob.getHp() < getInt(ob.alias['체력']):
            #print ob.getHp()
            ob.do_command('%s 먹어' % line)
