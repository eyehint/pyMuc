from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        words = line.split()
        if len(line) == 0 or len(words) < 2:
            ob.sendLine('☞ 사용법: [보관함이름] [물품] 꺼내')
            return
        box = ob.env.findObjName(words[0])
        if box == None or is_box(box) == False:
            ob.sendLine('☞ 당신의 안광으로는 그런것을 볼수 없다네')
            return
            
        if words[1] == '모두':
            objs = copy.copy(box.objs)
            c = 0
            nCnt = {}
            for item in objs:
                if ob.getItemWeight() + item['무게'] > ob.getStr() * 10:
                    if c == 0:
                        ob.sendLine('☞ 자네의 힘으로는 더이상 가질 수 없다네')
                        return
                    break
                if ob.getItemCount() > getInt(MAIN_CONFIG['사용자아이템갯수']):
                    if c == 0:
                        ob.sendLine('☞ 자네가 가질 물품의 한계라네')
                        return
                    break
                box.remove(item)
                ob.insert(item)
                if item.isOneItem():
                    ONEITEM.have(item.index, ob['이름'])
                nc = 0
                try:
                    nc = nCnt[item['이름']]
                except:
                    nCnt[item['이름']] = 0
                nCnt[item['이름']] = nc + 1
                c += 1
            if c == 0:
                ob.sendLine('☞ 더 이상 꺼낼 물건이 없어요. ^^')
                return
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('당신이 %s에서 [36m%s[37m%s 꺼냅니다.' % (box.getNameA(), name, han_obj(name)))
                        msg += '%s %s에서 [36m%s[37m%s 꺼냅니다.\r\n' % (ob.han_iga(), box.getNameA(), name, han_obj(name))
                    else:
                        ob.sendLine('당신이 %s에서 [36m%s[37m %d개를 꺼냅니다.' % (box.getNameA(), name, nc))
                        msg += '%s %s에서 [36m%s[37m %d개를 꺼냅니다.\r\n' % (ob.han_iga(), box.getNameA(), name, nc)
                ob.sendRoom(msg[:-2])
            box.save()
            return
        if words[1] == '약초':
            objs = copy.copy(box.objs)
            c = 0
            nCnt = {}
            for item in objs:
                if item['구매이름'] != '약초':
                    continue
                if ob.getItemWeight() + item['무게'] > ob.getStr() * 10:
                    if c == 0:
                        ob.sendLine('☞ 자네의 힘으로는 더이상 가질 수 없다네')
                        return
                    break
                if ob.getItemCount() > getInt(MAIN_CONFIG['사용자아이템갯수']):
                    if c == 0:
                        ob.sendLine('☞ 자네가 가질 물품의 한계라네')
                        return
                    break
                box.remove(item)
                ob.insert(item)
                if item.isOneItem():
                    ONEITEM.have(item.index, ob['이름'])
                nc = 0
                try:
                    nc = nCnt[item['이름']]
                except:
                    nCnt[item['이름']] = 0
                nCnt[item['이름']] = nc + 1
                c += 1
            if c == 0:
                ob.sendLine('☞ 더 이상 꺼낼 물건이 없어요. ^^')
                return
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('당신이 %s에서 [36m%s[37m%s 꺼냅니다.' % (box.getNameA(), name, han_obj(name)))
                        msg += '%s %s에서 [36m%s[37m%s 꺼냅니다.\r\n' % (ob.han_iga(), box.getNameA(), name, han_obj(name))
                    else:
                        ob.sendLine('당신이 %s에서 [36m%s[37m %d개를 꺼냅니다.' % (box.getNameA(), name, nc))
                        msg += '%s %s에서 [36m%s[37m %d개를 꺼냅니다.\r\n' % (ob.han_iga(), box.getNameA(), name, nc)
                ob.sendRoom(msg[:-2])
            box.save()
            return

        count = 1
        if len(words) > 2:
            count = getInt(words[2])
        item = None 
        order = -1
        if words[1].isdigit():
            idx = getInt(words[1])
            if len(box.objs) - idx >= 0:
                item = box.objs[idx - 1]
                order = 0
                name = item['이름']
        if item == None: 
            item = box.findObjName(words[1])
        if item == None:
            name, order = getNameOrder(words[1])
            item = box.findObjInven(name, order) 
            if item == None:
                ob.sendLine('☞ 그런 물건이 없어요. ^^')
                return
            count = 1
        
        if order != -1 and item != None:
            if ob.getItemWeight() + item['무게'] > ob.getStr() * 10:
                ob.sendLine('☞ 자네의 힘으로는 더이상 가질 수 없다네')
                return
            if ob.getItemCount() > getInt(MAIN_CONFIG['사용자아이템갯수']):
                ob.sendLine('☞ 자네가 가질 물품의 한계라네')
                return
            box.remove(item)
            ob.insert(item)
            if item.isOneItem():
                ONEITEM.have(item.index, ob['이름'])
            ob.sendLine('당신이 %s에서 [36m%s[37m%s 꺼냅니다.' % (box.getNameA(), item['이름'], han_obj(name)))
            msg = '%s %s에서 [36m%s[37m%s 꺼냅니다.\r\n' % (ob.han_iga(), box.getNameA(), item['이름'], han_obj(name))
            ob.sendRoom(msg[:-2])
            box.save()
            return

        objs = copy.copy(box.objs)
        c = 0
        nCnt = {}
        for item in objs:
            if words[1] != item['이름'] and words[1] not in item['반응이름']:
                continue
            if ob.getItemWeight() + item['무게'] > ob.getStr() * 10:
                if c == 0:
                    ob.sendLine('☞ 자네의 힘으로는 더이상 가질 수 없다네')
                    return
                break
            if ob.getItemCount() > getInt(MAIN_CONFIG['사용자아이템갯수']):
                if c == 0:
                    ob.sendLine('☞ 자네가 가질 물품의 한계라네')
                    return
                break
            box.remove(item)
            ob.insert(item)
            if item.isOneItem():
                ONEITEM.have(item.index, ob['이름'])
            nc = 0
            try:
                nc = nCnt[item['이름']]
            except:
                nCnt[item['이름']] = 0
            nCnt[item['이름']] = nc + 1
            c += 1
            if c == count:
                break
        if c == 0:
            ob.sendLine('☞ 더이상 꺼낼 물건이 없어요. ^^')
            return
        else:
            msg = ''
            for name in nCnt:
                nc = nCnt[name]
                if nc == 1:
                    ob.sendLine('당신이 %s에서 [36m%s[37m%s 꺼냅니다.' % (box.getNameA(), name, han_obj(name)))
                    msg += '%s %s에서 [36m%s[37m%s 꺼냅니다.\r\n' % (ob.han_iga(), box.getNameA(), name, han_obj(name))
                else:
                    ob.sendLine('당신이 %s에서 [36m%s[37m %d개를 꺼냅니다.' % (box.getNameA(), name, nc))
                    msg += '%s %s에서 [36m%s[37m %d개를 꺼냅니다.\r\n' % (ob.han_iga(), box.getNameA(), name, nc)
            ob.sendRoom(msg[:-2])
        box.save()
        
