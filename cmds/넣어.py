from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        words = line.split()
        if len(line) == 0 or len(words) < 2:
            ob.sendLine('☞ 사용법: [보관함이름] [물품] 넣어')
            return
        box = ob.env.findObjName(words[0])
        if box == None or is_box(box) == False:
            ob.sendLine('☞ 당신의 안광으로는 그런것을 볼수 없다네')
            return
            
        if words[1] == '은전':
            if box.isExpandable() == False:
                ob.sendLine('☞ 더 이상 수량의 증가가 안되요. ^^')
                return
            if len(words) < 3:
                m = 1
            else:
                m = getInt(words[2])
            if m <= 0:
                m = 1
            if ob['은전'] < m:
                ob.sendLine('☞ 돈이 모자라네요. ^^')
                return
            n = box.addMoney(m)
            ob['은전'] -= n
            ob.sendLine('당신이 %s에 은전 %d개를 보관합니다.' % ( box.getNameA(), n ))
            ob.sendRoom('%s %s에 은전 %d개를 보관합니다.' % ( ob.han_iga(), box.getNameA(), n))
            box.save()
            return
        if words[1] == '모두':
            objs = copy.copy(ob.objs)
            c = 0
            nCnt = {}
            for item in objs:
                if box.isFull():
                    if c == 0:
                        ob.sendLine('☞ 보관함에 더 이상 넣을 수 없어요. ^^')
                        return
                    break
                if item['종류'] not in box['보관종류']:
                    continue
                if item.checkAttr('아이템속성', '보관못함'):
                    continue
                if box.checkAttr('아이템속성', '공용보관함') and \
                    (item.checkAttr('아이템속성', '줄수없음') or \
                    item.checkAttr('아이템속성', '버리지못함') or \
                    item.checkAttr('아이템속성', '팔지못함') or \
                    item.checkAttr('아이템속성', '부수지못함')):
                    continue
                if item.inUse:
                    continue
                ob.remove(item)
                box.insert(item)
                if item.isOneItem():
                    ONEITEM.keep(item.index, ob['이름'] + ' %s' % box['이름'])
                nc = 0
                try:
                    nc = nCnt[item['이름']]
                except:
                    nCnt[item['이름']] = 0
                nCnt[item['이름']] = nc + 1
                c += 1
            if c == 0:
                ob.sendLine('☞ 더이상 보관할 물건이 없어요. ^^')
                return
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('당신이 %s에 [36m%s[37m%s 보관합니다.' % (box.getNameA(), name, han_obj(name)))
                        msg += '%s %s에 [36m%s[37m%s 보관합니다.\r\n' % (ob.han_iga(), box.getNameA(), name, han_obj(name))
                    else:
                        ob.sendLine('당신이 %s에 [36m%s[37m %d개를 보관합니다.' % (box.getNameA(), name, nc))
                        msg += '%s %s에 [36m%s[37m %d개를 보관합니다.\r\n' % (ob.han_iga(), box.getNameA(), name, nc)
                ob.sendRoom(msg[:-2])
            box.save()
            return
        if words[1] == '속성아이템':
            objs = copy.copy(ob.objs)
            c = 0
            nCnt = {}
            for item in objs:
                if box.isFull():
                    if c == 0:
                        ob.sendLine('☞ 보관함에 더 이상 넣을 수 없어요. ^^')
                        return
                    break
                if item['종류'] not in box['보관종류']:
                    continue
                if item.checkAttr('아이템속성', '보관못함'):
                    continue
                if box.checkAttr('아이템속성', '공용보관함') and \
                    (item.checkAttr('아이템속성', '줄수없음') or \
                    item.checkAttr('아이템속성', '버리지못함') or \
                    item.checkAttr('아이템속성', '팔지못함') or \
                    item.checkAttr('아이템속성', '부수지못함')):
                    continue
                if item.inUse:
                    continue
                if item.getOption() == None:
                    continue
                ob.remove(item)
                box.insert(item)
                if item.isOneItem():
                    ONEITEM.keep(item.index, ob['이름'] + ' %s' % box['이름'])
                nc = 0
                try:
                    nc = nCnt[item['이름']]
                except:
                    nCnt[item['이름']] = 0
                nCnt[item['이름']] = nc + 1
                c += 1
            if c == 0:
                ob.sendLine('☞ 더이상 보관할 물건이 없어요. ^^')
                return
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('당신이 %s에 [36m%s[37m%s 보관합니다.' % (box.getNameA(), name, han_obj(name)))
                        msg += '%s %s에 [36m%s[37m%s 보관합니다.\r\n' % (ob.han_iga(), box.getNameA(), name, han_obj(name))
                    else:
                        ob.sendLine('당신이 %s에 [36m%s[37m %d개를 보관합니다.' % (box.getNameA(), name, nc))
                        msg += '%s %s에 [36m%s[37m %d개를 보관합니다.\r\n' % (ob.han_iga(), box.getNameA(), name, nc)
                ob.sendRoom(msg[:-2])
            box.save()
            return
        if words[1] == '약초':
            objs = copy.copy(ob.objs)
            c = 0
            nCnt = {}
            for item in objs:
                if box.isFull():
                    if c == 0:
                        ob.sendLine('☞ 보관함에 더 이상 넣을 수 없어요. ^^')
                        return
                    break
                if item['종류'] not in box['보관종류']:
                    continue
                if item.checkAttr('아이템속성', '보관못함'):
                    continue
                if box.checkAttr('아이템속성', '공용보관함') and \
                    (item.checkAttr('아이템속성', '줄수없음') or \
                    item.checkAttr('아이템속성', '버리지못함') or \
                    item.checkAttr('아이템속성', '팔지못함') or \
                    item.checkAttr('아이템속성', '부수지못함')):
                    continue
                if item.inUse:
                    continue
                if item['구매이름'] != '약초':
                    continue
                ob.remove(item)
                box.insert(item)
                if item.isOneItem():
                    ONEITEM.keep(item.index, ob['이름'] + ' %s' % box['이름'])
                nc = 0
                try:
                    nc = nCnt[item['이름']]
                except:
                    nCnt[item['이름']] = 0
                nCnt[item['이름']] = nc + 1
                c += 1
            if c == 0:
                ob.sendLine('☞ 더이상 보관할 물건이 없어요. ^^')
                return
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('당신이 %s에 [36m%s[37m%s 보관합니다.' % (box.getNameA(), name, han_obj(name)))
                        msg += '%s %s에 [36m%s[37m%s 보관합니다.\r\n' % (ob.han_iga(), box.getNameA(), name, han_obj(name))
                    else:
                        ob.sendLine('당신이 %s에 [36m%s[37m %d개를 보관합니다.' % (box.getNameA(), name, nc))
                        msg += '%s %s에 [36m%s[37m %d개를 보관합니다.\r\n' % (ob.han_iga(), box.getNameA(), name, nc)
                ob.sendRoom(msg[:-2])
            box.save()
            return
        itm = None 
        item = ob.findObjInven(words[1])
        if item == None:
            name, order = getNameOrder(words[1])
            itm = item = ob.findObjInven(name, order) 
            if item == None:
                ob.sendLine('☞ 그런 아이템이 소지품에 없어요.')
                return
            
        if item['종류'] not in box['보관종류']:
            ob.sendLine('☞ 보관 할 수 없는 물품입니다. ^^')
            return
        
        if item.checkAttr('아이템속성', '보관못함'):
            ob.sendLine('☞ 보관 할 수 없는 물품입니다. ^^')
            return
            
        if box.checkAttr('아이템속성', '공용보관함') and \
            (item.checkAttr('아이템속성', '줄수없음') or \
            item.checkAttr('아이템속성', '버리지못함') or \
            item.checkAttr('아이템속성', '팔지못함') or \
            item.checkAttr('아이템속성', '부수지못함')):
                ob.sendLine('☞ 보관 할 수 없는 물품입니다. ^^')
                return
        count = 1
        if len(words) > 2:
            count = getInt(words[2])
        
        if itm != None:
            count = 1
        objs = copy.copy(ob.objs)
        c = 0
        nCnt = {}
        oCnt = 1
        for item in objs:
            if itm == None:
                if words[1] != item['이름'] and words[1] not in item['반응이름']:
                    continue
            else:
                if name != item['이름'] and name not in item['반응이름']:
                    continue

            if itm != None:
                if order != oCnt:
                    oCnt += 1
                    continue

            if box.isFull():
                if c == 0:
                    ob.sendLine('☞ 보관함에 더 이상 넣을 수 없어요. ^^')
                    return
                break
            if item['종류'] not in box['보관종류']:
                continue
            if item.checkAttr('아이템속성', '보관못함'):
                continue
            if item.inUse:
                continue
            ob.remove(item)
            box.insert(item)
            if item.isOneItem():
                ONEITEM.keep(item.index, ob['이름'] + ' %s' % box['이름'])
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
            ob.sendLine('☞ 더이상 보관할 물건이 없어요. ^^')
            return
        else:
            msg = ''
            for name in nCnt:
                nc = nCnt[name]
                if nc == 1:
                    ob.sendLine('당신이 %s에 [36m%s[37m%s 보관합니다.' % (box.getNameA(), name, han_obj(name)))
                    msg += '%s %s에 [36m%s[37m%s 보관합니다.\r\n' % (ob.han_iga(), box.getNameA(), name, han_obj(name))
                else:
                    ob.sendLine('당신이 %s에 [36m%s[37m %d개를 보관합니다.' % (box.getNameA(), name, nc))
                    msg += '%s %s에 [36m%s[37m %d개를 보관합니다.\r\n' % (ob.han_iga(), box.getNameA(), name, nc)
            ob.sendRoom(msg[:-2])
        box.save()
        
