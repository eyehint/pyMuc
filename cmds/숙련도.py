# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        ob.sendLine('[1m ★ 당신의 무기 숙련도 ★[0m[40m[37m')
        ob.sendLine('┏─────┬─────┓')
        ob.sendLine('│◁  검  ▷│[1m%10d[0m[40m[37m│' % getInt(ob['1 숙련도']))
        ob.sendLine('├─────┼─────┤')
        ob.sendLine('│◁  도  ▷│[1m%10d[0m[40m[37m│' % getInt(ob['2 숙련도']))
        ob.sendLine('├─────┼─────┤')
        ob.sendLine('│◁  창  ▷│[1m%10d[0m[40m[37m│' % getInt(ob['3 숙련도']))
        ob.sendLine('├─────┼─────┤')
        ob.sendLine('│◁ 기타 ▷│[1m%10d[0m[40m[37m│' % getInt(ob['4 숙련도']))
        ob.sendLine('├─────┼─────┤')
        ob.sendLine('│◁ 맨손 ▷│[1m%10d[0m[40m[37m│' % getInt(ob['5 숙련도']))
        ob.sendLine('┗─────┴─────┛')

