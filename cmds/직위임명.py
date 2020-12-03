from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if ob['직위'] != '방주':
            ob.sendLine('☞ 방파의 방주만이 할 수 있습니다.')
            return
        words = line.split()
        l = ['방주', '부방주', '장로', '방파인']
        if line == '' or len(words) < 2 or words[1] not in l:
            ob.sendLine('☞ 사용법 : [대상] [방주|부방주|장로|방파인] 직위임명')
            return
        obj = ob.env.findObjName(words[0])
        if obj == None:
            ob.sendLine('☞ 이곳에 그런 무림인이 없습니다.')
            return
        if obj == ob:
            ob.sendLine('☞ 자기 자신입니다.')
            return
        if obj['소속'] != ob['소속']:
            ob.sendLine('☞ 당신의 소속이 아닙니다.')
            return
        if obj['직위'] == words[1]:
            ob.sendLine('☞ 같은 직위입니다.')
            return
        g = GUILD[ob['소속']]
        c = MAIN_CONFIG['방파 %s 인원' % words[1]]
        if '%s리스트' % words[1] in g:
            l1 = g['%s리스트' % words[1]]
        else:
            l1 = []
            g['%s리스트' % words[1]] = l1
            
        if c <= len(l1):
            ob.sendLine('☞ 같은 직위의 인원이 너무 많습니다.')
            return
        g['%s리스트' % obj['직위']].remove(obj['이름'])
        g['%s리스트' % words[1]].append(obj['이름'])
        obj['직위'] = words[1]
        GUILD.save()

        msg = '%s %s [1m%s[0m%s 직위를 임명합니다.' % (ob.han_iga(), obj.han_obj(), words[1], han_uro(words[1]))
        ob.sendGroup(msg, prompt = True)
        
