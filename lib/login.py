# -*- coding: euc-kr -*-

from include.path import *
from include.define import *
from lib.object import *
from lib.hangul import *
from objs.cmd import Command
from lib.comm import broadcast
from lib.cmd import parse_command

def userlist(ob):
    list = '�� (' + str(len(ob.clients)) + ')\r\n'        
    #list = ''
    for c in ob.channel.clients:
        if len(c.get('�̸�')) != 0:
            list += ', ' + c.get('�̸�')
        else: 
            list += ', <������>'
                                                                   
    ob.sendLine(list);


def get_name(self, name, *args):
    if len(name) == 0:
        self.write('\r\n�̸� : ')
        return
    if is_han(name) == False:
        self.write('\r\n�ѱ� �Է¸� �����մϴ�.\r\�̸� : ')
        return
    if name == '�մ�':
        self.newidx = 0
        newbie_msg(self)
        self.input_to(DoNothing)
        return
    
    res = self.load(USER_PATH + name)
    if res == False:
        self.write('\r\n�׷� ����ڴ� �����ϴ�.\r\n�̸� : ')
        return
    #self.set('�̸�', name)
    self.write('\r\n��ȣ : ')
    self.loginRetry = 0
    self.input_to(get_pass)


def get_pass(self, line, *args):
    self.loginRetry += 1
    if len(line) == 0 or self.get('��ȣ') != line:
        if self.loginRetry >= 3:
            self.write('\r\n')
            self.channel.transport.loseConnection()
            return
        self.write('\r\n�߸��� ��ȣ �Դϴ�.\r\n��ȣ : ')
        return    
    #self.sendLine('\r\n�� ���̱�����^^ �ݰ�����')
    del self.loginRetry
    
    self.write('[2;28r[2J')

    self.state = ACTIVE
    self.channel.clients.append(self)
    self.channel.echoON()
    broadcast(self.get('�̸�') + '���� �����̽��ϴ�.', self)
    
    from lib.io import cat
    cat(self, 'data/text/notice.txt')
    self.sendLine('[Enter] Ű�� ��������.')
    self.input_to(showNotice)
    self.start_heart_beat()


def showNotice(self, line, *args):
    room = get_room('����/����')
    if room != None:
        room.append(self)

    self.INTERACTIVE = 1
    self.input_to(parse_command)


def newbie_msg(self):
    from twisted.internet import reactor
    
    self.newidx += 1
    
    if self.newidx == 1:
        self.write('[2J') # CLEAR SCREEN
    elif self.newidx == 2:
        self.sendLine('\r\n�ʱ��� ������ ���ô� ������ ������ ������ ���� .......')
    elif self.newidx == 3:
        self.sendLine('\r\n����� ��Ʈ���� ó���� ��� �Ҹ��� �ڷ� �ϰ� ���縦 �� Ż���� �ϴ� �̵���')
        self.sendLine('�־���.')
    elif self.newidx == 4:
        self.sendLine('\r\n�� ���� �系�� �� ������ �Ѿ��� ���� ����....')
    elif self.newidx == 5:
        self.sendLine('\r\n�� ���ڴ� �߳��� ������ ����̳� ���� �Ƿ� ����� �־��� �ٸ� �� ���ڴ�')
        self.sendLine('���� �λ��� ���� �� ���θ� �޼����� ���ΰ� ���� �տ� ���� ��� ������')
        self.sendLine('������� ���� �귯���� �ǰ� �˽��� Ÿ�� ���� ���� �귯 ������ �־���.')
    elif self.newidx == 6:
        self.sendLine('\r\n���ְ� ���մϴ�. "�ҷ�!, ���� �� �̻� ������ ���� �� ����...".')
        self.sendLine('                 "� �������� ��ð�  �� ���� ���������� ....."')
    elif self.newidx == 7:
        self.sendLine('\r\n                 "� �������� ��ð�  �� ���� ���������� ....."')
    elif self.newidx == 8:
        self.sendLine('\r\n������... ������... ������...������...')
    elif self.newidx == 9:
        self.sendLine('\r\n������... ������... ������...������...')
    elif self.newidx == 10:
        self.sendLine('\r\n������... ������... ������...������...')
    elif self.newidx == 11:
        self.sendLine('\r\n������... ������... ������...������...')
    elif self.newidx == 12:
        self.sendLine('\r\n������... ������... ������...������...')
    elif self.newidx == 13:
        self.sendLine('\r\n[Enter] Ű�� ��������.\r\n')
        self.input_to(NextPage)
        return
    elif self.newidx == 14:
        self.sendLine('\r\n�׷��� �����...')
    elif self.newidx == 15:
        self.sendLine('\r\n������... ������... ������...������...')
    elif self.newidx == 16:
        self.sendLine('\r\n������... ������... ������...������...')
    elif self.newidx == 17:
        self.sendLine('\r\n����� �̸��� �Է��ϼ���.\r\n�̸� : ')
        self.input_to(getNewname)
        return
    
    reactor.callLater(1, newbie_msg, self)


def DoNothing(self, line, *args):
    return


def NextPage(self, line, *args):
    from twisted.internet import reactor
    self.write('[2J') # CLEAR SCREEN
    self.input_to(DoNothing)
    reactor.callLater(3, newbie_msg, self)
    return
    

def getNewname(self, name, *args):
    if len(name) == 0:
        self.write('\r\n�ѱ��� �̻� �Է��ϼ���.\r\n�̸� : ')
        return
    if is_han(name) == False:
        self.write('\r\n�ѱ� �Է¸� �����մϴ�.\r\n�̸� : ')
        return
    if name == '�մ�':
        self.write('\r\n����� �� ���� �̸��Դϴ�.\r\n�̸� : ')
        return
    import os
    if os.path.exists(USER_PATH + name) == True:
        self.write('\r\n�̹� ������� �̸��Դϴ�.\r\n�̸� : ')
        return
    self.set('�̸�', name)
    self.write('\r\n����Ͻ� ��ȣ�� �Է��ϼ���.\r\n��ȣ : ')
    self.input_to(getNewpass)

def getNewpass(self, line, *args):
    if len(line) < 3:
        self.write('\r\n3�� �̻� �Է��ϼ���.\r\n��ȣ : ')
        return
    self.set('��ȣ', line)
    self.write('\r\n�ѹ� �� �Է��ϼ���.\r\n��ȣ : ')
    self.input_to(getNewpass2)


def getNewpass2(self, line, *args):
    if line != self.get('��ȣ'):
        self.write('\r\n���� �Է°� �ٸ��ϴ�.\r\n����Ͻ� ��ȣ�� �Է��ϼ���.\r\n��ȣ : ')
        self.input_to(getNewpass)
        return
    self.init_body()
    self.save(USER_PATH + self.get('�̸�'))
    self.write('[2;28r[2J')
    self.state = ACTIVE
    self.channel.clients.append(self)
    self.channel.echoON()
    broadcast(self.get('�̸�') + '���� �����̽��ϴ�.', self)
    
    from lib.io import cat
    cat(self, 'data/text/notice.txt')
    self.sendLine('[Enter] Ű�� ��������.')
    self.input_to(showNotice)
    self.start_heart_beat()
