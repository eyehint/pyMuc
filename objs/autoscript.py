# -*- coding: euc-kr -*-

class autoScript():
    def start(self, script, player):
        self.tick = 0
        self.lineNum = 0
        self.player = player
        self.script = script
        self.lastNum = len(script)
        self.run()
        self.name = ''
        
    def run(self):
        print(self.player['�̸�'] + ' %d/%d' %(self.lineNum, self.lastNum))
        if self.player == None:
            return
        printLine = False
        loopcount = 0
        while(True):
            if loopcount > 50:
                print('Exceed loop count in autoscript.py : lineNum = %d' % self.lineNum)
                self.player.sendLine('* ����մϴ�.')
                self.player.stopAutoScript()
                return
            
            if self.lineNum >= self.lastNum:
                self.player.stopAutoScript()
                return
            line = self.script[self.lineNum].strip()
            if line == '':
                self.player.sendLine('')
            elif line[0] == '#':
                self.lineNum += 1
                continue
            elif line[0] == '$':
                l = line.strip()
                if  l == '$��½���':
                    printLine = True
                elif l == '$��³�':
                    printLine = False
                    self.lineNum += 1
                    continue
                elif l[:5] == '$����':
                    self.player.stopAutoScript()
                    return
                elif l[:3] == '$ƽ':
                    tick = getInt(l[4:])
                    if tick != 0:
                        self.tick = tick * 0.1 * 1.5
                    self.lineNum += 1
                    continue
                elif l[:7] == '$Ű�Է�':
                    key = l.find(':')
                    if key == -1:
                        self.player.input_to(self.player.pressEnter1)
                    else:
                        self.player.input_to(self.player.getKeyInput, l[key + 1:])
                    self.lineNum += 1
                    return
                elif l[:9] == '$�ѱ�Ȯ��':
                    if is_han(stripANSI(self.player.temp_input)) == False:
                        self.lineNum -= int(l[10:])
                        self.player.sendLine('�ѱ۸� �Է� �����մϴ�. �ٽ� �Է��ϼ���.')
                        continue
                elif l[:9] == '$�ܾ��Է�':
                    words = l[10:].split()
                    limit = 10
                    keywords = []
                    if len(words) > 0:
                        limit = int(words[0])
                        if len(words) == 2:
                            keywords = words[1].split(',')
                    self.lineNum += 1
                    self.player.input_to(self.player.getWord, limit, keywords)
                    return
                elif l[:9] == '$�����Է�':
                    self.lineNum += 1
                    self.player.input_to(self.player.getLine, l[10:])
                    return
                elif l[:9] == '$�����Է�':
                    self.lineNum += 1
                    self.player.temp_input = []
                    self.player.sendLine('�Է��� ��ġ�÷��� \'.\' �� �Է��ϼ���.')
                    self.player.input_to(self.player.getLines, l[10:])
                    return
                elif l[:9] == '$�Է�Ȯ��':
                    self.lineNum += 1
                    from __builtin__ import type
                    if type(self.player.temp_input) == list:
                        self.player.write('�Է��Ͻ� ������ �½��ϱ�? (��/���) : ')
                    else:
                        self.player.write('�Է��Ͻ� ������ \'' + self.player.temp_input + '\' �½��ϱ�? (��/���) : ')
                    self.player.input_to(self.player.checkInput)
                    return
                elif l[:9] == '$�ߺ�Ȯ��':
                    find = False
                    for index in Item.Items:
                        item = Item.Items[index]
                        if item['�̸�'] == stripANSI(self.player.temp_input):
                            self.lineNum -= int(l[10:])
                            self.player.sendLine('�ߺ��� �̸��� �ֽ��ϴ�. �ٽ� �Է��ϼ���.')
                            find = True
                            break
                    if find == True:
                        continue
                elif l[:9] == '$�������':
                    #self.player.temp_item = Item() �Ǵ�
                    self.player.temp_item = getItem('�ü�����').deepclone()
                    self.player.temp_item.index = self.player['�̸�'] + '_�ü�����' 
                    self.player.temp_item.path = 'data/item/' + self.player.temp_item.index + '.itm'
                    type = int(self.player.temp_input) 
                    self.player.temp_item['��������'] = type
                    if type == 1:
                        msg = '��'
                    elif type == 2:
                        msg = '��'
                    elif type == 3:
                        msg = 'â'
                    elif type == 4:
                        msg = '��Ÿ'
                    elif type == 5:
                        msg = '�ָ�1'
                    self.player.temp_item['������ũ��'] = msg
                    self.player.temp_item['�����'] = self.player['�̸�']
                elif l[:9] == '$����Ӽ�':
                    if l[10:] == '�̸�':
                        self.player.temp_item[l[10:]] = self.player.temp_input
                        self.player.temp_item['�����̸�'] = stripANSI(self.player.temp_input)
                    elif l[10:] == '����2':
                        self.player.temp_item['����2'] = ''
                        for li in self.player.temp_input:
                            self.player.temp_item['����2'] += li + '\r\n'
                    elif l[10:] == '�����̸�':
                        mugong = self.player.temp_input 
                        jung = ['ö����', '�ݰ���', '��ȭ����', '�ݰ�����', '��ȭ������', '������ȯ', '��ȣ��', '������', '�Ѻ���', '���ؽ���', 'ȭ��������', 'û����', '�麸�ű�', 'ź���Ű�', 'Ż����', '��±ݰ���', '�ݾߴ����', 'õ������', '��ȭ����', 'ȥõ��', '���ݽŷ���', '���ش��', '�����Ͻ�', '��ȭ����', '��õ��', '��������', '��������', '��â����', '�����Ű�', '��Ż��ȭ', '������', '��ȭ������', 'õ�������', '�����Ͻ�', '��õ���ذ�', '�޸����', 'ǥ�����', '����ȥ��', '�������氭', '��������', '���ذ�']

                        sa = ['��õȣ��', '���߼�', '��ǥ��', '�ո���', '��õ��', '������', '��������', '�����', '������', 'ǳ����', '���꼳ȭ', 'ȭ������', '�������', '�Ҽ���', '��ȭ��õ', '������', '��ȭ��', '��õ����', '���������', '�����', '��������', '���ݽŷ���', '��õȭ��', '������', '��õ�ݳ�', '���ɴ�ȥ', '��������', '��õ��', '��Ȳ�����', '������', '������', '�ܻ�������', '��õ����', 'õ����', 'õ�����ݽ���', '�����', 'õ����', '����õ��']
                        if mugong in jung:
                            type = '����'
                        elif mugong in sa:
                            type = '����'
                        else:
                            type = '����'

                        self.player.temp_item['�����̸�'] = '%s %s 1000000 10000000 10' % (mugong, type)
                    else:
                        self.player.temp_item[l[10:]] = self.player.temp_input
                    #�̸�
                    #�����̸�
                    #��뽺ũ��
                    #��������

                    #�����̸�
                    #����1
                    #����2
                    pass
                elif l[:13] == '$���õ�����':
                    if self.player.temp_input == '1':
                        self.player.temp_move = 1
                    else:
                        self.player.temp_move = 0
                elif l[:11] == '$���õ�����':
                    if self.player.temp_move == 1:
                        main = self.player.temp_item['��������']
                        exp = 0
                        for i in range(1,6):
                            if i == main:
                                continue
                            s = self.player['%d ���õ�' % i]
                            exp += self.player['%d ���õ�����ġ' % i]
                            for i in range(0, s+1):
                                exp += (i + 5) * 7
                        s = self.player['%d ���õ�' % main]
                        a = 0
                        while(True):
                            e = (s + a + 1 + 5) * 7 
                            if exp - e < 0:
                                break
                            exp -= e
                            a += 1
                        self.player['%d ���õ�' % main] = s + a
                        for i in range(1,6):
                            if i == main:
                                continue
                            self.player['%d ���õ�' % i] = 0
                            self.player['%d ���õ�����ġ' % i] = 0
                        self.player.sendLine('�� ���õ� ����ġ�� �Ű������ϴ�.')
                elif l[:9] == '$��������':
                    self.player['�ü��Ϸ�'] = 1
                    self.player.temp_item.save()
                    del self.player.temp_item
                    self.player.temp_item = None
                    item = getItem(self.player['�̸�'] + '_�ü�����').deepclone()
                    self.player.objs.append(item)
                    self.player.save()
                elif l[:11] == '$�����ۻ���':
                    index, cnt = getStrCnt(line)
                    self.player.delItem(index, cnt)
                elif l[:11] == '$������Ȯ��':
                    if self.player.checkItemName(self.player.temp_input, 1) == False:
                        self.player.sendLine('�� �׷� �������� ����ǰ�� �����.')
                        self.player.sendLine('* ���Ⱝȭ�� �����մϴ�.')
                        self.player.stopAutoScript()
                        return
                    self.player.temp_item = self.player.getItemName(self.player.temp_input)
                    """
                        self.player.sendLine('�� ���⸸ �����մϴ�.')
                        self.player.sendLine('* ���Ⱝȭ�� �����մϴ�.')
                        self.player.stopAutoScript()
                        return
                    """ 
                elif l[:9] == '$�ɼ�Ȯ��':
                    if self.player['�ְ���'] < 5:
                        self.player.sendLine('�� ������ �����ؿ�.')
                        self.player.sendLine('* ���Ⱝȭ�� �����մϴ�.')
                        self.player.stopAutoScript()
                        return

                    op = self.player.temp_input
                    item = self.player.temp_item
                    option = item.getOption()
                    if op == '����':
                        self.player.sendLine('�� �ش� Ư��ġ�� �ȵǿ�.')
                        self.player.sendLine('* ���Ⱝȭ�� �����մϴ�.')
                        self.player.stopAutoScript()
                        return

                    if op not in option:
                        self.player.sendLine('�� �׷� Ư��ġ�� �����.')
                        self.player.sendLine('* ���Ⱝȭ�� �����մϴ�.')
                        self.player.stopAutoScript()
                        return
                    val = option[op]
                    myItem = self.player.getItemIndex(self.player['�̸�'] + '_�ü�����')
                    if myItem == None or myItem.inUse == True:
                        self.player.sendLine('�� ���⸦ ���� �ϼ���.')
                        self.player.sendLine('* ���Ⱝȭ�� �����մϴ�.')
                        self.player.stopAutoScript()
                        return
                    myOp = myItem.getOption()
                    if myOp == None:
                        myOp = {}
                    if op not in myOp:
                        myVal = 0
                    else:
                        myVal = myOp[op]
                    if myVal >= val:
                        self.player.sendLine('���� Ư��ġ ������ ���ƾ� �մϴ�.')
                        self.player.sendLine('* ���Ⱝȭ�� �����մϴ�.')
                        self.player.stopAutoScript()
                        return
                    d = int( (val - myVal) / 3 )
                    if d == 0:
                        d = 1     
                    myOp[op] = myVal + d
                    myItem.setOption(myOp)
                    if myItem['���ݷ�'] < 9999:
                        myItem['���ݷ�'] = myItem['���ݷ�'] + 10
                        myItem['�ⷮ'] = myItem['���ݷ�']
                    self.player['�ְ���'] = self.player['�ְ���'] - 5
                    self.player.delItem(item.index, 1)
                    myItem.save()
                    self.player.save()

                elif l[:9] == '$�ɼ����':
                    item = self.player.temp_item
                    if item == None:
                        self.player.sendLine('* ���Ⱝȭ�� �����մϴ�.')
                        self.player.stopAutoScript()
                        return
                    option = item.getOption()
                    if option is None:
                        self.player.sendLine('�� �ش� �������� Ư��ġ�� �����.')
                        self.player.sendLine('* ���Ⱝȭ�� �����մϴ�.')
                        self.player.stopAutoScript()
                        return
                    self.player.sendLine(item.getOptionStr())
                elif l[:9] == '$���Ⱝȭ':
                    pass
                
            else:
                #msg = line.replace('[��]', self.player['�̸�'])
                #self.player.write(postPosition1(msg))
                self.player.sendLine(line)
            self.lineNum += 1
            if printLine == True:
                continue
            if self.tick == 0:
                continue
            reactor.callLater(self.tick, self.run)
            break
