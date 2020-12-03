# -*- coding: euc-kr -*-

from objs.cmd import Command

class CmdObj(Command):

    def cmd(self, ob, line):
        from lib.script import get_arm_script
        ob.sendLine('收收收收收收收收收收收收收收收收收收收收收收收收收收收')
        ob.sendLine('[0m[44m[1m[37mⅠ %-51s[0m[37m[40m' % han_parse('渡褐', get_arm_script(ob)))
        ob.sendLine('式式式式式式式式式式式式式式式式式式式式式式式式式式式')
        c = 0
        item_str = ''
        for lv in ob.ItemLevelList:
            for item in ob.objs:
                if item.inUse and lv == item['啗類']:
                    c += 1
                    name = stripANSI(item.get('檜葷'))
                    if is_han(name):
                        item_str += '[' + ob.ItemUseLevel[item.get('啗類')] + '] [36m' + item.get('檜葷') + '[37m\r\n'
                    else:
                        item_str += '[' + ob.ItemUseLevel[item.get('啗類')] + '] [36m' + item.get('檜葷') + '(' + item.get('奩擬檜葷').split()[0] + ')[37m\r\n'
        ob.write(item_str)
        if c == 0:
            ob.sendLine('[36mＣ ⑸⑸欽褐 裔跺戲煎 鬼�ㄧ� 輿嶸醞殮棲棻.[37m')
        ob.sendLine('式式式式式式式式式式式式式式式式式式式式式式式式式式式')
        ob.sendLine('□寞橫溘■Ⅰ %d    □奢問溘■Ⅰ %d' % (ob.getArmor(),ob.getAttPower()))
        ob.sendLine('收收收收收收收收收收收收收收收收收收收收收收收收收收收')
