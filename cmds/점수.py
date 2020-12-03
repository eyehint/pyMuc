# -*- coding: euc-kr -*-

from objs.cmd import Command
from include.ansi import *

class CmdObj(Command):

    def cmd(self, ob, line):
        write = ob.sendLine
        get = ob.get
        write('Ｃ ' + ob.getDesc(True))
        write('牟收收收收收收收收收收收收收收收收收收收收收收收收收收收汕')
        write('弛[0m[44m[1m[37m ⅠⅡⅠⅡⅠⅡ      渡褐曖 ⑷營 鼻鷓      ９８９８９８ [0m[40m[37m弛')
        write('汝收收收收收收收收收收收收收次收收收收收收收收收收收收收汙')
        write('弛 [溯  漣]        [%6d] 弛 [釭  檜]          %6d 弛' % (get('溯漣'), get('釭檜')) )
        temp = '%d/%d' % (ob.getHp(), ob.getMaxHp())
        tmp = get('撩問')
        if tmp == '':
            tmp = '----------'
        write('弛 [羹  溘] %15s 弛 [撩  問]      %10s 弛' % (temp, tmp))
        temp = 0
        
        write('弛 [  ��  ]  %5d + %6d 弛 [撩  滌]              %2s 弛' % (ob.getAttPower(), ob.getStr(), get('撩滌')) )
        tmp = get('模樓')
        if tmp == '':
            tmp = '----------'
        write('弛 [裝  餵] %6d + %6d 弛 [模  樓]      %10s 弛' % (ob.getArmor(), ob.getArm(), tmp) )
        tmp = get('霜嬪')
        if tmp == '':
            tmp = '----------'
        else:
            g = GUILD[ob['模樓']]
            if '%s貲蘆' % ob['霜嬪'] in g:
                tmp = g['%s貲蘆' % ob['霜嬪']]
            else:
                tmp = ob['霜嬪']
        write('弛 [團  繪] %15d 弛 [霜  嬪]      %10s 弛' % (ob.getDex(), tmp) )
        write('弛 [暀  齌] %15d 弛 [��  靋] %15d 弛' % (ob.getHit(), ob.getMiss()))
        write('弛 [饡  蒍] %15d 弛 [  瞗  ] %15d 弛' % (ob.getCritical(), ob.getCriticalChance()))
        tmp = get('寡辦濠')
        if tmp == '':
            tmp = '----------'
        temp = '%d/%d' % (ob.getMp(), ob.getMaxMp())
        #write('弛 [頂  奢] %15d 弛 [寡辦濠]      %10s 弛' % (ob.getMp(), tmp) )
        write('弛 [頂  奢] %15s 弛 [寡辦濠]      %10s 弛' % (temp, tmp) )

        temp = '%d/%d' % (ob.getItemWeight(), ob.getStr() * 10)
        write('弛 [⑷  唳] %15d 弛 [模雖ヶ] %15s 弛' % (ob['⑷營唳я纂'], temp) )
        anger = getInt(ob['碟喻'])
        if anger >= 100:
            temp = '[1;31m%d[0;37m' % anger
        else:
            temp = '%d' % anger
        write('弛 [跡  唳] %15d 弛 [碟  喻]             %3s 弛' % (ob.getTotalExp(), temp))
        write('戍式式式式式式式式式式式式式扛式式式式式式式式式式式式式扣')
        write('弛[0m[47m[30m [擎  瞪]    %40d [0m[40m[37m弛' % get('擎瞪'))
        if ob['旎瞪'] == '':
            ob['旎瞪'] = 0
        if ob['旎瞪'] > 0:
            write('弛[0m[43m[30m [旎  瞪]    %40d [0m[40m[37m弛' % get('旎瞪'))
        write('汎收收收收收收收收收收收收收收收收收收收收收收收收收收收汛')
        if ob['模樓'] != '':
            g = GUILD[ob['模樓']]
            if '%s貲蘆' % ob['霜嬪'] in g:
                buf = g['%s貲蘆' % ob['霜嬪']]
            else:
                buf = ob['霜嬪']
            temp = ''
            if ob['寞だ滌��'] != '':
                temp = '(%s)' % ob['寞だ滌��']
            write('≠ %s%s [1m□%s■[0m 僥だ曖 [1m%s%s[0m 殮棲棻.' % \
                ('渡褐', han_un('渡褐'), ob['模樓'], buf, temp ))
        from lib.script import get_hp_script, get_mp_script
        write( '≠ ' + han_parse('渡褐', get_hp_script(ob)) )
        p = ob.getInsureCount()
        if p == 0:
            ob.sendLine('≠ 渡褐曖 ル措爾я擎 �蕙臍� 橈蝗棲棻.')
        else:
            ob.sendLine('≠ 渡褐擎 %d廓曖 ル措爾я ��鷗擊 嫡戲褒 熱 氈蝗棲棻.' % p)
        write( '≠ ' + han_parse('渡褐', get_mp_script(ob)) )

        p = getInt(ob['か撩纂'])
        if p != 0:
            ob.sendLine('≠ 渡褐擎 %d偃曖 罹嶸 か撩纂蒂 爾嶸ж堅 氈蝗棲棻.' % p)
