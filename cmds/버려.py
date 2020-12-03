# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('☞ 사용법: [아이템 이름] 버려')
            return
        
        if ob.env == None:
            ob.sendLine('☞ 아무것도 버릴수 없습니다.')
            return
            
        if line.find('은전') == 0:
            ob.sendLine('☞ 은전은 버릴 수 없어요. ^^')
            return
            
        if line == '모두' or line == '전부':
            cnt = 0
            objs = copy.copy(ob.objs)
            nCnt = {}
            nFail = {}
            for obj in objs:
                if is_item(obj):
                    if obj.inUse:
                        continue
                    if obj.checkAttr('아이템속성', '버리지못함'):
                        continue
                    if obj.checkAttr('아이템속성', '출력안함'):
                        continue
                    ob.remove(obj)
                    
                    cnt += 1
                    if ob.env.getItemCount() < 50:
                        ob.env.insert(obj)
                        obj.drop()
                        if obj.isOneItem():
                            ONEITEM.drop(obj.index, ob['이름'])
                        nc = 0
                        try:
                            nc = nCnt[obj.get('이름')]
                        except:
                            nCnt[obj.get('이름')] = 0
                        nCnt[obj.get('이름')] = nc + 1
                    else:
                        if obj.isOneItem():
                            ONEITEM.destroy(obj.index)
                        nc = 0
                        try:
                            nc = nFail[obj.get('이름')]
                        except:
                            nFail[obj.get('이름')] = 0
                        nFail[obj.get('이름')] = nc + 1
                        obj.env = None
                        del obj
            if cnt == 0:
                ob.sendLine('☞ 더이상 버릴 물건이 없다네')
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('당신이 [36m' + name + '[37m' + han_obj(name) + ' 버립니다.')
                        msg += '%s [36m%s[37m%s 버립니다.\r\n' % (ob.han_iga(), name, han_obj(name))
                    else:
                        ob.sendLine('당신이 [36m' + name + '[37m %d개를 버립니다.' % nc)
                        msg += '%s [36m%s[37m %d개를 버립니다.\r\n' % (ob.han_iga(), name, nc)
                for name in nFail:
                    nc = nFail[name]
                    if nc == 1:
                        ob.sendLine('당신이 [36m' + name + '[37m' + han_obj(name) + ' 버리자 바로 부서집니다.')
                        msg += '%s [36m%s[37m%s 버리자 바로 부서집니다.\r\n' % (ob.han_iga(), name, han_obj(name))
                    else:
                        ob.sendLine('당신이 [36m' + name + '[37m %d개를 버리자 바로 부서집니다.' % nc)
                        msg += '%s [36m%s[37m %d개를 버리자 바로 부서집니다.\r\n' % (ob.han_iga(), name, nc)
                ob.sendRoom(msg[:-2])
        else:
            i = 1
            c = 0
            nCnt = {}
            nFail = {}
            
            args = line.split()
            if len(args) >= 2:
                i = getInt(args[1])
            if i < 1:
                i = 1
            if i > 50:
                i = 50
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
                if obj.checkAttr('아이템속성', '버리지못함'):
                    if c == 0:
                        ob.sendLine('☞ 그 물건은 버릴 수 없어요. ^^')
                        return
                    continue
                c += 1
                ob.remove(obj)
                if ob.env.getItemCount() < 50:
                    ob.env.insert(obj)
                    obj.drop()
                    if obj.isOneItem():
                        ONEITEM.drop(obj.index, ob['이름'])
                    nc = 0
                    try:
                        nc = nCnt[obj.get('이름')]
                    except:
                        nCnt[obj.get('이름')] = 0
                    nCnt[obj.get('이름')] = nc + 1
                else:
                    if obj.isOneItem():
                        ONEITEM.destroy(obj.index)
                    nc = 0
                    try:
                        nc = nFail[obj.get('이름')]
                    except:
                        nFail[obj.get('이름')] = 0
                    nFail[obj.get('이름')] = nc + 1
                
                #ob.sendLine('당신이 ' + obj.get('이름') + han_obj(obj.get('이름')) + ' 버립니다.')
            if c == 0:
                ob.sendLine('☞ 그런 아이템이 소지품에 없어요.')
            else:
                msg = ''
                for name in nCnt:
                    nc = nCnt[name]
                    if nc == 1:
                        ob.sendLine('당신이 [36m' + name + '[37m' + han_obj(name) + ' 버립니다.')
                        msg += '%s [36m%s[37m%s 버립니다.\r\n' % (ob.han_iga(), name, han_obj(name))
                    else:
                        ob.sendLine('당신이 [36m' + name + '[37m %d개를 버립니다.' % nc)
                        msg += '%s [36m%s[37m %d개를 버립니다.\r\n' % (ob.han_iga(), name, nc)
                for name in nFail:
                    nc = nFail[name]
                    if nc == 1:
                        ob.sendLine('당신이 [36m' + name + '[37m' + han_obj(name) + ' 버리자 바로 부서집니다.')
                        msg += '%s [36m%s[37m%s 버리자 바로 부서집니다.\r\n' % (ob.han_iga(), name, han_obj(name))
                    else:
                        ob.sendLine('당신이 [36m' + name + '[37m %d개를 버리자 바로 부서집니다.' % nc)
                        msg += '%s [36m%s[37m %d개를 버리자 바로 부서집니다.\r\n' % (ob.han_iga(), name, nc)
                ob.sendRoom(msg[:-2])
