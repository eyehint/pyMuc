# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def sayWhat(self, ob):
        ob.sendLine('\r\nSay What???')

    def cmd(self, ob, line):
        if len(line) == 0:
            self.sayWhat(ob)
        else:
            #import time
            #from lib.hangul import han_iga
            #from lib.comm import tell_room
            m1 = self.ANSI(line, True) + '[0;40;37m'
            m2 = self.ANSI(line, False)
            ob.sendLine('당신이 말합니다 : \'' + m1 + '\'')
            ob.sendRoom('%s 말합니다 : \'%s\'' % (ob.han_iga(), m1))
            #ob.sendLine('당신이 말합니다 : \'' + line + '\'')
            #ob.sendRoom('%s 말합니다 : \'%s\'' % (ob.han_iga(), line))
            #from lib.comm import broadcast
            #tell_room(ob.env, '\r\n* ' + ob.get('이름') + ' : ' + line, ob)

    def ANSI(self, msg, conv):
        buf = msg
        if conv == True:
            buf = buf.replace('{밝}', '[1m')
            buf = buf.replace('{어}', '[0m')
            buf = buf.replace('{검}', '[30m')
            buf = buf.replace('{빨}', '[31m')
            buf = buf.replace('{초}', '[32m')
            buf = buf.replace('{노}', '[33m')
            buf = buf.replace('{파}', '[34m')
            buf = buf.replace('{자}', '[35m')
            buf = buf.replace('{하}', '[36m')
            buf = buf.replace('{흰}', '[37m')
            buf = buf.replace('{배검}', '[40m')
            buf = buf.replace('{배빨}', '[41m')
            buf = buf.replace('{배초}', '[42m')
            buf = buf.replace('{배노}', '[43m')
            buf = buf.replace('{배파}', '[44m')
            buf = buf.replace('{배자}', '[45m')
            buf = buf.replace('{배하}', '[46m')
            buf = buf.replace('{배흰}', '[47m')
        else:
            buf = buf.replace('{밝}', '')
            buf = buf.replace('{어}', '')
            buf = buf.replace('{검}', '')
            buf = buf.replace('{빨}', '')
            buf = buf.replace('{초}', '')
            buf = buf.replace('{노}', '')
            buf = buf.replace('{파}', '')
            buf = buf.replace('{자}', '')
            buf = buf.replace('{하}', '')
            buf = buf.replace('{흰}', '')
            buf = buf.replace('{배검}', '')
            buf = buf.replace('{배빨}', '')
            buf = buf.replace('{배초}', '')
            buf = buf.replace('{배노}', '')
            buf = buf.replace('{배파}', '')
            buf = buf.replace('{배자}', '')
            buf = buf.replace('{배하}', '')
            buf = buf.replace('{배흰}', '')
        return buf
