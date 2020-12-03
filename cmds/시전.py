# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cool1(self, ob, name):
        ob.cooltime[name] = 2
        if name == '���Ĺ̺�':
            if ob.act != ACT_DEATH:
                ob.sendLine('\n����� ���ĳ��� [1;36m����ڰ��[;37m�� �Ź��� ����ϴ�.')
            ob._miss -= 350
        elif name == '���ٰ�':
            if ob.act != ACT_DEATH:
                ob._str -= 500
                ob._arm -= 500
                ob._maxhp -= 50
                ob.sendLine('\n����� ���ĳ� [1;33m�����[0;37m�� ��� [1;32m�Ѩ����[0;37m [1;31m���[0;37m�� �ŵξ� ���Դϴ�.')
            if ob['ü��'] > ob.getMaxHp():
                ob['ü��'] = ob.getMaxHp()

        reactor.callLater(5, self.cool2, ob, name)
        return

    def cool2(self, ob, name):
        ob.cooltime[name] = 0
        return

    def cmd(self, ob, line):
        from objs.skill import MUGONG
        if ob.act == ACT_REST:
            ob.sendLine('�� ��������߿� ������ ����� �� �����ϴ�.')
            return

        if len(line) == 0:
            ob.sendLine('�� ����: [���|�����̸�] ����')
            return

        words = line.split()
        l = len(words)
        if l == 1:
            mName = line
            tName = ''
            if ob.act == ACT_FIGHT and len(ob.target) > 0:
                mob = ob.target[0]
        else:
            mName = words[1]
            if words[0] == '.':
                words[0] = '1'
            mob = ob.env.findObjName(words[0])
            if mob == None:
                ob.sendLine('�� �׷� ��밡 �����ϴ�.')
                return
            if is_player(mob) == False and is_mob(mob) == False:
                ob.sendLine('�� �׷� ��밡 �����ϴ�.')
                return
            if mob.act == ACT_DEATH:
                ob.sendLine('�� �׷� ��밡 �����ϴ�.')
                return
            if mob['�̸�'] != '���ĸ�' and len(mob.target) != 0 and ob not in mob.target:
                ob.sendLine('�� �׷� ��밡 �����ϴ�.')
                return
            #if mob['������'] == 5:
            #    ob.sendLine('�� ��ȣ���� ������ �� �ִ°Ͱ� ���°��� ����!')
            #    return
        """
        if line in [ '���Ĺ̺�', '���ٰ�']:
            try:
                cool = ob.cooltime
                if line in cool:
                    c = cool[line]
                else:
                    c = 0
                    cool[line] = 0
            except:
                ob.cooltime = {}
                cool = ob.cooltime
                cool[line] = 0
                c = 0
            for c1 in cool:
                if cool[c1] == 1:
                    ob.sendLine('[1;37m����� �������Ⱑ ������� ���� ��ȯ�� ���߾� �����ϴ�.[0;37m')
                    return
            if c != 0:
                ob.sendLine('[1;37m����� �������Ⱑ ������� ���� ��ȯ�� ���߾� �����ϴ�.[0;37m')
                return
            if ob['����'] < 1000:
                ob.sendLine('[1;37m����� �������Ⱑ ������� ���� ��ȯ�� ���߾� �����ϴ�.[0;37m')
                return

            ob['����'] -= 1000

            from twisted.internet import reactor
            if line == '���Ĺ̺�':
                ob._miss += 350
                ob.sendLine('����� �߰����� [1;37m���[0;37m�ϸ� [1;36m����ڰ��[;37m�� �绡�� ���ĳ��ϴ�.')
                reactor.callLater(2, self.cool1, ob, line)
            elif line == '���ٰ�':
                ob._arm += 500
                ob._maxhp += 50
                ob._str += 500
                ob.sendLine('����� [1;33m�����[0;37m�� ��� [1;32m�Ѩ����[0;37m [1;31m���[0;37m�� ���ĳ��ϴ�.')
                reactor.callLater(3, self.cool1, ob, line)

            ob.cooltime[line] = 1
            return
        """
        s = None
        if mName in ob.skillList:
            s = MUGONG[mName]
        else:
            for sName in ob.skillList:
                if sName.find(mName) == 0:
                    s = MUGONG[sName]
                    break
        if s == None:
            ob.sendLine('�� �׷� ������ ������ ���� �����ϴ�.')
            return
        if s == '':
            ob.sendLine('�� ���� ����� �� ���� �����Դϴ�.')
            return
        
        if s['����'] == '����':
            if l == 1 and ob.act == ACT_STAND:
                ob.sendLine('�� ������ ��ĥ �� �ִ� ��밡 �ʿ��մϴ�.')
                return
            if is_item(mob) or is_box(mob):
                ob.sendLine('�� ��ȣ���� ������ �� �ִ°Ͱ� ���°��� ����!')
                return
            if ob.skill != None:
                ob.sendLine('[1;37m����� �������Ⱑ ������� ���� ��ȯ�� ���߾� �����ϴ�.[0;37m')
                return
            if ob.act == ACT_FIGHT and mob not in ob.target:
                ob.sendLine('�� ������ �񹫿� �Ű��� �����ϼ���. @_@')
                return
            if is_player(mob) and ob.env.checkAttr('�������������'):
                ob.sendLine('�� ������ [1m[31m���[0m[37m[40m�� ����Ű�⿡ �������� ��Ȳ �̶��')
                return
            # ����� ���� ������ ����
            if is_player(mob):
                ob.sendLine('�� ��ȣ���� ������ �� �ִ°Ͱ� ���°��� ����!')
                return
            if mob not in ob.target and mob['������'] != 1:
                ob.sendLine('�� ��ȣ���� ������ �� �ִ°Ͱ� ���°��� ����!')
                return
            if ob.getMp() < s.mp or ob['ü��'] <  (ob['�ְ�ü��'] * s.hp) / 100 or ob['ü��'] < (ob['�ְ�ü��'] * s.maxhp) / 100:
                ob.sendLine('[1;37m����� �������⸦ ���� �������� �Ⱑ ����� �����ϴ�.[0;37m')
                return
            ob['����'] -= s.mp
            ob['ü��'] -=  (ob['�ְ�ü��'] * s.hp) / 100
            ob.getSkill(s.name)
            ob.skill.init()
            
            buf1, buf2, buf3 = ob.makeFightScript(s['������ũ��'], mob)
            ob.sendLine(buf1)
            ob.addStr(s.bonus, False)
            if ob.act == ACT_STAND:
                ob.sendRoom(buf3, noPrompt = True)
            else:
                ob.sendRoomFightScript(buf3)
            if mob not in ob.target:
                ob.setFight(mob)
            if ob.getDex() >= 4200:
                ob._advance = True
                ob.doFight(True)
        else:
            if l == 1:
                mob = ob
            attr = s['�Ӽ�'].splitlines()
            if '�ڽű���' in attr and mob == ob:
                ob.sendLine('�� �ڽſ��� ����� �� ���� �����Դϴ�. ^^')
                return
            if 'Ÿ�α���' in attr and mob != ob:
                ob.sendLine('�� �ڽŸ� ����� �� �ִ� �����Դϴ�. ^^')
                return
            if is_item(mob) or is_box(mob):
                ob.sendLine('�� ��ȣ���� ������ �� �ִ°Ͱ� ���°��� ����!')
                return
            for ss in mob.skills:
                # ���� ���� Ȥ�� ���� �迭�� ������ �ι��̻� ����Ҽ� ����. �Ӽ����� �迭������ �����µ� ���ʿ�
                if s.name == ss.name or s['�迭'] == ss.getAntiType():
                    ob.sendLine('[1m����� �������⸦ ���� �������� �Ⱑ ����� �����ϴ�.[0;37m')
                    return
            for ss in ob.skills:
                # ���� ���� Ȥ�� ���� �迭�� ������ �ι��̻� ����Ҽ� ����. �Ӽ����� �迭������ �����µ� ���ʿ�
                if s.name == ss.name or s['�迭'] == ss.getAntiType():
                    ob.sendLine('[1m����� �������⸦ ���� �������� �Ⱑ ����� �����ϴ�.[0;37m')
                    return
            if ob.getMp() < s.mp:
                ob.sendLine('[1m����� �������⸦ ���� �������� �Ⱑ ����� �����ϴ�.[0;37m')
                return
            if  ob['ü��'] < (ob['�ְ�ü��'] * s.hp) / 100 or ob['ü��'] < (ob['�ְ�ü��'] * s.maxhp) / 100:
                ob.sendLine('[1m����� �������Ⱑ ������� ���� ��ȯ�� ���߾� �����ϴ�.[0;37m')
                return
            ob['����'] -= s.mp
            ob['ü��'] -= (ob['�ְ�ü��'] * s.hp) / 100
            s = copy.copy(s)
            ob.skillUp(s)
            t = ob.skillMap[s.name][0]
            
            mob._str += s._str
            mob._dex += s._dex
            mob._arm += s._arm
            against = ''
            for at in attr:
                if at.find('��빫��') == 0:
                    aName = at[9:]
                    against = MUGONG[aName].clone()
                    break
            
            if against != '':
                chance = ob.getAttackChance(mob)

                if s['�迭'] == '�������' and mob.getMp() > 0:
                    if chance >= randint(0, 100):
                        try:
                            plus = mob.mp * against._mp / 100 * -1
                            if plus + ob['����'] > ob['�ְ���']:
                                plus = ob['�ְ���'] - ob['����']
                            ob['����'] += plus
                            mob.mp -= plus
                        except:
                            plus = mob['����'] * against._mp / 100 * -1
                            if plus + ob['����'] > ob['�ְ���']:
                                plus = ob['�ְ���'] - ob['����']
                            ob['����'] += plus
                            mob['����'] -= plus
                elif s['�迭'] == '��������':    
                    mob._mp += against._mp
                    mob._maxmp += against._maxmp
                    mob.skills.append(against)
                    if is_mob(mob):
                        against.end_time = time.time() + against['���ð�'] + against['���ð�����ġ'] * (t - 1)
                    else:
                        against.start_time = against['���ð�'] + against['���ð�����ġ'] * (t - 1)
                ob.skills.append(s)
            else:
                mob.skills.append(s)
                
            
            
            if is_mob(mob):
                s.end_time = time.time() + s['���ð�'] + s['���ð�����ġ'] * (t - 1)
            s.start_time = s['���ð�'] + s['���ð�����ġ'] * (t - 1)
            buf1, buf2, buf3 = ob.makeFightScript(s['������ũ��'], mob)
            try:
                ob.sendLine(buf1 + ' ([1;36m+ %d[0;37m)' % plus)
            except:
                ob.sendLine(buf1)

#if mob != ob:
#                mob.sendLine(buf2)
#                mob.lpPrompt()
                
            if mob != ob and is_player(mob):
                mob.sendLine('\r\n' + buf2)
                mob.lpPrompt()
                ob.sendFightScriptRoom(buf3, ex = mob)
            else:
                ob.sendFightScriptRoom(buf3)
