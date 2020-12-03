# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('☞ 사용법: [아이템 이름] 주워')
            return

        if line == '모두' or line == '전부':
            cnt = 0
            nCnt = {}
            objs = copy.copy(ob.env.objs)
            for obj in objs:
                if is_item(obj) == False:
                    continue
                if ob.getItemWeight() + obj['무게'] > ob.getStr() * 10:
                    continue
                if ob.getItemCount() > getInt(MAIN_CONFIG['사용자아이템갯수']):
                    break
                ob.env.remove(obj)
                if obj.isOneItem():
                    ONEITEM.have(obj.index, ob['이름'])
                ob.insert(obj)
                nc = 0
                try:
                    nc = nCnt[obj.get('이름')]
                except:
                    nCnt[obj.get('이름')] = 0
                nCnt[obj.get('이름')] = nc + 1
                cnt = cnt + 1
            if cnt == 0:
                ob.sendLine('☞ 더이상 가질 물건이 없다네')
                return
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('당신이 [36m' + name + '[37m' + han_obj(name) + ' 집어서 품속에 갈무리 합니다.')
                        msg += '%s [36m%s[37m%s 집어서 품속에 갈무리 합니다.\r\n' % (ob.han_iga(), name, han_obj(name))
                    else:
                        ob.sendLine('당신이 [36m' + name + '[37m %d개를 집어서 품속에 갈무리 합니다.' % nc)
                        msg += '%s [36m%s[37m %d개를 집어서 품속에 갈무리 합니다.\r\n' % (ob.han_iga(), name, nc)
                ob.sendRoom(msg[:-2])
        else:
            i = 1
            c = 0
            nCnt = {}
            args = line.split()
            if len(args) >= 2:
                i = getInt(args[1])
            if i < 1:
                i = 0
            if i > 100:
                i = 50
            for j in range(i):
                obj = ob.env.findObjName(args[0])
                if obj == None:
                    break
                if is_item(obj) == False:
                    ob.sendLine('☞ 강호에 그런 물건은 존재하지 않는다네')
                    return
                if ob.getItemWeight() + obj['무게'] > ob.getStr() * 10:
                    if c == 0:
                        ob.sendLine('☞ 자네의 힘으로는 더이상 가질 수 없다네')
                        return
                    break
                if ob.getItemCount() > getInt(MAIN_CONFIG['사용자아이템갯수']):
                    if c == 0:
                        ob.sendLine('☞ 자네가 가질 물품의 한계라네')
                        return
                    break
                c += 1
                ob.env.remove(obj)
                if obj.isOneItem():
                    ONEITEM.have(obj.index, ob['이름'])
                ob.insert(obj)
                nc = 0
                try:
                    nc = nCnt[obj.get('이름')]
                except:
                    nCnt[obj.get('이름')] = 0
                nCnt[obj.get('이름')] = nc + 1
                #ob.sendLine('당신이 [36m' + obj.get('이름') + '[37m' + han_obj(obj.get('이름')) + ' 집어서 품속에 갈무리 합니다.')
            if c == 0:
                ob.sendLine('☞ 강호에 그런 물건은 존재하지 않는다네')
                return
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('당신이 [36m' + name + '[37m' + han_obj(name) + ' 집어서 품속에 갈무리 합니다.')
                        msg += '%s [36m%s[37m%s 집어서 품속에 갈무리 합니다.\r\n' % (ob.han_iga(), name, han_obj(name))
                    else:
                        ob.sendLine('당신이 [36m' + name + '[37m %d개를 집어서 품속에 갈무리 합니다.' % nc)
                        msg += '%s [36m%s[37m %d개를 집어서 품속에 갈무리 합니다.\r\n' % (ob.han_iga(), name, nc)
                ob.sendRoom(msg[:-2])

