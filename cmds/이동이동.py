# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):
    level = 1000
    def cmd(self, ob, line):
        if getInt(ob['�����ڵ��']) < 1000:
            ob.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
            return
        if len(line) == 0:
            ob.sendLine('�� ����: [���̸�:�ʹ�ȣ] �̵�')
            return
        room = getRoom(line)
        if room == None:
            ob.sendLine('* �̵� ����!!!')
            return
        
        if room == ob.env:
            ob.sendLine('�� ���� �ڸ�����. ^^')
            return
            
        #ob.act = ACT_STAND
        ob.clearTarget()
        
	ob.env.remove(ob)
	ob.env = room
	room.insert(ob)
        
        #reactor.callLater(2, ob.do_command, '��')
        #ob.parse_command('��')
