# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['관리자등급']) < 2000:
            ob.sendLine('☞ 무슨 말인지 모르겠어요. *^_^*')
            return
        
        words = line.split()
        if line == '' or len(words) < 3:
            ob.sendLine('☞ 사용법: [대상] [키] [값] 옵설정')
            return
        name, order = getNameOrder(words[0])
        item = ob.findObjInven(name, order)
        if item == None:
            ob.sendLine('☞ 그런 아이템이 소지품에 없어요.')
            return
        option = item.getOption() 
        if option == None:
            option = {}
        option[words[1]] = int(words[2])

        item.setOption(option)
        ob.sendLine('☞ 설정되었습니다.')
        #n = stripANSI(item['이름'])
        item['이름'] = '[1;34m' + item['이름'] + '[0;37m'

        
