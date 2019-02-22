"""
filename : CheckKRCERT.py
KRCERT 보안공지 게시판 첫 페이지에 있는 최신 게시물 정보를 텔레그램으로 보내기
"""
# 텔레그램으로 보낼 때 필수 정보
# Bot name: alarm4you_bot
# Bot token : 000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# Channel name : Financial_IT_Security
# Channel's chat_id : @Financial_IT_Security
# Teleg_URL = "https://api.telegram.org/봇's token/sendMessage?chat_id=@채널명&text="

from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import urllib3
import pandas as pd
import sys
import time

urllib3.disable_warnings()
http = urllib3.PoolManager()

# KRCERT 보안공지 게시판 URL
BOARD_URL = "https://www.krcert.or.kr/data/secNoticeList.do"
DOMAIN = "\nhttps://www.krcert.or.kr"

# 텔레그램 URL(@Financial_IT_Security)
Teleg_URL = "https://api.telegram.org/bot000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/sendMessage?chat_id=@Financial_IT_Security&text="

# telegram url(bot, test용)    
#Teleg_URL = "https://api.telegram.org/bot000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/sendMessage?chat_id=65875188&text="

filename = 'LatestNoKRCERT.txt'   

# 파일에서 게시물번호 가져오기(리턴값:fileNo)
# 파일이 없으면 새로 만들어서 최신 게시물번호로 저장하기
def GetTheNoFromFile(strNum):
        try:
                input_file = open(filename, 'r')
                fileNo = input_file.readline()
                input_file.close()
                return(fileNo)
        except FileNotFoundError as e:
                print(str(e))
                output_file = open(filename, 'w')
                output_file.write(strNum)   
                output_file.close()
                print("파일이 생성되었습니다.\n다시 실행시켜주세요! ^_^")
                sys.exit(1)


# 텔레그램에 제목과 URL 발송하기                        
def SendMessage( strTitle, article_URL ):
	target_URL = DOMAIN + article_URL
	strTelMsg = '{}{}{}{}'.format(Teleg_URL, urllib.parse.quote("|| KRCERT 보안공지 ||\n "), urllib.parse.quote(strTitle), urllib.parse.quote(target_URL))
	resultData = http.request('GET', strTelMsg).data 
    
# 새 번호로 파일내용 업데이트
def UpdateTheNewNo(strNewNo):
        input_file = open(filename, 'w')
        input_file.write(strNewNo)
        input_file.close()

while True:

    # 홈페이지 접속 1(BeautifulSoup)
    html = urlopen(BOARD_URL)
    bs = BeautifulSoup(html.read(), "html.parser")

    # 홈페이지 접속 2(Pandas)
    df = pd.read_html(BOARD_URL)[0]

    # 2차원 배열(box) 선언과 초기화
    box = [['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','','']]

    # 첫 페이지 게시물번호 10개를 2차원 배열(box)에 차례로 저장
    for n in range(0, 10):
        box[n][0] = df['번호'][n]
    
    # 최신 게시물번호를 별도 변수에 저장(int형)
    NoOfNewest = int(box[0][0])
    
    # 최신 게시물번호를 별도 변수에 저장(str형)
    strNumber = str(NoOfNewest)

    # 파일에서 게시물번호 가져오기(리턴값:fileNo)
    # 파일이 없으면 새로 만들어서 최신 게시물번호(strNumber)로 저장하기
    NoFromFile = int(GetTheNoFromFile(strNumber))

    # 새 번호로 파일내용 업데이트
    UpdateTheNewNo(strNumber)

    # 첫 페이지 게시판 접속해서 리스트(myList)에 저장
    myList = bs.find_all('td', {'class':'colTit'})

    # 첫 페이지 10개 게시물 정보(게시물번호, 제목, URL)를 2차원 배열(box)에 저장
    for i in range(0, 10):
        box[i][1] = myList[i].get_text().strip()   # 제목
        title_link = myList[i].select('a')
        box[i][2] = title_link[0]['href'] # URL 

    # 최신 게시물이라면 텔레그램으로 메시지 발송
    for j in range(0, 10):
        if int(box[j][0]) > NoFromFile:     # 최신 게시물인지 비교
            SendMessage(box[j][1], box[j][2])

    time.sleep(60*5)                        # 5분마다 새 게시물 확인

    
