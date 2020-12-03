# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line != '' and getInt(ob['�����ڵ��']) >= 1000:
            target = ob.env.findObjName(line)
            if target == None or is_item(target):
                ob.sendLine('�� ����� �ȱ����δ� �׷����� ���� ���ٳ�')
                return
        else:
            target = ob
        
        ob.sendLine('������������������������������������������������������������')
        buf = ' [1m[32m�� [37m%s[0;37m�� �������� ���� [1m[32m��[0m[37m' % target['�̸�']
        ob.sendLine(buf)
        
        if len(target.skills) == 0:
            ob.sendLine('������������������������������������������������������������')
            ob.sendLine(MAIN_CONFIG['������������'])
            ob.sendLine('������������������������������������������������������������')
            return
        ob.sendLine('������������������������������������������������������������')
        for s in target.skills:
            inc = 1
            if s.name in target.skillMap:
                inc = target.skillMap[s.name][0]
            n = s['���ð�'] + s['���ð�����ġ'] * (inc - 1)
            t = s.start_time
            cnt = len(target.strBar)
            a = t * 10 / n
            if a < 0:
                a = 0
            if a >= cnt:
                a = cnt - 1
            buf = '%5d��%s' % (t, target.strBar[a])
            ob.sendLine('[1m[40m[36m��[0m[40m[37m%-14s��%-12s�� %s' % (s.name, s['���������'], buf)) 
        ob.sendLine('������������������������������������������������������������')
