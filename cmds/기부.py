# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('�� ����: [�ݾ�] ���')
            return
        mob = ob.env.findObjName('ǥ��')
        if mob == None:
            ob.sendLine('�� �̰��� ǥ�����簡 ���׿�.')
            return
        m = getInt(line)
        if m <= 0:
            ob.sendLine('�� ���� 1�� �̻� �Ա� �ϼž� �ؿ�.')
            return
        if m > ob['����']:
            m = ob['����']
        ob['����'] -= m
        mob['����'] += m
        msg = '����� ���� %d���� ǥ�����翡�� ��Ź�մϴ�.\r\n' % m
        msg += '������� ���� ��α� �Ѿ��� ���� [1m%d[0;37m�� �Դϴ�.' %(mob['����'])
        ob.sendLine(msg)

        msg = '[������]\n\n'
        l = mob.attr.keys()
        l.sort()
        for at in l:
            msg += '#%s\n' % at
            for m in str(mob.attr[at]).splitlines():
                msg += ':%s\n' % m
            msg += '\n'

        try:
            f = open(mob.path, 'w')
        except:
            return False
        f.write(msg)
        f.close()
