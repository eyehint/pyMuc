# -*- coding: euc-kr -*-

from os import makedirs
from os.path import isfile, split
from lib.io import write_file
from lib.sutil import isNull

#---------------------------------------
# ���� : �α� ���.
# strFilePath   : ����� ���� ���.
# strDesc       : ����� ����
#---------------------------------------
def writeLog(strFilePath, strDesc = ''):

    if  isNull(strFilePath) is True:
        return

    strDesc = procDesc(strDesc)
        
    if  isfile(strFilePath) is True:
        write_file(strFilePath, strDesc, 'a')

    else:
        tupPath = split(strFilePath)
        try:
        #-------------------------------------
        # ���͸��� �̹� �����Ѵٸ�? except
            makedirs(tupPath[0])
        except OSError:
            pass
        
        bResult = write_file(strFilePath, strDesc)


#---------------------------------------
# ���� : [xx��/xx��] �α׳��� ���� ����
#---------------------------------------
# writeLog ���������� �����.
def procDesc(strDesc):
    from time import time
    from lib.timeutil import frmTime_A
    
    return frmTime_A(time()) +' '+ strDesc + "\n"
