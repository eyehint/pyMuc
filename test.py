import os
from unicodedata import normalize

target = './data/script'
dirs = os.listdir(target)
os.chdir(target)
for directory in dirs:
    filename_nfc = normalize('NFC', directory)
    os.rename(directory, filename_nfc.encode('ISO-8859-1').decode('cp949'))
    print(filename_nfc.encode('ISO-8859-1').decode('cp949'))

