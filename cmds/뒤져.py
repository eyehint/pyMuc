# -*- coding: euc-kr -*-

from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):

    def cmd(self, ob, line):
        if len(line) == 0:
            ob.sendLine('�� ����: [���] ����')
            return
        obj = ob.env.findObjName(line)

        if obj == None or is_item(obj) or is_box(obj):
            ob.sendLine('�� ��������� �����. ^^')
            return
        if is_player(obj):
            ob.sendLine('����� %s�� ���� ������ϴ�. "�� ����~~ -.-"' % obj.getNameA())
            ob.sendRoom('%s %s�� ���� ������ϴ�. "�� ����~~ -.-"' % (ob.han_iga(), obj.getNameA()))
            return
            
        if obj.act != ACT_DEATH and obj['������'] != 6:
            ob.sendLine('����� %s�� ���� ������ϴ�. "�� ����~~ -.-"' % obj.getNameA())
            ob.sendRoom('%s %s�� ���� ������ϴ�. "�� ����~~ -.-"' % (ob.han_iga(), obj.getNameA()))
            return
        
        if len(obj.objs) == 0:
            if obj.act == ACT_DEATH:
                ob.sendLine('����� %s�� ��ü�� �����ϴ�. \'����~ ����~\'' % obj.getNameA())
                ob.sendRoom('%s %s�� ��ü�� �����ϴ�. \'����~ ����~\'' % (ob.han_iga(), obj.getNameA()))
            else:
                ob.sendLine('����� %s �����ϴ�. \'����~ ����~\'' % obj.han_obj())
                ob.sendRoom('%s %s �����ϴ�. \'����~ ����~\'' % (ob.han_iga(), obj.han_obj()))
            return
            
        msg = ''
        c = 0
        objs = copy.copy(obj.objs)
        for item in objs:
            if ob.getItemCount() >= getInt(MAIN_CONFIG['����ھ����۰���']) or ob.getItemWeight() + item['����'] > ob.getStr() * 10:
                if c == 0:
                    if obj.act == ACT_DEATH:
                        ob.sendLine('����� %s�� ��ü�� �����ϴ�. \'����~ ����~\'' % obj.getNameA())
                        ob.sendRoom('%s %s�� ��ü�� �����ϴ�. \'����~ ����~\'' % (ob.han_iga(), obj.getNameA()))
                    else:
                        ob.sendLine('����� %s �����ϴ�. \'����~ ����~\'' % obj.han_obj())
                        ob.sendRoom('%s %s �����ϴ�. \'����~ ����~\'' % (ob.han_iga(), obj.han_obj()))
                    return
                break

            c += 1
            obj.remove(item)
            ob.insert(item)
            if item.isOneItem():
                    ONEITEM.have(item.index, ob['�̸�'])
            if obj.act == ACT_DEATH:
                ob.sendLine('����� %s�� ��ü�ӿ��� %s ������ �����ϴ�.' % (obj.getNameA(), item.han_obj()))
                msg += '%s %s�� ��ü�ӿ��� %s ������ �����ϴ�.\r\n' %( ob.han_iga(), obj.getNameA(), item.han_obj())
            else:
                ob.sendLine('����� %s���Լ� %s ������ �����ϴ�.' % (obj.getNameA(), item.han_obj()))
                msg += '%s %s���Լ� %s ������ �����ϴ�.\r\n' %( ob.han_iga(), obj.getNameA(), item.han_obj())
        obj.timeofregen = time.time()
        ob.sendRoom(msg[:-2])

