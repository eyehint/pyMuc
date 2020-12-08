import tossi


def is_han(word):
    if len(word) <= 0:
        return False
    # UNICODE RANGE OF KOREAN: 0xAC00 ~ 0xD7A3
    for c in range(len(word)):
        if word[c] < "\uac00" or word[c] > "\ud7a3":
            return False
    return True


def han_iga(word):
    return tossi.pick(word, '이(가)')

def han_ira(word):
    if _is_jong(word):
        return '이라'
    return tossi.pick(word, '이라(가)')
def han_obj(word):
    return tossi.pick(word, '을(를)')

def han_un(word):
    return tossi.pick(word, '은()')


def han_wa(word):
    return tossi.pick(word, '과(와)')

def han_uro(word):
    return tossi.pick(word, '으로(로)')


def han_i(word):
    return tossi.pick(word, '이()')


def han_aya(word):
    return tossi.pick(word, '야(아)')


def postPosition(line, name):
    s = line.find('(')
    if s == -1:
        return line
    e = line.find(')')
    pps = line[s:e + 1]
    pp = tossi.postfix(name, pps)
    return line.replace(pps, pp)


def postPosition1(line):
    s = line.find('(')
    if s == -1 or s < 2:
        return line
    e = line.find(')')
    pps = line[s:e + 1]
    for i in range(1, len(line) - s):
        a = ord(line[s - i])
        if a >= 0xA1 and a <= 0xFE:
            s = s + 1 - i
            break
    if s - 2 < 0:
        return line
    pp = tossi.postfix(line[:s], pps)
    return line.replace(pps, pp, 1)
