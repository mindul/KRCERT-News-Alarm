# KRCERT-News-Alarm

    KRCERT 보안공지 게시판 첫 페이지에 있는 첫 번째 게시물(최신) 정보를 가져와 텔레그램으로 보내기
    filename : CheckKRCERT.py
    개발언어 : Python 3
    버전 :  1.1
    작성일 : 2018. 6. 27.
    주안점 : 
    - Pandas 사용
    - Pandas로 긁어온 웹페이지에서 제목 추출

    텔레그램으로 보낼 때 필수 정보
    Bot name: alarm4you_bot
    Bot token : 000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    Channel name : Financial_IT_Security
    Channel's chat_id : @Financial_IT_Security
    Teleg_URL = "https://api.telegram.org/봇's token/sendMessage?chat_id=@채널명&text="


참고문서
* 텔레그램으로 웹사이트 새 글 발행 알림 보내기(봇과 채널 이용) : 
https://mytory.net/2016/10/18/how-to-send-telegram-message-automatically.html

* Telegram Bot API : 
https://core.telegram.org/bots/api#sendmessage
