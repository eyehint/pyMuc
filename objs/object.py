import copy
from lib.func import getInt, stripANSI
from lib.hangul import han_iga, han_obj, han_un


class Object:
    def __init__(self):
        # 현재 오브젝트의 속성맵
        self.attr = {}
        self.temp = {}
        
        # 현재 오브젝트를 가지는 상위 오브젝트
        self.env = None
        
        # 현재 오브젝트가 가지는 하위 오브젝트 리스트
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
        return self.get('이름')
        
    def getInt(self, key):
        try:
            keydata = self.attr[key]
        except:
            return 0
        return getInt(keydata)

    def getNameA(self):
        return '[33m' + self.get('이름') + '[37m'
    
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
        return self.getNameA() + han_iga(self['이름'])
        
    def han_obj(self):
        return self.getNameA() + han_obj(self['이름'])
        
    def han_un(self):
        return self.getNameA() + han_un(self['이름'])
        
    def findObjName(self, name, order = 1):
        n = 0
        for obj in self.objs:
            if obj.get('이름') == name or name in obj.get('반응이름'):
                if obj.checkAttr('아이템속성', '출력안함'):
                    continue
                n += 1
                if n == order:
                    return obj
        return None
        
    def findObjInven(self, name, order = 1):
        n = 0
        for obj in self.objs:
            if obj.get('이름') == name or name in obj.get('반응이름'):
                if obj.inUse:
                    continue
                n += 1
                if n == order:
                    return obj
        return None

    def findObjInUse(self, name, order = 1):
        n = 0
        for obj in self.objs:
            if obj.get('이름') == name or name in obj.get('반응이름'):
                if obj.inUse == False:
                    continue
                n += 1
                if n == order:
                    return obj
        return None
        
    def checkAttr(self, key, attr):
        keydata = self.get(key)
        
        if attr in keydata:
            return True
            
        return False
        
    def setAttr(self, key, attr):
        lines = self[key]
        if attr in lines:
            return
        at = ''
        for line in lines:
            at += line + '\n'
        at += attr + '\n'
        self[key] = at
        
    def delAttr(self, key, attr):
        at = self[key]
        if attr in at:
            at.remove(attr)
            text = ''
            for s in at:
                if s == '':
                    continue
                text += s + '\n'
            self.set(key, text)
        
