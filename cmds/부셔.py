# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('☞ 사용법: [물품이름] [수량] 부숴')
            return
        i = 1
        c = 0
        
        args = line.split()
        if len(args) >= 2:
            i = getInt(args[1])
        if i < 1:
            i = 1
        if i > 100:
            i = 100
        name = args[0]
        order = getInt(name)
        if order != 0:
            for i in range( len(name) ):
                if name[i].isdigit() == False:
                    name = name[i:]
                    break
        else:
            order = 1
        if order != 1:
            i = 1
        objs = copy.copy(ob.objs)
        n = 0
        for obj in objs:
            if c >= i:
                break
            if name != obj.get('이름') and name not in obj.get('반응이름').splitlines():
                continue
            if obj.checkAttr('아이템속성', '출력안함'):
                continue
            if obj.inUse:
                continue
            
            n += 1
            if n < order:
                continue
            if obj.checkAttr('아이템속성', '부수지못함'):
                if c == 0:
                    ob.sendLine('☞ 부셔지지 않네요. ^^')
                    return
                continue
            c += 1
            name = obj['이름']
            ob.remove(obj)
            if obj.isOneItem():
                ONEITEM.destroy(obj.index)
        if c == 0:
            ob.sendLine('☞ 그런 아이템이 소지품에 없어요.')
        elif c == 1:
            ob.sendLine('당신이 [36m%s[37m%s 부셔버립니다.' % (name, han_obj(name)))
            ob.sendRoom('%s [36m%s[37m%s 부셔버립니다.' % (ob.han_iga(), name, han_obj(name)))
        else:
            ob.sendLine('당신이 [36m%s[37m %d개를 부셔버립니다.' % (name, c))
            ob.sendRoom('%s [36m%s[37m %d개를 부셔버립니다.' % (ob.han_iga(), name, c))
