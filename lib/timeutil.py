# -*- coding: euc-kr -*-
from time import ctime

dicMonth = \
{ 'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4,  'May':5,  'Jun':6,
  'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12 }
  
#'Fri Dec 02 11:01:26 2005'
#---------------------------------------
# ����          : [xx��/xx��]�� ����ó��.
# nTimeStamp    : Ÿ�ӽ�������.
#---------------------------------------
def frmTime_A(nTimeStamp):
    
    strFormat = ctime(nTimeStamp)
    strFormat = strFormat.replace('  ', ' ')
    lstFormat = strFormat.split(' ')
    strDay, strMonth, strNday, strNtime, strNyear = lstFormat
 
    nDay = int(strNday)
 
    return '[%2d��/%2d��]' % (dicMonth[strMonth], nDay)
