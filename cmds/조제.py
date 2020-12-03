# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('☞ 사용법: [이름] 조제')
            return
        found = False
        doctor = False
        for mob in ob.env.objs:
            if is_mob(mob) == False:
                continue
            if '의원' in mob['반응이름'].splitlines():
                doctor = True
                key = '조제 %s' % line
                if key in mob.attr:
                    found = True
                    break
        if doctor == False:
            ob.sendLine('☞ 이곳에 약을 조제할만한 의원이 없어요. ^^')
            return
        if found == False:
            ob.sendLine('☞ 그러한 것을 조제할 의원이 없어요. ^^')
            return
        take = []
        for l in mob[key].splitlines():
            words = l.split()
            if len(words) < 2:
                continue
            if words[0][0] == '+':
                give = words[0][1:]
                ngive = int(words[1])
            else:
                take.append( (words[0] , int(words[1])) )
        indexs = []
        for obj in ob.objs:
            if obj.inUse:
                continue
            indexs.append(obj.index)
        
        for i in take:
            c = 0
            for j in range(0, i[1]):
                if i[0] in indexs:
                    c += 1
                    indexs.remove(i[0])
                    continue
                break
            if c != i[1]:
                ob.sendLine('%s 말합니다. "음.. 부족한게 있다네... 재료를 더 구해오게나"' % mob.han_iga())
                return
        msg = ''
        items = []
        for i in range(0, ngive):
            item = getItem(give)
            if item == None:
                ob.sendLine('%s 말합니다. "음.. 재료가 다 떨어져서 한동안 조제가 힘들겠어..."' % mob.han_iga())
                return
            item = item.clone()
            items.append(item)
            msg += '%s 당신에게 %s 줍니다.' % (mob.han_iga(), item.han_obj())
        ob.sendLine('당신이 %s에게 [36m%s[37m%s 만들수 있는 재료들을 건네줍니다.' % ( mob.getNameA(), line, han_obj(line)))
        ob.sendLine('%s 재료들을 가지고 심오한 기를 불어 넣으며 작업합니다.'% mob.han_iga())
        ob.sendLine(msg)
        objs = copy.copy(ob.objs)
        for i in take:
            c = 0
            for j in range(0, i[1]):
                self.delItem(ob, i[0]) 
        for i in items:
            ob.insert(i)

    def delItem(self, ob, index):
        for obj in ob.objs:
            if obj.inUse:
                continue
            if obj.index == index:
                ob.objs.remove(obj)
                return
