# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        msg = ''
        i = 0
        if line ==  '':
            for cfg in ob.CFG:
                msg += '[1m[40m[32m·[0m[40m[37m %-17s' % cfg
                if ob.checkConfig(cfg):
                    msg += '[[1m설  정[0;37m]    '
                else:
                    msg += '[비설정]    '
                i += 1
                if i % 2 == 0:
                    msg += '\r\n'
                
            ob.sendLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
            ob.sendLine('[47m[30m◁               설      정      상      태               ▷[40m[37m')
            ob.sendLine('──────────────────────────────')
            ob.write(msg)
            ob.sendLine('\r\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        else:
            if line not in ob.CFG:
                ob.sendLine('☞ 그런 설정은 없어요. ^^')
                return
            s = ob.checkConfig(line)
            if s:
                msg = '[1m[비설정][0;37m'
            else:
                msg = '[1m[설정][0;37m'
            ob.setConfig(line)
            ob.sendLine('☞ ' + line + han_obj(line) + ' ' + msg + ' 하였습니다.')

