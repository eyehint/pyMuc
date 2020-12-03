# -*- coding: euc-kr -*-

def doEvent(self, mob, key, words):
    from lib.hangul import postPosition1, han_iga, han_obj
    from objs.rank import RANK
    from objs.oneitem import ONEITEM
    from objs.skill import MUGONG
    from objs.room import getRoom
    from lib.func import getStrCnt, getInt, stripANSI
    from lib.func import loadScriptFile
    from include.define import *
    import copy
    import time
    
    tab = 0
    rank1 = 0
    rank2 = 0
    searchEnd = False
    broadcast = False
    sub = {}
    script = mob.get(key).splitlines()
    for line in script:
        if line.strip() == '':
            if searchEnd == False:
                self.sendLine('')
            continue
        sline = line.strip()

        if searchEnd:
            if sline[0] == '{':
                tab = tab + 1
                continue
            elif sline[0] != '}':
                continue
            tab = tab - 1
            if tab != 0:
                continue
            searchEnd = False
            tab = 0
            continue

        if sline.find('$����') == 0:
            break

        sline = sline.replace('[������̸�]', self['�̸�'])

        if sline[0] == '$':
            if len(words) > 2:
                sline = sline.replace('$����:1', words[1])

            func = line.split()[0]
            #self.sendLine( line )
            if func == '$�̺�ƮȮ��!':
                if self.checkEvent(sline[13:].strip()) == True:
                    searchEnd = True
            elif func == '$�̺�ƮȮ��':
                if self.checkEvent(sline[12:].strip()) == False:
                    searchEnd = True
            elif func == '$�̺�Ʈ����':
                self.setEvent(sline[12:].strip())
            elif func == '$�̺�Ʈ����':
                self.delEvent(sline[12:].strip())
            elif func == '$����Ȯ��!':
                index, cnt = getStrCnt(sline)
                if '$����:' in line:
                    item = self.getItemName(index)
                    if item != None and item.inUse == False:
                        searchEnd = True
            elif func == '$�����ۼӼ�Ȯ��!':
                index, cnt = getStrCnt(sline)
                if '$����:' in line:
                    item = self.getItemName(index)
                    if item != None and item.getOption() != None:
                        searchEnd = True
            elif func == '$��ȭȮ��4000!':
                index, cnt = getStrCnt(sline)
                item = self.getItemIndex(index)
                print '11'
                if item != None and item['���ݷ�'] < 4000:
                    searchEnd = True
                    print '22'
            elif func == '$������Ȯ��!':
                index, cnt = getStrCnt(sline)
                if index == '����' and cnt < 1:
                    continue
                if index == '����' and cnt < 1:
                    continue
                if '$����:' in line:
                    if self.checkItemName(index, cnt) == True:
                        searchEnd = True
                else:
                    if self.checkItemIndex(index, cnt) == True:
                        searchEnd = True
            elif func == '$�Ӽ�����':
                self[sline[10:].strip()] = 1
            elif func == '$�����ۿɼǻ���':
                index, cnt = getStrCnt(sline)
                if '$����:' in line:
                    item = self.getItemName(index)
                    if item != None:
                        item.delOption()
                    else:
                        searchEnd = True
            elif func == '$������Ȯ��':
                index, cnt = getStrCnt(sline)
                if index == '����' and cnt < 1:
                    searchEnd = True
                    continue
                if index == '����' and cnt < 1:
                    searchEnd = True
                    continue
                if '$����:' in sline:
                    if self.checkItemName(words[1], cnt) == False:
                        searchEnd = True
                else:
                    if self.checkItemIndex(index, cnt) == False:
                        searchEnd = True
            elif func == '$������Ȯ��Ȯ��':
                item = self.getItemName(words[1])
                if item != None and item.get('Ȯ�� �̸�') != '':
                    continue
                else:
                    searchEnd = True
            elif func == '$������Ȯ��Ȯ��!':
                item = self.getItemName(words[1])
                if item != None and item.get('Ȯ�� �̸�') != '':
                    searchEnd = True
            elif func == '$������Ȯ�弳��':
                item = self.getItemName(words[1])
                if item != None and len(words) == 4:
                    item.set('Ȯ�� �̸�', words[2])
                    item.setAttr('�����ۼӼ�', '��������')
                    ac = item['�����̸�']
                    aclist = ac.splitlines()
                    aclist.append(words[2])
                    acline = ''
                    for a in aclist:
                        acline += a + '\r\n'
                    item['�����̸�'] = acline[:-2]
                        
            elif func == '$������Ȯ�弳������':  # ���缺:�̸��� (ũ����Ʈ)
                item = self.getItemName(words[1])
                if item != None and len(words) == 3:
                    acname = item['Ȯ�� �̸�']
                    ac = item['�����̸�']
                    aclist = ac.splitlines()
                    aclist.remove(acname)
                    acline = ''
                    for a in aclist:
                        acline += a + '\r\n'
                    item['�����̸�'] = acline[:-2]
                    item.set('Ȯ�� �̸�', '')
            elif func == '$�����ۻ���':
                index, cnt = getStrCnt(sline)
                if '$����:' in line:
                    item = self.getItemName(index)
                    self.remove(item)
                else:
                    self.delItem(index, cnt)
            elif func == '$�Ӽ����ֱ�':
                index, cnt = getStrCnt(sline)
                self.addItem(index, cnt, 1)
            elif func == '$�������ֱ�':
                index, cnt = getStrCnt(sline)
                self.addItem(index, cnt)
            elif func == '$����������Ȯ��':
                item = self.getItemName(words[1])
                if item != None and item.getType() == sline.split()[1]:
                    continue
                else:
                    searchEnd = True
            elif func == '$������ȣ����':
                if self.getTendency(sline[13:]) == False:
                    searchEnd = True
            elif func == '$��ġ�̵�':
                roomName = sline[10:].strip()
                #try:
                d = str( mob['���̵�'] )
                if d != '':
                    idx = roomName.find(':')
                    if idx != -1:
                        roomName = roomName[:idx] + d + roomName[idx:]
                #except:
                #    pass
                room = getRoom(roomName)
                if room == None:
                    self.sendLine('��������ε� ��ġ�̵� �� �� �����ϴ�.')
                    continue
                self.sendLine('')
                self.enterRoom(room, '��ȯ', '��ȯ')
                self.lpPrompt()
            elif func == '$���':
                self.printScript(sline[6:])
            elif func == '$��������ƮȮ��':
                if self.checkMugongList(sline[16:]) == False:
                    searchEnd = True
            elif func == '$��������ƮȮ��!':
                if self.checkMugongList(sline[17:]) == True:
                    searchEnd = True
            elif func == '$��������Ʈ����':
                var = sline.split()
                for m in var:
                    if m in self.skillList:
                        self.skillList.remove(m)
            elif func == '$��������Ȯ��':
                if len(self.skillList) < getInt(sline[14:]):
                    searchEnd = True                        
            elif func == '$����Ȯ��':
                if self.checkMugong(sline[10:]) == False:
                    searchEnd = True
            elif func == '$����Ȯ��!':
                if self.checkMugong(sline[11:]) == True:
                    searchEnd = True
            elif func == '$��������':
                self.addMugong(sline[10:])
            elif func == '$����ȸ��':
                self.delMugong(sline[10:])
            elif func == '$��������':
                skill_found = False
                for s in self.skills:
                    if s.name == sline[10:]:
                        skill_found = True
                        break
                if skill_found == False:
                    s = MUGONG[sline[10:]].clone()
                    s.start_time = s['���ð�']
                    self.skills.append(s)
                    self._str += s._str
                    self._dex += s._dex
                    self._arm += s._arm
                    buf1, buf2, buf3 = mob.makeFightScript(s['������ũ��'], self)
                    self.sendLine(buf2)
            elif func == '$������������':
    		if mob.act == ACT_DEATH:
                    self.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
                    return
                if self.act == ACT_FIGHT:
                    if mob in self.target:
                        self.sendLine('�� �̹� �������̿���. ^_^')
                    else:
                        self.sendLine('�� ������ �񹫿� �Ű��� �����ϼ���. @_@')
                else:
                    self.setFight(mob, True)
            elif func == '$��������':
                searchEnd = True
                if mob.act == ACT_DEATH:
                    self.sendLine('�� ���� ������ �𸣰ھ��. *^_^*')
                    return
                if mob.act == ACT_FIGHT:
                    if mob in self.target:
                        self.sendLine('�� �̹� �������̿���. ^_^')
                    else:
                        self.sendLine('�� �̹� �ٸ� ����� �������̶� ������ ���� ���׿�')
                    continue
                if self.act == ACT_FIGHT:
                    if mob in self.target:
                        self.sendLine('�� �̹� �������̿���. ^_^')
                    else:
                        self.sendLine('�� ������ �񹫿� �Ű��� �����ϼ���. @_@')
                else:
                    self.setFight(mob, True)
                    searchEnd = False
            elif func == '$������Ȯ��!':
                if mob.getAct() == sline[13:].strip():
                    searchEnd = True
            elif func == '$������Ȯ��':
                if mob.getAct() != sline[12:].strip():
                    searchEnd = True
            elif func == '$�����¼���':
                mob.setAct(sline[12:].strip())
            elif func == '$ü�¼Ҹ�':
                self.minusHP( getInt(sline[10:].strip()) )
            elif func == '$ü�°���':
                self.minusHP( getInt(sline[10:].strip()) )
            elif func == '$����Ȯ��':
                var = sline.split()
                c = getInt(var[1])
                if len(words) < 3 or len(var) < 3 or c > len(words) - 2:
                    searchEnd = True
                elif words[c] != var[2]:
                    searchEnd = True
            elif func == '$Ư��ġ����':
                var = sline.split()
                c = getInt(var[2])
                cc = getInt(self.get(var[1]))
                cc = cc + c
                self.set(var[1], cc)
                self.lpPrompt()

            elif func == '$������ȯ':
                if self.get('����') == '����':
                    self.set('����', '����')
                elif self.get('����') == '����':
                    self.set('����', '����')
                
            elif func == '$����Ȯ��':
                if self.get('����') == '��':
                    searchEnd = True
                    
            elif func == '$���ڼ���':
                self.set('����', '��')
            elif func == '$���ڼ���':
                self.set('����', '��')                                
            elif func == '$Ư��ġ����':
                var = sline.split()
                c = getInt(var[2])
                self.set(var[1], c)
            elif func == '$Ư��ġȮ��':
                var = sline.split()
                c = getInt(var[2])
                if self.get(var[1]) < c:
                    searchEnd = True
            elif func == '$����Ĩ�ż���':
                self.setEunDun()
            elif func == '$��ȭ�����':
                self.setSunIn()
            elif func == '$�ҿ���ȣ����':
                self.setGiIn()

            elif func == '$��ȣ����':
                if len(words) != 3:
                    self.sendLine('�� �ٲܺ�ȣ�� �Է��ϼ���.')
                    continue
                print words[1]
                if self['������ȣ'] == '':
                    self.sendLine('�� ����� �����Դϴ�.')
                    continue
                if len(words[1]) < 3:
                    self.sendLine('�� ����Ͻ÷��� ��ȣ�� �ʹ� ª�ƿ�.')
                    continue
                if len(words[1]) > 10:
                    self.sendLine('�� ����Ͻ÷��� ��ȣ�� �ʹ� ����.')
                    continue
                from objs.nickname import Nickname, NICKNAME
                if words[1] in NICKNAME.attr:
                    self.sendLine('�� �ٸ� �������� ������� ��ȣ�Դϴ�. ^^')
                    continue
                NICKNAME.attr.__delitem__(self['������ȣ'])
                NICKNAME[words[1]] = self['�̸�']
                NICKNAME.save()
                self['������ȣ'] = words[1]
                self.do_command('��ȯ')
            elif func == '$�⿬����Ȯ��':
                bRet, owner = ONEITEM.checkOneItemName(sline[14:].strip())
                if bRet:
                    sub['[�⿬������]'] = owner
                else:
                    searchEnd = True
            elif func == '$�⿬Ȯ��':
                bRet, owner = ONEITEM.checkOneItemIndex(sline[10:].strip())
                if bRet:
                    sub['[�⿬������]'] = owner
                else:
                    searchEnd = True
            elif func == '$�⿬Ȯ��!':
                bRet, owner = ONEITEM.checkOneItemIndex(sline[11:].strip())
                if bRet:
                    sub['[�⿬������]'] = owner
                    searchEnd = True
            elif func == '$�������':
                ws = sline.split(None, 2)
                if len(ws) != 3:
                    #print '!!!!'
                    searchEnd = True
                    continue
                value = self[ws[2]]
                if value == '':
                    value = -1
                rank1 = RANK.read_rank(ws[2], self['�̸�'])
                rank2 = RANK.write_rank(ws[2], self['�̸�'], value, int(ws[1]))
                #print rank1, rank2
                if rank2 == 0:
                    searchEnd = True
            elif func == '$��������':
                ws = sline.split(None, 1)
                if rank1 != rank2 and rank2 == 1:
                    l = ws[1].replace('[��]', '���')
                    self.sendLine(postPosition1(l))
                    l = ws[1].replace('[��]', self['�̸�'])
                    self.channel.sendToAll1(postPosition1(l), ex = self, noPrompt = True)
                    broadcast = True
            elif func == '$����Ȯ��':
                
                ws = sline.split(None, 2)
                if len(ws) != 3:
                    searchEnd = True
                    continue
                if len(words) == 3:
                    r = getInt(words[1])
                    if words[1] == '���':
                        msg = RANK.getRankAll(ws[2])
                        self.sendLine(msg)
                        return
                    elif r > 0:
                        if r > int(ws[1]):
                            r = int(ws[1])
                        name = RANK.getRankNum(ws[2], r)
                        if name != None:
                            sub['[������]'] = name
                            sub['[����]'] = str(r)
                        else:
                            sub['[������]'] = '[%d��]' % r
                            searchEnd = True
                        continue
                    else:
                        name = words[1]
                else:
                    name = self['�̸�']
                rank1 = RANK.read_rank(ws[2], name)
                sub['[������]'] = name
                sub['[����]'] = str(rank1)
                if rank1 == 0:
                    searchEnd = True
            elif func == '$����Ȯ��!':
                ws = sline.split(None, 2)
                if len(ws) != 3:
                    searchEnd = True
                    continue
                if len(words) == 3:
                    r = getInt(words[1])
                    if words[1] == '���':
                        msg = RANK.getRankAll(ws[2])
                        self.sendLine(msg)
                        return
                    elif r > 0:
                        if r > int(ws[1]):
                            r = int(ws[1])
                        name = RANK.getRankNum(ws[2], r)
                        if name != None:
                            sub['[������]'] = name
                            sub['[����]'] = str(r)
                        else:
                            sub['[������]'] = '[%d��]' % r
                            searchEnd = True
                        continue
                    else:
                        name = words[1]
                else:
                    name = self['�̸�']
                rank1 = RANK.read_rank(ws[2], name)
                sub['[������]'] = name
                sub['[����]'] = str(rank1)
                if rank1 != 0:
                    searchEnd = True
            elif func == '$��������Ȯ��':
                if int(sline[13:]) > self['����']:
                    searchEnd = True
            elif func == '$��������Ȯ��!':
                if int(sline[14:]) <= self['����']:
                    searchEnd = True
            elif func == '$��������':
                self.setAttr('�����̸�', sline.split()[1])
            elif func == '$��������Ȯ��': # ���缺:������ (��������)
                if self['��������'] == '':
                    searchEnd = True
            elif func == '$��������Ȯ��':
                var = sline.split()
                if len(var) != 2:
                    print('[��������Ȯ��] Ű���� Ȥ�� ���� ����')
                    return
                if var[1] not in self['�����̸�']:
                    searchEnd = True
            elif func == '$��������Ȯ��!':
                var = sline.split()
                if len(var) != 2:
                    print('[��������Ȯ��] Ű���� Ȥ�� ���� ����')
                    return
                if var[1] in self['�����̸�']:
                    searchEnd = True
            elif func == '$�������ü���Ȯ��':
                var = sline.split()
                if len(var) != 3:
                    print('[�������ü���Ȯ��] Ű���� Ȥ�� ���� ����')
                    return
                if var[1] != var[2]:
                    searchEnd = True
            elif func == '$�������ð���Ȯ��!':
                var = sline.split() 
                if var[1] in var[2:]:
                    searchEnd = True
            elif func == '$�������û���':
                self['��������'] = ''
            elif func == '$�������ü���':
                var = sline.split()
                if len(var) != 2:
                    print('[�������ü���] Ű���� Ȥ�� ���� ����')
                    return
                self['��������'] = var[1]
            elif func == '$���̵����Ա��':
                self['���̵����Խð�'] = int(time.time())

            elif func == '$���̵�������Ȯ��':
                t = self['���̵����Խð�']
                if t == '':
                    t = 0
                    self['���̵����Խð�'] = 0
                if int(time.time()) > t + 60 * 5:
                    searchEnd = True
                else:
                    searchEnd = False

            elif func == '$���̵�������Ȯ��!':
                t = self['���̵����Խð�']
                if t == '':
                    t = 0
                    self['���̵����Խð�'] = 0
                if int(time.time()) > t + 60 * 5:
                    searchEnd = False
                else:
                    searchEnd = True

            elif func == '$��ũ��Ʈȣ��':
                scr = sline[13:].strip()
                self.INTERACTIVE = 0
                #from objs.autoscript import autoScript
                self.autoscript = self.autoScript()
                self.autoscript.start(loadScriptFile(scr), self)
                return
            elif func == '$�ü�Ȯ��':
                if getInt(self['�ü��Ϸ�']) == 1:
                    searchEnd = False 
                    continue
                searchEnd = True
            elif func == '$�ü�Ȯ��!':
                if getInt(self['�ü��Ϸ�']) == 0:
                    searchEnd = False 
                    continue
                searchEnd = True
            elif func == '$�ü��ڰ�Ȯ��':
                if self['1 ���õ�'] >= 1000 and self['2 ���õ�'] >= 1000 and self['3 ���õ�'] >= 1000 and self['4 ���õ�'] >= 1000 and self['5 ���õ�'] >= 1000: 
                    searchEnd = False 
                    continue
                searchEnd = True
            elif func == '$Ư��ġ����':
                oldattr = mob.attr
                #mob.attr = copy.deepcopy(oldattr)
                mob.attr = {}
                for k in oldattr.keys():
                    mob.attr[k] = oldattr[k]
                del oldattr
                mob['ü��'] = mob.hp = self['�ְ�ü��'] * 6
                mob['��'] = self['��'] * 2
                if self['����'] >= 1800:
                    mob['��'] = 20000
                mob['����'] = self['����'] + 180
                mob['����'] = self['����'] * 2.5
            elif func == '$�߱޼���':
                oldattr = mob.attr
                mob.attr = {}
                for k in oldattr.keys():
                    mob.attr[k] = oldattr[k]
                del oldattr
                mob['��'] = self['��'] * 1
                mob['����'] = self['����'] + 200
                mob['ȸ��'] = 160
            """
            elif func == '$�񹫰�������':
                pass
            elif func == '$�񹫰�����':
                pass
            """
        elif sline[0] == '{':
            pass
        elif sline[0] == '}':
            pass
        else:
            if '[��﹫���̸�����]' in line:
                nCount = 0
                w = self.findObjInven(words[1])
                if w != None:
                    mlist = w['�����̸�'].splitlines()
                    for m in mlist:
                        if m.split()[0] in self.skillList:
                            continue
                        type = m.split()[1]
                        if type != '����':
                            if self['����'] != type and self['����'] != '����' and self['����'] != '����':
                                continue
                        nCount += 1
                sub['[��﹫���̸�����]'] = str(nCount)
            elif '[�����ۻ��Ƚ��]' in line:
                nCount = 0
                for it in self.objs:
                    if it.inUse == False and stripANSI(it['�̸�']) == words[1]:
                        words[1] = it['�̸�']
                        break
                        
                if words[1] in self.itemSkillMap:
                    nCount = self.itemSkillMap[words[1]]
                sub['[�����ۻ��Ƚ��]'] = str(nCount)
            elif '[����]' in line:
                sub['����'] = words[1]

            for su in sub:
                line = line.replace(su, sub[su])
            self.sendLine(postPosition1(line))
    if broadcast:
        self.channel.sendToAll1('', ex = self)
    return True
