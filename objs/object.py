# -*- coding: euc-kr -*-

import copy
from lib.func import getInt, stripANSI
from lib.hangul import han_iga, han_obj, han_un

class Object:

    def __init__(self):
        # ���� ������Ʈ�� �Ӽ���
        self.attr = {}
        self.temp = {}
        
        # ���� ������Ʈ�� ������ ���� ������Ʈ
        self.env = None
        
        # ���� ������Ʈ�� ������ ���� ������Ʈ ����Ʈ
        self.objs = []
        
    def __del__(self):
        pass
        
    def __getitem__(self, key):
        return self.get(key)
        
    def __setitem__(self, key, data):
        return self.set(key, data)

    def __delitem__(self, key):
        del self.attr[key]
        
    def init(self):
        pass
        
    def create(self, path):
        pass
        
    def set(self, key, keydata):
        self.attr[key] = keydata
    
    def get(self, key):
        try:
            keydata = self.attr[key]
        except:
            return ''
        return keydata

    def getStrip(self, key):
        return stripANSI(self[key])
    
    def getName(self):
        return self.get('�̸�')
        
    def getInt(self, key):
        try:
            keydata = self.attr[key]
        except:
            return 0
        return getInt(keydata)
    
    def getString(self, key):
        try:
            keydata = self.attr[key]
        except:
            return ''
        return str(keydata)
    
    def setTemp(self, key, keydata):
        self.temp[key] = keydata
    
    def getTemp(self, key):
        try:
            keydata = self.temp[key]
        except:
            return ''
        return keydata
    
    def clone(self):
        return copy.copy(self)
    
    def deepclone(self):
        return copy.deepcopy(self)

    def insert(self, obj):
        if obj not in self.objs:
            obj.env = self
            self.objs.insert(0, obj)
    
    def append(self, obj):
        if obj not in self.objs:
            obj.env = self
            self.objs.append(obj)

    def remove(self, obj):
        if obj in self.objs:
            obj.env = None
            self.objs.remove(obj)
        
    def clear(self):
        pass
        
    def han_iga(self):
        return self.getNameA() + han_iga(self['�̸�'])
        
    def han_obj(self):
        return self.getNameA() + han_obj(self['�̸�'])
        
    def han_un(self):
        return self.getNameA() + han_un(self['�̸�'])
        
    def findObjName(self, name, order = 1):
        n = 0
        for obj in self.objs:
            if obj.get('�̸�') == name or name in obj.get('�����̸�').splitlines():
                if obj.checkAttr('�����ۼӼ�', '��¾���'):
                    continue
                n += 1
                if n == order:
                    return obj
        return None
        
    def findObjInven(self, name, order = 1):
        n = 0
        for obj in self.objs:
            if obj.get('�̸�') == name or name in obj.get('�����̸�').splitlines():
                if obj.inUse:
                    continue
                n += 1
                if n == order:
                    return obj
        return None

    def findObjInUse(self, name, order = 1):
        n = 0
        for obj in self.objs:
            if obj.get('�̸�') == name or name in obj.get('�����̸�').splitlines():
                if obj.inUse == False:
                    continue
                n += 1
                if n == order:
                    return obj
        return None
        
    def checkAttr(self, key, attr):
        keydata = self.get(key)
        
        if attr in keydata.splitlines():
            return True
            
        return False
        
    def setAttr(self, key, attr):
        lines = self[key].splitlines()
        if attr in lines:
            return
        at = ''
        for line in lines:
            at += line + '\n'
        at += attr + '\n'
        self[key] = at
        
    def delAttr(self, key, attr):
        at = self[key].splitlines()
        if attr in at:
            at.remove(attr)
            text = ''
            for s in at:
                if s == '':
                    continue
                text += s + '\n'
            self.set(key, text)
        
