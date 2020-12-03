# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            ob.sendLine('�� ����: [�⿬�̸�] �⿬����')
            return
            
        msg = ''
        if line not in ONEITEM.index:
            ob.sendLine('�� �׷� �������� �����ϴ�.!')
            return
        index = ONEITEM.index[line]
        owner = ONEITEM[index]
        words = owner.split()
        if len(words) == 1:
            who = owner
            where = ''
        elif len(words) == 3:
            who = words[0]
            where = words[1]
        else:
            ob.sendLine('�ƹ��� �����ϰ� ���� �ʽ��ϴ�.!')
            return
        for obj in ob.channel.players:
            if obj['�̸�'] == who:
                ob.sendLine('����ڰ� �������Դϴ�.!')
                return
        if where == '':
            player = Player()
            if player.load(who) == False:
                ob.sendLine('���������ʴ� ������Դϴ�.')
                return
            last = player['����������ð�']
            if last != '' and time.time() - last < 259200:
                ob.sendLine('���� 3���� ������� �ʾҽ��ϴ�.')
                return
            for obj in player.objs:
                print obj['�̸�']
                if obj.index == index:
                    player.objs.remove(obj)
                    player.save(False)
                    ob.sendLine('%s�� %s%s �����Ͽ����ϴ�.' % (who, line, han_obj(line)))
                    del player
                    ONEITEM.attr.__delitem__(index)
                    ONEITEM.save()
                    return
        else:
            pass
        ob.sendLine('%s %s' % (who, where))
        ONEITEM.attr.__delitem__(index)
        ONEITEM.save()

