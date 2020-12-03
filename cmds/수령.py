# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('�� ����: [�ݾ�] ����')
            return
        mob = ob.env.findObjName('ǥ��')
        if mob == None:
            ob.sendLine('�� �̰��� ǥ�����簡 ���׿�.')
            return
        m = getInt(line)
        if m <= 0:
            ob.sendLine('�� ���� 1�� �̻� �Է� �ϼž� �ؿ�.')
            return
        if ob['����'] > 500:
            ob.sendLine('�� ����� �ɷ��� �־� ���̴µ���???')
            return
        if m > 10000000:
            ob.sendLine('�� �ʹ� ����� ũ����???')
            return
        if m > mob['����']:
            ob.sendLine('�� ��α��� ���߶��^^;')
            return
        if getInt(ob['���ɾ�']) >= 1000000000:
            ob.sendLine('�� ���̻� ������ ����ؿ�^^;')
            return
        if getInt(ob['���ɾ�']) + m >= 1000000000:
            ob.sendLine('�� �ѵ� �ʰ�����!!!')
            return
        if getInt(ob['����������']) + 86400 > time.time():
            ob.sendLine('�� �� ���̾��???')
            return

        ob['����������'] = time.time()
        ob['����'] += m
        ob['���ɾ�'] = getInt(ob['���ɾ�']) + m
        mob['����'] -= m
        msg = '����� ���� %d���� ǥ�����翡�� �����մϴ�.\r\n' % m
        msg += '������� ������ ��α� �Ѿ��� ���� [1m%d[0;37m�� �Դϴ�.' %(ob['���ɾ�'])
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
