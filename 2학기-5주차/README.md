# Gmail SMTP 메일 전송 프로그램

## 프로젝트 개요
Gmail SMTP 프로토콜을 사용하여 메일을 전송하는 Python 프로그램입니다.
- 기본 메일 전송 기능
- 첨부 파일 지원 (보너스 과제)
- 예외 처리 포함
- PEP 8 스타일 가이드 준수

## 주요 기능

### 1. 기본 메일 전송
- Gmail SMTP 서버를 통한 메일 전송
- 텍스트 형식의 메일 내용
- UTF-8 인코딩 지원

### 2. 첨부 파일 메일 전송 (보너스 과제)
- 파일 첨부 기능
- 자동 MIME 타입 감지
- Base64 인코딩

### 3. 예외 처리
- SMTP 인증 오류
- 서버 연결 오류
- 파일 관련 오류
- 기타 예상치 못한 오류

## 설치 및 설정

### 1. Gmail 앱 비밀번호 설정
1. Google 계정 설정 → 보안
2. 2단계 인증 활성화
3. 앱 비밀번호 생성
4. 생성된 비밀번호를 프로그램에서 사용

### 2. 필요한 라이브러리
Python 표준 라이브러리만 사용하므로 별도 설치 불필요:
- `smtplib` (SMTP 클라이언트)
- `email` (메일 메시지 생성)
- `mimetypes` (MIME 타입 감지)
- `os` (파일 시스템 접근)

## 실행 방법

### 1. 기본 실행
```bash
python sendmail.py
```

### 2. 실행 과정
1. Gmail 계정 정보 입력
2. 받는 사람 정보 입력
3. 메일 제목 및 내용 입력
4. 자동으로 메일 전송 시도
5. 첨부 파일이 포함된 메일도 자동 전송

## 사용 예시

### 입력 예시
```
보내는 사람 Gmail 주소: your_email@gmail.com
Gmail 앱 비밀번호: your_app_password
받는 사람 이메일 주소: recipient@example.com
메일 제목: 테스트 메일
메일 내용: 안녕하세요! 테스트 메일입니다.
```

### 출력 예시
```
==================================================
Gmail SMTP 메일 전송 프로그램
==================================================

Gmail 계정 정보를 입력해주세요:
보내는 사람 Gmail 주소: your_email@gmail.com
Gmail 앱 비밀번호: ********
받는 사람 이메일 주소: recipient@example.com
메일 제목: 테스트 메일
메일 내용: 안녕하세요! 테스트 메일입니다.

1. 간단한 메일 전송 시도 중...
메일 전송 성공: recipient@example.com
간단한 메일 전송이 완료되었습니다!

2. 첨부 파일이 포함된 메일 전송 시도 중...
테스트용 첨부 파일이 생성되었습니다: test_attachment.txt
첨부 파일이 포함된 메일 전송 성공: recipient@example.com
첨부 파일: test_attachment.txt
첨부 파일이 포함된 메일 전송이 완료되었습니다!

프로그램을 종료합니다.
```

## 기술적 세부사항

### SMTP 설정
- 서버: `smtp.gmail.com`
- 포트: `587` (TLS 암호화)
- 프로토콜: SMTP with STARTTLS

### 보안 고려사항
- Gmail 앱 비밀번호 사용 권장
- 일반 비밀번호 사용 시 보안 위험
- 2단계 인증 필수

### 예외 처리
- `SMTPAuthenticationError`: 인증 실패
- `SMTPRecipientsRefused`: 잘못된 수신자
- `SMTPServerDisconnected`: 서버 연결 끊김
- `SMTPException`: 기타 SMTP 오류
- `FileNotFoundError`: 첨부 파일 없음

## 문제 해결

### 1. 인증 오류
- Gmail 앱 비밀번호 사용 확인
- 2단계 인증 활성화 확인
- 계정 정보 정확성 확인

### 2. 연결 오류
- 인터넷 연결 상태 확인
- 방화벽 설정 확인
- Gmail 서버 상태 확인

### 3. 첨부 파일 오류
- 파일 경로 정확성 확인
- 파일 권한 확인
- 파일 크기 제한 확인 (Gmail: 25MB)

## 파일 구조
```
2학기-5주차/
├── sendmail.py          # 메인 프로그램
├── README.md           # 이 파일
└── test_attachment.txt # 자동 생성되는 테스트 파일
```

## 개발 환경
- Python 3.x
- PEP 8 스타일 가이드 준수
- 표준 라이브러리만 사용
- UTF-8 인코딩
