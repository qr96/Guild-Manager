
#단어 비교 함수
def compare(arr_a, arr_b):
    for a in arr_a:
        print(a)
        for b in arr_b:
            #유사한 경우
            if similar(a[0], b[0]) >= 0.5:
                if a[-2] == 'I' or a[-2] == 'I!':
                    b[-2] = '0'
                elif a[-2].isdigit:
                    b[-2] = a[-2]

                if a[-1] == 'I' or a[-1] == 'I!' or a[-1] == "ø" or a[-1] == "1":
                    b[-1] = '0'
                elif a[-1][0:2] == "10":
                    b[-1] = '100'
                elif a[-1][0:2].isdigit:
                    b[-1] = a[-1][0:2]+'0'
                elif a[-1].isdigit:
                    b[-1] = a[-1]

    return arr_b


# 단어 유사도 측정 함수
def similar(a, b):
    return Jaccad(a, b)

# 자카드 유사도, 이 방법이 정확하진 않음... 제대로된 유사도 검사 필요
def Jaccad(a, b):
    ua = a.encode("UTF-8")
    ub = b.encode("UTF-8")

    sa = set()
    sb = set()

    for e in ua:
        sa.add(e)

    for e in ub:
        sb.add(e)

    inter = len(sa & sb)
    union = len(sa | sb)

    return inter/union


