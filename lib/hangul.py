#tossi 사용 

def is_han(word):
    if len(word) <= 0:
        return False
    # UNICODE RANGE OF KOREAN: 0xAC00 ~ 0xD7A3
    for c in range(len(word)):
        if word[c] < "\uac00" or word[c] > "\ud7a3":
            return False
    return True


def han_iga(word):
    if _is_jong(word):
        return '이'
    return '가'

def han_ira(word):
    if _is_jong(word):
        return '이라'
    return '라'
    
def han_obj(word):
    if _is_jong(word):
        return '을'
    return '를'

def han_un(word):
    if _is_jong(word):
        return '은'
    return '는'

def han_wa(word):
    if _is_jong(word):
        return '과'
    return '와'

def han_uro(word):
    if _is_jong(word):
        return '으로'
    return '로'

def han_i(word):
    if _is_jong(word):
        return '이'
    return ''

def han_aya(word):
    if _is_jong(word):
        return '아'
    return '야'


S_ATT = ['(은/는)', '(을/를)', '(이/가)', '(의/의)', '(에게/에게)', '(으로/로)', '(이라/라)', '(과/와)', '(아/야)']
def han_parse(name, line):
    n = 0
    for cmp in S_ATT:
        i = line.find(cmp)
        if i is not -1:
            s = cmp.split('/')
            if _is_jong(name):
                r = s[0][1:]
            else:
                r = s[1][0:-1]
            newline = line.replace(cmp, r)
            return name + newline
        n += 1
    return name + line

def postPosition(line, name):
    s = line.find('(')
    if s == -1:
        return line
    e = line.find(')')
    pps = line[s:e + 1]
    sep = pps.find('/')
    pp1 = pps[1:sep]
    pp2 = pps[sep + 1:-1]
    if _is_jong(name):
        pp = pp1
    else:
        pp = pp2
    return line.replace(pps, pp)
    
def postPosition1(line):
    s = line.find('(')
    if s == -1 or s < 2:
        return line
    e = line.find(')')
    pps = line[s:e + 1]
    sep = pps.find('/')
    pp1 = pps[1:sep]
    pp2 = pps[sep + 1:-1]
    for i in range(1, len(line) - s):
        a = ord(line[s - i])
        if a >= 0xA1 and a <= 0xFE:
            s = s + 1 - i
            break
    if s - 2 < 0:
        return line
    if _is_jong(line[:s]):
        pp = pp1
    else:
        pp = pp2
    return line.replace(pps, pp, 1)
