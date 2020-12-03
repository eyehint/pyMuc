# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) != 0:
            for ply in ob.channel.players:
                if ply.env == None or ply.state != ACTIVE or ply['�������'] == 1:
                    continue
                if ply['�̸�'] == line:
                    ob.sendLine('[1m%-10s[0;37m �� %s' % ( line, ply.env['�̸�']))
                    return
            ob.sendLine('�� Ȱ������ �׷� �������� �����. ^^')
            return
        else:
            for ply in ob.channel.players:
                if ply['�������'] == 1:
                    continue
                if ply.env != None and ply.env.zone == ob.env.zone:
                    ob.sendLine('[1m%-10s[0;37m �� %s' % ( ply['�̸�'], ply.env['�̸�']))

