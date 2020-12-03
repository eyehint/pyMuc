# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    room_num = [
        12,14,16,18,20,
        34,36,38,40,42,
        56,58,60,62,64,
        78,80,82,84,86,
        100,102,104,106,108,
    ]


    level = 2000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 2000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        words = line.split()
        if len(words) < 1:
            ob.sendLine('�� ����: [�����ҹ���] ��')
            return
        if ob.env == None:
            ob.sendLine('\r\n* �ƹ��͵� ������ �ʽ��ϴ�.\r\n')
            return
        c = 0
        for exitName in ob.env.exitList:
            if exitName[-1] == '$':
                continue
            c += 1
        if c == 0:
            ob.sendLine('�� �ƹ��͵� ������ �ʽ��ϴ�.')
            return
        if words[0] not in ob.env.exitList:
            ob.sendLine('�� �� �������δ� ������ �����!.')
            return

        ob.walkhis = []
        ob.mapQ = {}
        l = copy.copy(ob.env.exitList)
        l.remove(words[0])
        a = []
        for ex in l:
            if ex in ['��', '��', '��', '��', '�ϼ�', '�ϵ�', '����', '����']:
                a.append(ex)
        l = a
        ob.mapQ[ob.env.index] = []
        if len(l) == 0:
            ob.sendLine('�� �� �������δ� ������ �����!.')
            del ob.mapQ
            del ob.walkhis
            return
        self.explorer(ob, ob.env.getExit(l[0]), l[0])
        ob.write(self.map(ob.walkhis))
        #print ob.walkhis

        del ob.mapQ
        del ob.walkhis

    def count_explorer(self, ob, env, direction):
        if env == None:
            return 0

        reverse = self.reverseDir(direction)
        if reverse == '':
            return 0

        if env.index in ob.tempQ:
            return 0
        else:
            l = copy.copy(env.exitList)
            ob.tempQ[env.index] = l

        if reverse in l:
            l.remove(reverse)

        if len(l) == 0:
            return 1

        n = 0
        for exit in l:
            if exit not in ['��', '��', '��', '��', '�ϼ�', '�ϵ�', '����', '����']:
                continue
            r = env.getExit(exit)
            if r == None:
                continue
            if env.zone != r.zone:
                continue
            n += self.count_explorer(ob, r, exit)

        ob.tempQ[env.index] = []
        return n

    def explorer(self, ob, env, direction):
        if env == None:
            print 'env is None'
            return
        #print env.index, direction

        reverse = self.reverseDir(direction)
        if reverse == '':
            return

        if env.index in ob.mapQ:
            l = ob.mapQ[env.index]
            if reverse in l:
                l.remove(reverse)
            return
            #l = ob.mapQ[env.index]
        else:
            l = copy.copy(env.exitList)
            ob.mapQ[env.index] = l

        if reverse in l:
            l.remove(reverse)
        ob.walkhis.append(direction)

        dirs = {}
        for exit in l:
            ob.tempQ = {}
            if exit not in ['��', '��', '��', '��', '�ϼ�', '�ϵ�', '����', '����']:
                continue
            r = env.getExit(exit)
            if r == None:
                print env.index, exit
                continue
            if env.zone != r.zone:
                continue
            n = self.count_explorer(ob, r, exit)
            dirs[exit] = n
        import operator
        sorted_x = sorted(dirs.iteritems(), key=operator.itemgetter(1))
        sorted_l = []
        for item in sorted_x:
            sorted_l.append(item[0]) 

        l = sorted_l
        while(True):
            if len(l) == 0:
                break
            exit = l.pop()
            if exit not in ['��', '��', '��', '��', '�ϼ�', '�ϵ�', '����', '����']:
                continue
            r = env.getExit(exit)
            if r == None:
                print env.index, exit
                continue
            if env.zone != r.zone:
                continue
            self.explorer(ob, r, exit)

        ob.mapQ[env.index] = []

        if self.checkEmpty(ob.mapQ) == False:
            ob.walkhis.append( reverse )
        return

    def checkEmpty(self, mapQ):
        for m in mapQ:
            l = mapQ[m]
            for exit in l:
                #print m, exit
                return False
        return True

    def reverseDir(self, direction):
        if direction == '��':
            return '��'
        if direction == '��':
            return '��'
        if direction == '��':
            return '��'
        if direction == '��':
            return '��'
        if direction == '�ϼ�':
            return '����'
        if direction == '����':
            return '�ϼ�'
        if direction == '�ϵ�':
            return '����'
        if direction == '����':
            return '�ϵ�'
        if direction == '��':
            return '�Ʒ�'
        if direction == '�Ʒ�':
            return '��'
        return ''

    def map(self, l):
        maptext=''
        for i in l:
    	    maptext += i + ';';
        return maptext

