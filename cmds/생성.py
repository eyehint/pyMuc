# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['관리자등급']) < 2000:
            ob.sendLine('☞ 무슨 말인지 모르겠어요. *^_^*')
            return
        if len(line) == 0:
            ob.sendLine('사용법: [아이템 이름] [갯수] 생성')
            return
        var = line.split()
        if len(var) == 1:
            cnt = 1
        else:
            cnt = int(var[1])

        item = getItem(var[0])

        if item == None:
            ob.sendLine('* 생성 실패!!!')
            return
            
        if item.isOneItem():
            if item.isOneThere():
                ob.sendLine('[단일아이템] %s 이미 생성되어 있습니다.' % item.han_iga())
                return
            else:
                ONEITEM.have(item.index, ob['이름'])
        for i in range(cnt):
            item = item.deepclone()
            ob.objs.append(item)
            if item['종류'] == '호위':
                item.hp = item['체력']
        
        ob.sendLine('[1;32m* [' + item.get('이름') + '] 생성 되었습니다.[0;37m')
