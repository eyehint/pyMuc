from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        from lib.script import get_arm_script
        ob.sendLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        ob.sendLine('[0m[44m[1m[37m▷ %-51s[0m[37m[40m' % han_parse('당신', get_arm_script(ob)))
        ob.sendLine('───────────────────────────')
        c = 0
        item_str = ''
        for lv in ob.ItemLevelList:
            for item in ob.objs:
                if item.inUse and lv == item['계층']:
                    c += 1
                    name = stripANSI(item.get('이름'))
                    if is_han(name):
                        item_str += '[' + ob.ItemUseLevel[item.get('계층')] + '] [36m' + item.get('이름') + '[37m\r\n'
                    else:
                        item_str += '[' + ob.ItemUseLevel[item.get('계층')] + '] [36m' + item.get('이름') + '(' + item.get('반응이름').split()[0] + ')[37m\r\n'
        ob.write(item_str)
        if c == 0:
            ob.sendLine('[36m☞ 혈혈단신 맨몸으로 강호를 주유중입니다.[37m')
        ob.sendLine('───────────────────────────')
        ob.sendLine('【방어력】▷ %d    【공격력】▷ %d' % (ob.getArmor(),ob.getAttPower()))
        ob.sendLine('━━━━━━━━━━━━━━━━━━━━━━━━━━━')
