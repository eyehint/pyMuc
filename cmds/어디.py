# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) != 0:
            for ply in ob.channel.players:
                if ply.env == None or ply.state != ACTIVE or ply['투명상태'] == 1:
                    continue
                if ply['이름'] == line:
                    ob.sendLine('[1m%-10s[0;37m ▷ %s' % ( line, ply.env['이름']))
                    return
            ob.sendLine('☞ 활동중인 그런 무림인이 없어요. ^^')
            return
        else:
            for ply in ob.channel.players:
                if ply['투명상태'] == 1:
                    continue
                if ply.env != None and ply.env.zone == ob.env.zone:
                    ob.sendLine('[1m%-10s[0;37m ▷ %s' % ( ply['이름'], ply.env['이름']))

