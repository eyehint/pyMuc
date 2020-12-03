# -*- coding: euc-kr -*-

import os
import glob
import time

from objs.object import Object

from lib.hangul import *
from lib.loader import load_script, save_script
from objs.item import Item, getItem, is_item
from lib.func import *

class Box(Object):
    
    def __init__(self):
        Object.__init__(self)
        
    def __del__(self):
        pass
        #self.save()
        #print 'Delete!!! ' + self.getName()
        
    def create(self, index):
        #print(path)
        self.index = index
        self.path = 'data/box/' + index + '.box'
        scr = load_script(self.path)
        if scr == None:
            return False
        try:
            self.attr = scr['��������']
        except:
            return False
        
        items = None
        if '������' not in scr:
            return True

        items = scr['������']

        if type(items) == dict:
            items = [items]

        for item in items:
            obj = getItem(str(item['�ε���']))
            if obj == None:
                print '�����Ծ����� �ε� ���� : %s' % str(item['�ε���'])
            if obj != None:
                obj = obj.deepclone()
                if 'Ȯ�� �̸�' in item:
                    obj.set('Ȯ�� �̸�', item['Ȯ�� �̸�'])
                if '�̸�' in item:
                    obj['�̸�'] = item['�̸�']
                if '�����̸�' in item:
                    obj['�����̸�'] = item['�����̸�']
                if '���ݷ�' in item:
                    obj['���ݷ�'] = item['���ݷ�']
                if '����' in item:
                    obj['����'] = item['����']
                if '�ⷮ' in item:
                    obj['�ⷮ'] = item['�ⷮ']
                if '�ɼ�' in item:
                    obj.set('�ɼ�', item['�ɼ�'])
                if '�����ۼӼ�' in item:
                    obj.set('�����ۼӼ�', item['�����ۼӼ�'])
                if '�ð�' in item:
                    obj.set('�ð�', item['�ð�'])
                self.insert(obj)
            
    def save(self):
        o = {}
        o['��������'] = self.attr
        
        items = []
        for item in self.objs:
            obj = {}
            obj['�ε���'] = item.index
            obj['�̸�'] = item.get('�̸�')
            obj['�����̸�'] = item.get('�����̸�').splitlines()
            if item.get('���ݷ�') != '':
                obj['���ݷ�'] = item.get('���ݷ�')
            if item.get('����') != '':
                obj['����'] = item.get('����')
            if item.get('�ⷮ') != '':
                obj['�ⷮ'] = item.get('�ⷮ')
            if item.get('�ɼ�') != '':
                obj['�ɼ�'] = item.get('�ɼ�').splitlines()
            if item.get('�����ۼӼ�') != '':
                obj['�����ۼӼ�'] = item.get('�����ۼӼ�').splitlines()
            if item.get('Ȯ�� �̸�') != '':
                obj['Ȯ�� �̸�'] = item.get('Ȯ�� �̸�')
            if item.get('�ð�') != '':
                obj['�ð�'] = item.get('�ð�')
            items.append(obj)

        o['������'] = items
        
        try:
            f = open(self.path, 'w')
        except:
            return False
        save_script(f, o)
        f.close()
        return True
        
    def viewShort(self):
        return '%s (%d/%d)' % (self['�̸�'], len(self.objs), int(self['��������']))
        
    def view(self, ob):
        p = int(self['��������'])
        pm = self['������������']
        pp = self['�����ִ����']
        
        ob.sendLine('������������������������������������������������������������������������������')
        buf = '�� %s�� %s ��' % (self['����'], self['�̸�'])
        ob.sendLine('[1m[44m[37m%-78s[0m[40m[37m' % buf)
        ob.sendLine('������������������������������������������������������������������������������')
        c = 0
        nCnt = {}
        for item in self.objs:
            c += 1
            nc = 0
            try:
                nc = nCnt[item['�̸�']]
            except:
                nCnt[item['�̸�']] = 0
            nCnt[item['�̸�']] = nc + 1
        if c == 0:
            ob.sendLine('�� �ƹ��͵� �����ϴ�.')
        else:
            msg = ''
            c = 0
            for name in nCnt:
                nc = nCnt[name]
                if nc == 1:
                    buf = name
                else:
                    buf = '%s %d��' % (name, nc)
                c += 1
                msg += '[1;36m��[0;36m%-20s[0;37m  ' % buf
                if c % 3 == 0:
                    msg += '\r\n'
            if c % 3 == 0:
                msg = msg[:-2]
            ob.sendLine(msg)
        if self['��������'] == self['�����ִ����']:
            buf = '�� ���� (%d/%d)' % ( len(self.objs), self['��������'])
        else:
            buf = '�� ���� (%d/%d)  �� �ִ���� (%d)  �� Ȯ�忡 �ʿ��� ���� (%d/%d)' % ( len(self.objs), self['��������'], \
            self['�����ִ����'], getInt(self['����']), self['������������'])
        ob.sendLine('������������������������������������������������������������������������������')
        ob.sendLine('[0m[47m[30m%-78s[0m[40m[37m' % buf)
        ob.sendLine('������������������������������������������������������������������������������')

        
    def destroy(self):
        self.env.remove(self)
        self.env = None
        del self
        
    def getNameA(self):
        return '[36m' + self.get('�̸�') + '[37m'
        
    def isFull(self):
        l = len(self.objs)
        if l >= self['��������']:
            return True
        return False
        
    def isExpandable(self):
        if self['��������'] == self['�����ִ����']:
            return False
        return True
        
    def addMoney(self, money):
        if self['����'] == '':
            self['����'] = 0
        self['����'] += money
        a = self['�����ִ����'] - self['��������']
        req = self['������������']
        cnt = self['����'] / req
        if cnt == 0:
            return money
        if cnt > a:
            cnt = a
        self['����'] -= cnt * req
        self['��������'] += cnt
        if self['��������'] == self['�����ִ����']:
            if self['����'] != 0:
                m = self['����']
                self['����'] = 0
                return money - m
        return money
        
def is_box(obj):
    return isinstance(obj, Box)

