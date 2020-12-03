mp_script = [
'(은/는) [1;32m소주천[0;37;40m을 하고 있습니다.',
'(은/는) [1;32m대주천[0;37;40m을 하고 있습니다.',
'(은/는) [1m안광[0;37;40m이 [1;33m형형[0;37;40m하고 [1;32m태양혈[0;37;40m이 튀어나와 있습니다.',
'(은/는) [1m무인의 꿈[0;37;40m인 [1;33m생[37mㆍ[33m사[37m ㆍ[33m현[37mㆍ[33m관 [32m임독양맥[0;37;40m이 타동되었습니다.',
'(은/는) 상단전 [33m중단전[40m[37m [1;33m하단전[0;37;40m의 기운을 모아 [1;32m삼화취정[0;37;40m의 단계를 이루었습니다.',
'(은/는) [1m오행의 기운[0;37;40m을 조절하는 [1;32m오기조원[0;37;40m의 경지에 도달 했습니다.',
'(은/는) 무공이 드러나지 않는 [1;32m노화순청[0;37;40m의 경지에도달 했습니다.',
'의 귀밑머리가 희어지고 안광을 갈무리하는 [1;32m반박귀진[0;37;40m에 도달했습니다.',
'(은/는) [1m운기조식의 절정[0;37;40m인 [1;32m등복조극[0;37;40m의 경지에 도달했습니다.',
'(은/는) [1m여섯호흡이 근본[0;37;40m으로 돌아가는 [1;32m육식 귀전[0;37;40m을 이루었습니다.',
'(은/는) 늙음을 돌이켜 아이로 돌아가는 [1;32m반노환등[0;37;40m의 경지 입니다.',
'(은/는) [1;36m음신[40m[37m과 [31m양신[0;37;40m을 만들어내 는 [1;32m출신입화지경[0;37;40m을 이루었습니다.',
'(은/는) 인간의 육신으로 [1m신선의 경지[0;37;40m에 오르는 [1;32m우화등선[0;37;40m을 이루었습니다.',
'(은/는) 사기로 내공을 올렸습니다.'
]

def get_mp_script(ob):
    mp = ob.get('내공')
    if mp >= 0 and mp <= 100:
        return mp_script[0]
    elif mp > 100  and mp <=250 :
        return mp_script[1]
    elif mp > 251 and mp <= 400:
        return mp_script[2]
    elif mp > 401 and mp <= 600:
        return mp_script[3]
    elif mp > 601 and mp <= 800:
        return mp_script[4]
    elif mp > 801 and mp <= 1050:
        return mp_script[5]
    elif mp > 1051 and mp <= 1300:
        return mp_script[6]
    elif mp > 1301 and mp <= 1550:
        return mp_script[7]
    elif mp > 1551 and mp <= 1850:
        return mp_script[8]
    elif mp > 1851 and mp <= 2150:
        return mp_script[9]
    elif mp > 2151 and mp <= 2550:
        return mp_script[10]
    elif mp > 2551 and mp <= 3050:
        return mp_script[11]
    elif mp > 3051 and mp <= 9999:
        return mp_script[12]
    elif mp > 9999:
        return mp_script[13]
    return mp_script[0]

hp_script = [
    '(은/는) 아주 활력이 넘칩니다.',
    '의 팔다리에 약간의 다친 흔적이 보입니다.',
    '의 가슴에서 피가 번지기 시작합니다.',
    '(은/는) 피를 약간씩 흘리고 있습니다.',
    '의 이곳 저곳에 깊은 상처를 입었습니다.',
    '(이/가) 몸을 조금 비틀거리고 있습니다.',
    '(이/가) 몸을 가누기 어려울 정도로 비틀거리고 있습니다.',
    '(이/가) 신음소리를 내며 쓰러질것 같이 휘청 거립니다.',
    '(이/가) 정신을 잃을정도로 혼미한 상태에 이르렀습니다.',
    '(이/가) 피가 분수처럼 뿜어져 나오며 숨을 헐떡 거립니다.',
    '(은/는) 숨이 멈출듯 헐떡 거리며 의식이 몽롱합니다.',
    '(이/가) 몸을 움직일수 없이 휘청거립니다.',
    '(은/는) 의식을 잃어가고 죽음의 문턱을 넘나듭니다.',
    '(은/는) 가느다란 숨만 몰아쉬고 죽음의 문과 가깝게 있습니다.',
    '에게 저승사자가 손짓하고 있습니다.'
]

def get_hp_script(ob):
    curhp = ob.get('체력')
    maxhp = ob.get('최고체력')
    if curhp > maxhp:
        curhp = maxhp
    cnt = len(hp_script)
    return hp_script[(cnt - 1) - ((cnt - 1) * curhp / maxhp)]

arm_script = [
'의 몸을 눈부신 광채가 찬란히 보호 합니다.',
'의 몸에서 은은한 광채가 뿜어져 나옵니다.',
'(을/를) 모든 무림인이 우러러 봅니다.',
'의 위엄에 모든 사람이 고개를 숙입니다.',
'(을/를) 다른 무림인들이 똑바로 바라보지 못합니다.',
'(은/는) 환상적인 방어구를 착용하고 있습니다.',
'(은/는) 어마어마한 방어구를 착용하고 있습니다.',
'(은/는) 아주 강력한 방어구를 착용하고 있습니다.',
'(은/는) 강력한 방어구를 착용하고 있습니다.',
'(은/는) 튼튼한 방어구를 착용하고 있습니다.',
'(은/는) 쓸만한 방어구를 착용하고 있습니다.',
'(은/는) 그럭저럭 쓸만한 방어구를 착용하고 있습니다.',
'의 방어구는 형식만 갖추고 있습니다.',
'(은/는) 초라한 방어구를 착용하고 있습니다.',
'(은/는) 형편없는 방어구를 착용하고 있습니다.',
'(은/는) 너무나 형편없는 방어구를 착용하고 있습니다.',
'(은/는) 주위의 동정을 사기에 충분합니다.',
'(은/는) 불쌍함이 몸에서 철철 흐르고 있습니다.',
'(은/는) 거의 벗다시피 하고 있습니다.',
]


def get_arm_script(ob):
    arm = ob.getArmor()
    if arm is None:
        arm = 0
    if arm >= 0 and arm <= 10:
        return arm_script[18]
    if arm >= 11 and arm <= 31:
        return arm_script[17]
    if arm >= 32 and arm <= 57:
        return arm_script[16]
    if arm >= 58 and arm <= 88:
        return arm_script[15]
    if arm >= 89 and arm <= 119:
        return arm_script[14]
    if arm >= 120 and arm <= 135:
        return arm_script[13]
    if arm >= 136 and arm <= 176:
        return arm_script[12]
    if arm >= 177 and arm <= 217:
        return arm_script[11]
    if arm >= 218 and arm <= 262:
        return arm_script[10]
    if arm >= 263 and arm <= 313:
        return arm_script[9]
    if arm >= 314 and arm <= 368:
        return arm_script[8]
    if arm >= 369 and arm <= 429:
        return arm_script[7]
    if arm >= 430 and arm <= 495:
        return arm_script[6]
    if arm >= 496 and arm <= 566:
        return arm_script[5]
    if arm >= 557 and arm <= 642:
        return arm_script[4]
    if arm >= 643 and arm <= 723:
        return arm_script[3]
    if arm >= 724 and arm <= 804:
        return arm_script[2]
    if arm >= 805 and arm <= 885:
        return arm_script[1]
    if arm >= 886:
        return arm_script[0]

