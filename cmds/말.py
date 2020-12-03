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
            ob.sendLine('����� ���մϴ� : \'' + m1 + '\'')
            ob.sendRoom('%s ���մϴ� : \'%s\'' % (ob.han_iga(), m1))
            #ob.sendLine('����� ���մϴ� : \'' + line + '\'')
            #ob.sendRoom('%s ���մϴ� : \'%s\'' % (ob.han_iga(), line))
            #from lib.comm import broadcast
            #tell_room(ob.env, '\r\n* ' + ob.get('�̸�') + ' : ' + line, ob)

    def ANSI(self, msg, conv):
        buf = msg
        if conv == True:
            buf = buf.replace('{��}', '[1m')
            buf = buf.replace('{��}', '[0m')
            buf = buf.replace('{��}', '[30m')
            buf = buf.replace('{��}', '[31m')
            buf = buf.replace('{��}', '[32m')
            buf = buf.replace('{��}', '[33m')
            buf = buf.replace('{��}', '[34m')
            buf = buf.replace('{��}', '[35m')
            buf = buf.replace('{��}', '[36m')
            buf = buf.replace('{��}', '[37m')
            buf = buf.replace('{���}', '[40m')
            buf = buf.replace('{�軡}', '[41m')
            buf = buf.replace('{����}', '[42m')
            buf = buf.replace('{���}', '[43m')
            buf = buf.replace('{����}', '[44m')
            buf = buf.replace('{����}', '[45m')
            buf = buf.replace('{����}', '[46m')
            buf = buf.replace('{����}', '[47m')
        else:
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{��}', '')
            buf = buf.replace('{���}', '')
            buf = buf.replace('{�軡}', '')
            buf = buf.replace('{����}', '')
            buf = buf.replace('{���}', '')
            buf = buf.replace('{����}', '')
            buf = buf.replace('{����}', '')
            buf = buf.replace('{����}', '')
            buf = buf.replace('{����}', '')
        return buf
