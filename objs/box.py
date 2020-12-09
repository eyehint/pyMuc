from lib.func import *
from lib.loader import load_script, save_script
from objs.item import getItem
from objs.object import Object
import json

class Box(Object):

    def __init__(self):
        Object.__init__(self)

    def __del__(self):
        pass
        # self.save()
        #print 'Delete!!! ' + self.getName()
        
    def create(self, index):
        #print(path)
        self.index = index
        self.path = 'data/box/' + index + '.box'
        scr = load_script(self.path)
        if scr == None:
            return False
        try:
            self.attr = scr['상자정보']
        except:
            return False
        
        items = None
        if '아이템' not in scr:
            return True

        items = scr['아이템']

        if type(items) == dict:
            items = [items]

        for item in items:
            obj = getItem(str(item['인덱스']))
            if obj == None:
                print('보관함아이템 로딩 실패 : %s' % str(item['인덱스']))
            if obj != None:
                obj = obj.deepclone()
                if '확장 이름' in item:
                    obj.set('확장 이름', item['확장 이름'])
                if '이름' in item:
                    obj['이름'] = item['이름']
                if '반응이름' in item:
                    obj['반응이름'] = item['반응이름']
                if '공격력' in item:
                    obj['공격력'] = item['공격력']
                if '방어력' in item:
                    obj['방어력'] = item['방어력']
                if '기량' in item:
                    obj['기량'] = item['기량']
                if '옵션' in item:
                    obj.set('옵션', item['옵션'])
                if '아이템속성' in item:
                    obj.set('아이템속성', item['아이템속성'])
                if '시간' in item:
                    obj.set('시간', item['시간'])
                self.insert(obj)
            
    def save(self):
        o = {}
        o['상자정보'] = self.attr
        
        items = []
        for item in self.objs:
            obj = {}
            obj['인덱스'] = item.index
            obj['이름'] = item.get('이름')
            obj['반응이름'] = item.get('반응이름')
            if item.get('공격력') != '':
                obj['공격력'] = item.get('공격력')
            if item.get('방어력') != '':
                obj['방어력'] = item.get('방어력')
            if item.get('기량') != '':
                obj['기량'] = item.get('기량')
            if item.get('옵션') != '':
                obj['옵션'] = item.get('옵션')
            if item.get('아이템속성') != '':
                obj['아이템속성'] = item.get('아이템속성')
            if item.get('확장 이름') != '':
                obj['확장 이름'] = item.get('확장 이름')
            if item.get('시간') != '':
                obj['시간'] = item.get('시간')
            items.append(obj)

        o['아이템'] = items
        
        try:
            with open(self.path, 'w') as fp:
                save_script(fp, o)
        except:
            return False
        return True
        
    def viewShort(self):
        return '%s (%d/%d)' % (self['이름'], len(self.objs), int(self['보관수량']))
        
    def view(self, ob):
        p = int(self['보관수량'])
        pm = self['보관증가은전']
        pp = self['보관최대수량']
        
        ob.sendLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        buf = '◁ %s의 %s ▷' % (self['주인'], self['이름'])
        ob.sendLine('[1m[44m[37m%-78s[0m[40m[37m' % buf)
        ob.sendLine('───────────────────────────────────────')
        c = 0
        nCnt = {}
        for item in self.objs:
            c += 1
            nc = 0
            try:
                nc = nCnt[item['이름']]
            except:
                nCnt[item['이름']] = 0
            nCnt[item['이름']] = nc + 1
        if c == 0:
            ob.sendLine('☞ 아무것도 없습니다.')
        else:
            msg = ''
            c = 0
            for name in nCnt:
                nc = nCnt[name]
                if nc == 1:
                    buf = name
                else:
                    buf = '%s %d개' % (name, nc)
                c += 1
                msg += '[1;36m·[0;36m%-20s[0;37m  ' % buf
                if c % 3 == 0:
                    msg += '\r\n'
            if c % 3 == 0:
                msg = msg[:-2]
            ob.sendLine(msg)
        if self['보관수량'] == self['보관최대수량']:
            buf = '◆ 수량 (%d/%d)' % ( len(self.objs), self['보관수량'])
        else:
            buf = '◆ 수량 (%d/%d)  ◆ 최대수량 (%d)  ◆ 확장에 필요한 은전 (%d/%d)' % ( len(self.objs), self['보관수량'], \
            self['보관최대수량'], getInt(self['은전']), self['보관증가은전'])
        ob.sendLine('───────────────────────────────────────')
        ob.sendLine('[0m[47m[30m%-78s[0m[40m[37m' % buf)
        ob.sendLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')

        
    def destroy(self):
        self.env.remove(self)
        self.env = None
        del self
        
    def getNameA(self):
        return '[36m' + self.get('이름') + '[37m'
        
    def isFull(self):
        l = len(self.objs)
        if l >= self['보관수량']:
            return True
        return False
        
    def isExpandable(self):
        if self['보관수량'] == self['보관최대수량']:
            return False
        return True
        
    def addMoney(self, money):
        if self['은전'] == '':
            self['은전'] = 0
        self['은전'] += money
        a = self['보관최대수량'] - self['보관수량']
        req = self['보관증가은전']
        cnt = self['은전'] / req
        if cnt == 0:
            return money
        if cnt > a:
            cnt = a
        self['은전'] -= cnt * req
        self['보관수량'] += cnt
        if self['보관수량'] == self['보관최대수량']:
            if self['은전'] != 0:
                m = self['은전']
                self['은전'] = 0
                return money - m
        return money
        
def is_box(obj):
    return isinstance(obj, Box)

