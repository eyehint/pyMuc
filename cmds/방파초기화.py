# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if line == '':
            ob.sendLine('�� ����: [�����̸�] �����ʱ�ȭ')
            return
            for g in GUILD.attr:
                guild = GUILD.attr[g]
                #���Ŀ����� �ҼӰ� ������ ���־���...
                path = guild['���ĸ�']
                room = getRoom(path)
                if room == None:
                    contimue
                room.attr.__delitem__('��������')
                room.save()
                for r in room['�����Ա�'].splitlines():
                    if r.find(':') == -1:
                        path = room.zone + ':' + r
                    else:
                        path = r
                    enter = getRoom(path)
                    if enter == None:
                        continue
                    enter.attr.__delitem__('��������')
                    enter.save()
            GUILD.attr = {}
            GUILD.save()
        else:
            if line in GUILD.attr:
                guild = GUILD.attr[line]
                #���Ŀ����� �ҼӰ� ������ ���־���...
                path = guild['���ĸ�']
                room = getRoom(path)
                if room == None:
                    contimue
                try:
                    room.attr.__delitem__('��������')
                    room.save()
                except:
                    pass

                for r in room['�����Ա�'].splitlines():
                    if r.find(':') == -1:
                        path = room.zone + ':' + r
                    else:
                        path = r
                    enter = getRoom(path)
                    if enter == None:
                        continue
                    try:
                        enter.attr.__delitem__('��������')
                        enter.save()
                    except:
                        pass
                GUILD.attr.__delitem__(line) 
                GUILD.save()
            else:
                ob.sendLine('* �׷� ���İ� �����ϴ�.')
                return
        ob.sendLine('* ���İ� �ʱ�ȭ�Ǿ����ϴ�.')
