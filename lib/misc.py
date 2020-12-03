def status_ansi(ob):
    from include.ansi import *
    hp = ob.get('체력')
    maxhp = ob.get('최고체력')
    mp = ob.get('내공')
    maxmp = ob.get('최고내공')

    hcnt = 20*hp/maxhp
    msg = '[1;1H' + HIR
    for i in range(hcnt):
        msg += '━'
    msg += RED
    for i in range(20-hcnt):
        msg += '━'
    
    mcnt = 20*mp/maxmp
    msg += HIB
    for i in range(mcnt):
        msg += '━'
    msg += BLU
    for i in range(20-mcnt):
        msg += '━'
    msg += WHT + '[26;1H'
    ob.sendLine(msg);
