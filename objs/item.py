# -*- coding: euc-kr -*-

import os
import glob
import time

from objs.object import Object
from objs.oneitem import Oneitem, ONEITEM
from lib.hangul import *
from lib.loader import load_script, save_script
from lib.func import *

class Item(Object):
    Items = {}
    
    MagicMap = {}
    OptionName = []

    def __init__(self):
        self.timeofdrop = 0
        
    def __del__(self):
        pass
        #print 'Delete!!! ' + self.getName()
        
    def create(self, index):
        #print(path)
        self.index = index
        self.path = 'data/item/' + index + '.itm'
        scr = load_script(self.path)
        if scr == None:
            return False
        try:
            self.attr = scr['����������']
        except:
            return False
            
        self.inUse = False
        #print '%s ����!!!' % str(index)

    def save(self, mode = True):
        o = {}
        o['����������'] = self.attr

        try:
            f = open(self.path, 'w')
        except:
            return False
        save_script(f, o)
        f.close()
        return True
        
    def view(self, ob):
        ob.sendLine('������������������������������������������')
        ob.sendLine('[0m[44m[1m[37m�� �̸� �� %-31s[0m[37m[40m' % self.get('�̸�'))
        ob.sendLine('[0m[44m[1m[37m�� ���� �� %-31s[0m[37m[40m' % self.get('����'))
        ob.sendLine('������������������������������������������')
        #ob.sendLine(self.get('����2'))
        desc = self['����2']
        d = desc.splitlines()
        for l in d:
            if l.find('���� - ') == 0:
                ob.sendLine('���� - %d' % self['����'])
            else:
                ob.sendLine(l)
        s = self.getOptionStr()
        if s != '':
            ob.sendLine(s)
        ob.sendLine('������������������������������������������')
        
    def drop(self, sec = None):
        if sec != None:
            self.timeofdrop = time.time() - sec
        else:
            self.timeofdrop = time.time()
        
    def update(self):
        if self.timeofdrop == 0:
            self.timeofdrop = time.time()
            return False
        curTime = time.time()
        if curTime - self.timeofdrop >= 600:
            self.destroy()
            return True
    
    def destroy(self):
        if self.isOneItem():
            ONEITEM.destroy(self.index)
        if self.env != None:
            self.env.remove(self)
            self.env = None
        del self
        
    def getNameA(self):
        return '[36m' + self.get('�̸�') + '[37m'
        
    def getDesc1(self):
        return self.get('����1').replace('$������$', '[36m' + self.get('�̸�') + '[37m')
    
    def getType(self):
        return self.get('����')

    def getUseScript(self):
        return self.get('��뽺ũ��').replace('$������$', self.get('�̸�'))
        
    def isOneItem(self):
        if self.checkAttr('�����ۼӼ�', '���Ͼ�����'):
            return True
        return False
        
    def isOneThere(self):
        bRet, owner = ONEITEM.checkOneItemIndex(self.index)
        return bRet

    def delOption(self):
        if self['�ɼ�'] != None:
            del self['�����ۼӼ�']
            del self['�ɼ�']

    def getOption(self):
        s = self['�ɼ�']
        if s == '':
            return None
        option = {}
        lines = s.splitlines()
        for l in lines:
            w = l.split()
            option[w[0]] = int(w[1])
        return option
        
    def setOption(self, option):
        s = ''
        for d in option:
            s += d + ' ' + str(option[d]) + '\r\n'
        self['�ɼ�'] = s

    def getOptionStr(self):
        option = self.getOption()
        if option == None:
            return ''
        s = ''
        for d in option:
            s += d + '(' + str(option[d]) + '), '
        return s[:-2]
        #return '[0m[47m[30m%s[0m[37m[40m' % s[:-2]
        

def is_item(obj):
    return isinstance(obj, Item)

def getItem(itemName):

    try:
        item = Item.Items[itemName]
    except KeyError:
        item = Item()
        ret = item.create(itemName)
        if ret == False:
            return None

        Item.Items[itemName] = item

    return item
    

def loadAllItem():
    log('������ �ε���... ��ø� ��ٷ��ּ���.')
    pwd = os.getcwd()
    c = 0
    os.chdir('data/item')
    files = glob.glob('*.itm')
    os.chdir(pwd)
    for file in files:
        item = getItem(file[:-4])
        if item != None:
            c = c + 1
    
    log(str(c) + '���� �������� �ε��Ǿ����ϴ�.')

