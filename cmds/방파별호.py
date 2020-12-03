from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob['소속'] == '':
            ob.sendLine('☞ 당신은 소속이 없습니다.')
            return
        if ob['직위'] != '방주':
            ob.sendLine('☞ 방파의 방주만이 할 수 있습니다.')
            return
        words = line.split()
        if len(words) != 2:
            ob.sendLine('☞ 사용법 : [대상] [무림별호] 방파별호')
            return
            
        obj = ob.env.findObjName(words[0])
        if obj == None  or is_player(obj) == False:
            ob.sendLine('☞ 이곳에 그런 무림인이 없습니다.')
            return
        if obj['소속'] != ob['소속']:
            ob.sendLine('☞ 당신의 소속이 아닙니다.')
            return
        if obj == ob:
            buf3 = '자신'
        else:
            buf3 = obj['이름']
        if len(words[1]) > 10:
            ob.sendLine('☞ 사용하시려는 별호가 너무 길어요.')
            return
            
        obj['방파별호'] = words[1]
        ob.sendLine('당신이 [1m%s[0;37m의 방파별호를 『[1;32m%s[0;37m』%s 함을 선포합니다.' % (buf3, words[1], han_uro(words[1])))
        ob.sendGroup('%s [1m%s[0;37m의 방파별호를 『[1;32m%s[0;37m』%s 함을 선포합니다.' % (ob.han_iga(), buf3, words[1], han_uro(words[1])), prompt = True, ex = ob)

