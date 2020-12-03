# -*- coding: euc-kr -*-

#---------------------------------------
# ���� : ������ ����
#---------------------------------------
def read_file(strFileName):

    try:
        fp = open(strFileName)
    except IOError:
        return None 
    else:
        strDesc = ''
        strLine = fp.readline()

        while strLine:
            strDesc += line + "\r"
            strLine = f.readline()

        fp.close()
        return strDesc

#---------------------------------------
# ���� : ���Ͽ� ���.
# strFileName   : ���� ���
# strDesc       : ����� ����
# strWriteMode  : � ���� ����ұ�?
#---------------------------------------
def write_file(strFileName, strDesc = '', strWriteMode = 'w'):
    
    try:
        fp = open(strFileName, strWriteMode)
    except IOError:
        return False
    else:
        fp.write(strDesc)
        fp.close()
        return True
        

def cat(ob, filename):
    try:
        f = open(filename, 'U')
    except IOError:
        ob.sendLine('[''filename' '] �� �� �����ϴ�.')
    
    else:
        ob.sendLine(f.read().replace('\n', '\r\n'))
        #ob.sendLine(f.read())
        f.close()    

