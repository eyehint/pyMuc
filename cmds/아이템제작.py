from objs.cmd import Command
from lib.hangul import *

class CmdObj(Command):
    def cmd(self, ob, line):
        words = line.split()
        if len(words) < 1:
            ob.sendLine('☞ 사용법: [파일명] 아이템제작')
            return
        if getInt(ob['관리자등급']) < 1000:
            ob.sendLine('☞ 무슨 말인지 모르겠어요. *^_^')
            return
        ob.write('작성을 마치시려면 \'.\' 를 입력하세요.\r\n:')
        ob.INTERACTIVE = 0
        ob._lineData = ''
        ob._lineDataTarget = 'item/' + words[0] + '.itm'
        ob.input_to(ob.write_edit)

