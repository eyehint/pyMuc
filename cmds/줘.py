from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        words = line.split()
        if len(words) < 2:
            ob.sendLine('☞ 사용법: [대상] [물품] 주다')
            return
        if words[1] == '은전':
            obj = ob.env.findObjName(words[0])
            if obj == None or is_player(obj) == False:
                ob.sendLine('☞ 물품을 건내줄 무림인을 찾을 수 없어요. ^^')
                return
            if len(words) < 3:
                cnt = 1
            else:
                cnt = getInt(words[2])
                if cnt <= 0:
                    cnt = 1
            if ob['은전'] == 0:
                ob.sendLine('☞ 돈이 모자라네요. ^^')
                return
            if ob['은전'] < cnt:
                cnt = ob['은전']
            ob['은전'] -= cnt
            obj['은전'] += cnt
            ob.sendLine('당신이 %s에게 은전 %d개를 줍니다.' % (obj.getNameA(), cnt))
            obj.sendLine('\r\n%s 당신에게 은전 %d개를 줍니다.' % (ob.han_iga(), cnt))
            obj.lpPrompt()
            ob.sendRoom('%s %s에게 은전 %d개를 줍니다.' % (ob.han_iga(), obj.getNameA(), cnt), ex = obj)
            return
        if words[1] == '금전':
            obj = ob.env.findObjName(words[0])
            if obj == None or is_player(obj) == False:
                ob.sendLine('☞ 물품을 건내줄 무림인을 찾을 수 없어요. ^^')
                return
            if len(words) < 3:
                cnt = 1
            else:
                cnt = getInt(words[2])
                if cnt <= 0:
                    cnt = 1
            if ob['금전'] == '':
                ob['금전'] = 0
            if ob['금전'] == 0:
                ob.sendLine('☞ 돈이 모자라네요. ^^')
                return
            if ob['금전'] < cnt:
                cnt = ob['금전']
            ob['금전'] -= cnt
            if obj['금전'] == '':
                obj['금전'] = 0
          
            obj['금전'] += cnt
            ob.sendLine('당신이 %s에게 금전 %d개를 줍니다.' % (obj.getNameA(), cnt))
            obj.sendLine('\r\n%s 당신에게 금전 %d개를 줍니다.' % (ob.han_iga(), cnt))
            obj.lpPrompt()
            ob.sendRoom('%s %s에게 금전 %d개를 줍니다.' % (ob.han_iga(), obj.getNameA(), cnt), ex = obj)
            return
        name = words[1]
        
        order = getInt(name)
        if order != 0:
            for i in range( len(name) ):
                if name[i].isdigit() == False:
                    name = name[i:]
                    break
        else:
            order = 1
        #print order, name
        
        obj = ob.findObjName(name, order)
        if obj == None:
            ob.sendLine('☞ 그런 아이템이 소지품에 없어요.')
            return
        name = obj['이름']
        target = ob.env.findObjName(words[0])
        if target == None or not is_player(target):
            ob.sendLine('☞ 물품을 건내줄 무림인을 찾을 수 없어요. ^^')
            return
        if target == ob:
            ob.sendLine('당신이 [36m' + obj['이름'] + '[37m' + han_obj(obj['이름']) + ' 가지고 장난합니다. \'@_@\'')
            return
        i = 1
        c = 0
        if len(words) >= 3:
            i = getInt(words[2])
        if i < 1:
            i = 1
        if i > 50:
            i = 50
        if order != 1:
            i = 1
        objs = copy.copy(ob.objs)
        n = 0
        for obj in objs:
            if c >= i:
                break
            if not(name == obj.get('이름') or name in obj['반응이름']):
                continue
            if obj.checkAttr('아이템속성', '출력안함'):
                continue
            if obj.inUse:
                continue
            n += 1
            if n < order:
                continue
            if obj.checkAttr('아이템속성', '줄수없음'):
                if c == 0:
                    ob.sendLine('☞ 그 물건은 줄 수 없어요. ^^')
                    return
                continue
            if target.getItemWeight() + obj['무게'] > target.getStr() * 10:
                if c == 0:
                    ob.sendLine('[1m' + target['이름'] + '[0;37m' + han_iga(target['이름']) + \
                        ' 무거워서 받지 못합니다.')
                    target.sendLine('\r\n[1m' + ob['이름'] + '[0;37m' + han_iga(ob['이름']) + ' 줄려는 ' + 
                        '[36m' + obj['이름'] + '[37m' + han_obj(obj['이름']) + ' 무거워서 받지 못합니다.')
                    target.lpPrompt()
                    return
                break
            if target.getItemCount() >= getInt(MAIN_CONFIG['사용자아이템갯수']):
                if c == 0:
                    ob.sendLine('[1m' + target['이름'] + '[0;37m' + han_iga(target['이름']) + \
                        ' 수량 한계로 받지 못합니다.')
                    target.sendLine('\r\n[1m' + ob['이름'] + '[0;37m' + han_iga(ob['이름']) + ' 줄려는 ' + \
                        '[36m' + obj['이름'] + '[37m' + han_obj(obj['이름']) + ' 수량 한계로 받지 못합니다.')
                    target.lpPrompt()
                    return
                break
            c += 1
            ob.remove(obj)
            target.insert(obj)
            if obj.isOneItem():
                ONEITEM.have(obj.index, target['이름'])

        if c == 0:
            ob.sendLine('☞ 그런 아이템이 소지품에 없어요.')
        elif c == 1:
            ob.sendLine('당신이 [1m' + target['이름'] + '[0;37m에게 [36m' + name + '[37m' + han_obj(name) + ' 줍니다.')
            target.sendLine('\r\n[1m' + ob['이름'] + '[0;37m' + han_iga(ob['이름']) + ' 당신에게 [36m' + name + '[37m' + han_obj(name) + ' 줍니다.')
            ob.sendRoom('%s %s에게 [36m%s[37m%s 줍니다.' % ( ob.han_iga(), target.getNameA(), name, han_obj(name)), ex = target)
            target.lpPrompt()
        else:
            ob.sendLine('당신이 [1m' + target['이름'] + '[0;37m에게 [36m' + name + '[37m' + ' %d개를 줍니다.' % c)
            target.sendLine('\r\n[1m' + ob['이름'] + '[0;37m' + han_iga(ob['이름']) + ' 당신에게 [36m' + name + '[37m' + ' %d개를 줍니다.' % c)
            target.lpPrompt()
            ob.sendRoom('%s %s에게 [36m%s[37m %d개를 줍니다.' % ( ob.han_iga(), target.getNameA(), name, c), ex = target)


