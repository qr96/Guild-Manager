import requests
from bs4 import BeautifulSoup as bs

#월드 코드
world = {'0':'스카니아', '1' : '베라', '3' : '루나', '4' : '제니스',
         '5' : '크로아', '10' : '유니온', '16' : '엘리시움', '29' : '이노시스',
         '43' : '레드', '44' : '오로라', '45' : '리부트', '46' : '리부트2',
         '48' : '버닝2', '49' : '버닝', '50' : '아케인', '51' : '노바',
         '52' : '버닝3'}

#길드 검색 함수,  [길드코드, 길드마스터, 월드] 반환
def search(guildName):
    link = "https://maplestory.nexon.com/Ranking/World/Guild?w=0&n=" + guildName;
    page = requests.get(link)
    soup = bs(page.text, "html.parser")

    elements = soup.select('table.rank_table2 tbody tr')

    guildCodes = []

    for e in elements:
        #guildCode.append(e.attrs['href'])
        code = e.select('a')[0].attrs['href'] #길드 코드
        master = e.select('span.gd_name')[0].text #길드마스터 이름
        wid = code.split('=')[-1] #월드 코드
        w_name = world[wid] #월드 이름
        tmp = [code, master, w_name]
        guildCodes.append(tmp)
        #print(tmp)
    #print(guildCodes)

    return guildCodes

    #print(guildCode)
    #print(guildMaster)
    #print(world[4])



#길드원 정보 여러 페이지에서 파싱 [직위, 닉네임, 레벨, 기여도, 수로, 플래그] 출력
def find_all_page(code):
    members = []
    for i in range(1,11):
        members = members + find_one_page('https://maplestory.nexon.com'+code+'&orderby=0&page='+str(i))

    return members


#길드원 정보 한페이지 파싱
def find_one_page(link):
    #link = 'https://maplestory.nexon.com/Common/Guild?gid=300219&wid=4&orderby=0&page=5'
    page = requests.get(link)
    soup = bs(page.text, "html.parser")
    elements = soup.select('div.guild_user_list table.rank_table tbody tr')

    members = []

    for e in elements:
        position = e.select('td')[0].text
        name = e.select('img')[0].attrs['alt']
        level = e.select('td')[2].text
        tmp = [name, position, level, '', '', '']
        members.append(tmp)
        #print(tmp)

    return members






