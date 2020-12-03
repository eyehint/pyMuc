# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        if line == '':
            ob.sendLine('�� ����: [���] ��ġ')
            return
        item = ob.findObjName(line)
        if item == None:
            ob.sendLine('�� �׷� �������� ����ǰ�� �����.')
            return
        if item['����'] != '��ġ������':
            ob.sendLine('�� ��ġ�� �� �ִ� ���� �ƴմϴ�. ^^')
            return
        name = item['�̸�']
        owner = ob['�̸�']
        if ob.env['����'] == '':
            if ob.env['��������'] == ob['�Ҽ�']:
                if item.checkAttr('�����ۼӼ�', '���뺸����') == False:
                    ob.sendLine('�� �̰��� ��ġ�� �㰡���� �����ϴ�.')
                    return
                owner = ob['�Ҽ�']
            else:
                ob.sendLine('�� �̰��� ��ġ�� �㰡���� �����ϴ�.')
                return
        elif ob.env['����'] != ob['�̸�']:
            ob.sendLine('�� �̰��� ��ġ�� �㰡���� �����ϴ�.')
            return
        if name in ob.env['��ġ����Ʈ'].splitlines():
            ob.sendLine('�� �̹� ��ġ�� �Ǿ� �ֽ��ϴ�. ^^')
            return
        
        ob.env.setAttr('��ġ����Ʈ', name)
        ob.env.save()
        
        box = Box()
        box['�̸�'] = item['�̸�']
        box['��������'] = item['��������']
        box['�����̸�'] = item['�����̸�']
        box['����'] = item['����']
        box['��������'] = item['��������']
        box['������ġ'] = item['������ġ']
        box['��������'] = item['��������']
        box['�����ִ����'] = item['�����ִ����']
        box['������������'] = item['������������']
        box['�ǸŰ���'] = item['�ǸŰ���']
        box['����'] = item['����']
        box['�����ۼӼ�'] = item['�����ۼӼ�']
        box['����1'] = item['����1']
        box['����2'] = item['����2']
        box['����'] = owner
        box.index = '%s_%s' % (owner, item['�̸�'])
        box.path = 'data/box/%s.box' % box.index
        box.save()
        ob.env.insert(box)
        ob.sendLine('����� %s ��ġ�մϴ�.' % item.han_obj())
        ob.sendRoom('%s %s ��ġ�մϴ�.' % ( ob.han_iga(), item.han_obj() ))
        ob.remove(item)
        del item

