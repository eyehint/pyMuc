# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        from objs.skill import MUGONG
        
        if line == '':
            if ob['자동무공'] == '':
                ob.sendLine('☞ 자동무공 : 없음')
                return
            else:
                ob.sendLine('☞ 자동무공 : [[1;37m%s[0;37m]' % ob['자동무공'])
                return
        s = None
        if line in ob.skillList:
            s = MUGONG[line]
        else:
            for sName in ob.skillList:
                if sName.find(line) == 0:
                    s = MUGONG[sName]
                    break
        if s == None or s == '':
            ob.sendLine('☞ 그런 무공을 습득한 적이 없습니다.')
            return
        if s['종류'] != '전투':
            ob.sendLine('☞ 자동무공을 할 수 없는 무공입니다.')
            return
        ob['자동무공'] = s.name
        ob.sendLine('☞ 자동무공을 지정하였습니다.')
