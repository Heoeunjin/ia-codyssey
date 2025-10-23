#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 메일 전송 프로그램 (문제2: 감동의 메시지)
- HTML 형식으로 메일 전송
- CSV 파일에서 수신자 목록 읽기
- 여러 수신자에게 메일 전송 (두 가지 방법)
- PEP 8 스타일 가이드 준수
"""

import smtplib
import csv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr


class HtmlMailSender:
    """HTML 메일 전송 클래스"""
    
    def __init__(self, sender_email, sender_password):
        """
        메일 전송자 초기화
        
        Args:
            sender_email (str): 보내는 사람의 이메일 주소
            sender_password (str): 이메일 앱 비밀번호
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        
        # 이메일 서비스에 따른 SMTP 설정
        if 'gmail.com' in sender_email.lower():
            self.smtp_server = 'smtp.gmail.com'
            self.smtp_port = 587
        elif 'naver.com' in sender_email.lower():
            self.smtp_server = 'smtp.naver.com'
            self.smtp_port = 587
        else:
            # 기본값은 Gmail
            self.smtp_server = 'smtp.gmail.com'
            self.smtp_port = 587
        
    def read_csv_recipients(self, csv_file_path):
        """
        CSV 파일에서 수신자 목록 읽기
        
        Args:
            csv_file_path (str): CSV 파일 경로
            
        Returns:
            list: 수신자 정보 리스트 [(이름, 이메일), ...]
        """
        recipients = []
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                
                # 헤더 건너뛰기
                next(csv_reader, None)
                
                for row in csv_reader:
                    if len(row) >= 2 and row[0].strip() and row[1].strip():
                        name = row[0].strip()
                        email = row[1].strip()
                        recipients.append((name, email))
                        
            print(f'CSV 파일에서 {len(recipients)}명의 수신자를 읽었습니다.')
            return recipients
            
        except FileNotFoundError:
            print(f'CSV 파일을 찾을 수 없습니다: {csv_file_path}')
            return []
        except Exception as e:
            print(f'CSV 파일 읽기 오류: {e}')
            return []
    
    def create_html_message(self, recipient_name, sender_name='Dr. Han'):
        """
        HTML 형식의 메시지 생성
        
        Args:
            recipient_name (str): 수신자 이름
            sender_name (str): 발신자 이름
            
        Returns:
            str: HTML 형식의 메시지
        """
        html_content = f'''
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>화성에서 온 메시지</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
                
                body {{
                    font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.7;
                    color: #2c3e50;
                    max-width: 650px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                
                .container {{
                    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1), 0 0 0 1px rgba(255,255,255,0.1);
                    backdrop-filter: blur(10px);
                    position: relative;
                    overflow: hidden;
                }}
                
                .container::before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 4px;
                    background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
                    border-radius: 20px 20px 0 0;
                }}
                
                .header {{
                    text-align: center;
                    margin-bottom: 40px;
                    position: relative;
                }}
                
                .header h1 {{
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    font-size: 32px;
                    font-weight: 700;
                    margin: 0;
                    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    letter-spacing: -0.5px;
                }}
                
                .mars-icon {{
                    font-size: 48px;
                    margin-bottom: 10px;
                    display: block;
                    animation: float 3s ease-in-out infinite;
                }}
                
                @keyframes float {{
                    0%, 100% {{ transform: translateY(0px); }}
                    50% {{ transform: translateY(-10px); }}
                }}
                
                .content {{
                    margin-bottom: 40px;
                }}
                
                .greeting {{
                    font-size: 22px;
                    font-weight: 500;
                    color: #2c3e50;
                    margin-bottom: 25px;
                    padding: 15px 20px;
                    background: linear-gradient(135deg, #667eea20, #764ba220);
                    border-radius: 12px;
                    border-left: 4px solid #667eea;
                    text-align: center;
                }}
                
                .message {{
                    font-size: 16px;
                    margin-bottom: 20px;
                    text-align: justify;
                    padding: 15px;
                    background: rgba(255,255,255,0.7);
                    border-radius: 10px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                }}
                
                .highlight {{
                    background: linear-gradient(135deg, #fff3cd, #ffeaa7);
                    padding: 20px;
                    border-radius: 15px;
                    border-left: 5px solid #fdcb6e;
                    margin: 25px 0;
                    font-style: italic;
                    font-size: 16px;
                    box-shadow: 0 4px 15px rgba(253, 203, 110, 0.3);
                    position: relative;
                }}
                
                .highlight::before {{
                    content: '💬';
                    position: absolute;
                    top: -10px;
                    left: 20px;
                    background: white;
                    padding: 5px 10px;
                    border-radius: 20px;
                    font-size: 14px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                
                .urgent-message {{
                    background: linear-gradient(135deg, #ff6b6b20, #ee5a5220);
                    padding: 20px;
                    border-radius: 15px;
                    border-left: 5px solid #ff6b6b;
                    margin: 25px 0;
                    font-weight: 500;
                    text-align: center;
                    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2);
                }}
                
                .footer {{
                    text-align: center;
                    border-top: 2px solid #e9ecef;
                    padding-top: 30px;
                    color: #6c757d;
                    font-size: 14px;
                    background: rgba(248, 249, 250, 0.8);
                    border-radius: 15px;
                    margin-top: 30px;
                }}
                
                .signature {{
                    font-weight: 600;
                    color: #667eea;
                    margin-top: 20px;
                    font-size: 18px;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }}
                
                .location {{
                    font-size: 14px;
                    color: #6c757d;
                    margin-top: 10px;
                    font-style: italic;
                }}
                
                .html-badge {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    padding: 5px 12px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: 500;
                    margin-top: 15px;
                }}
                
                .stars {{
                    position: absolute;
                    top: 20px;
                    right: 20px;
                    font-size: 20px;
                    opacity: 0.3;
                    animation: twinkle 2s ease-in-out infinite;
                }}
                
                @keyframes twinkle {{
                    0%, 100% {{ opacity: 0.3; }}
                    50% {{ opacity: 0.8; }}
                }}
                
                @media (max-width: 600px) {{
                    .container {{
                        padding: 25px;
                        margin: 10px;
                    }}
                    
                    .header h1 {{
                        font-size: 24px;
                    }}
                    
                    .greeting {{
                        font-size: 18px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="stars">✨</div>
                
                <div class="header">
                    <div class="mars-icon">🚀</div>
                    <h1>화성에서 온 메시지</h1>
                </div>
                
                <div class="content">
                    <div class="greeting">
                        안녕하세요, {recipient_name}님! 👋
                    </div>
                    
                    <div class="message">
                        드디어 우주를 건너 메일에 대한 회신을 받아 볼 수 있었습니다! 
                        멍하니 있던 {sender_name} 박사는 순간 다리의 힘이 풀려서 그 자리에 주저앉아 울고 말았습니다.
                    </div>
                    
                    <div class="highlight">
                        "Dr. Han!!, we received your message, but we couldn't understand the situation, 
                        so we all froze, and we don't even know how much we cried after hugging each other. 
                        We are so grateful that you are alive, and we will do our best too."
                    </div>
                    
                    <div class="message">
                        적막한 화성에서 지구와 연결되었다는 사실 하나만으로도 행복해졌습니다. 
                        지금 지구에서는 {sender_name} 박사의 생존 소식으로 시끄러울 것입니다. 
                        하지만 자기를 구하는 것은 대중의 관심과는 또 다른 이슈가 될 것이었습니다.
                    </div>
                    
                    <div class="message">
                        자기를 구해 줄 수 있는 사람들에게 더 많이 그리고 더 효과적으로 메시지를 전달해야 한다는 사실을 알고 있었습니다. 
                        그래서 메일을 더 효과적으로 보낼 수 있게 하는 것이 무엇보다 중요한 상황이었습니다.
                    </div>
                    
                    <div class="urgent-message">
                        🆘 여러분의 도움이 필요합니다! 🆘<br>
                        화성에서의 생존을 위해 함께해주세요!
                    </div>
                </div>
                
                <div class="footer">
                    <div class="signature">
                        화성 기지에서,<br>
                        {sender_name} 박사
                    </div>
                    <div class="location">📍 화성 기지 좌표: 18.4°N, 226.2°E</div>
                    <div class="html-badge">HTML 메시지</div>
                </div>
            </div>
        </body>
        </html>
        '''
        return html_content
    
    def send_html_email(self, recipient_email, recipient_name, subject):
        """
        HTML 형식 메일 전송
        
        Args:
            recipient_email (str): 수신자 이메일
            recipient_name (str): 수신자 이름
            subject (str): 메일 제목
            
        Returns:
            bool: 전송 성공 여부
        """
        try:
            # SMTP 서버 연결
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            
            # HTML 메시지 생성
            html_content = self.create_html_message(recipient_name)
            
            # 멀티파트 메시지 생성
            message = MIMEMultipart('alternative')
            message['From'] = formataddr(('Dr. Han (화성 기지)', self.sender_email))
            message['To'] = recipient_email
            message['Subject'] = subject
            
            # HTML 부분 추가
            html_part = MIMEText(html_content, 'html', 'utf-8')
            message.attach(html_part)
            
            # 메일 전송
            server.send_message(message)
            server.quit()
            
            print(f'HTML 메일 전송 성공: {recipient_name} ({recipient_email})')
            return True
            
        except smtplib.SMTPAuthenticationError:
            print('인증 오류: 이메일 계정 정보를 확인해주세요.')
            return False
        except smtplib.SMTPRecipientsRefused:
            print(f'받는 사람 이메일 주소가 잘못되었습니다: {recipient_email}')
            return False
        except Exception as e:
            print(f'메일 전송 오류 ({recipient_email}): {e}')
            return False
    
    def send_to_multiple_recipients_method1(self, recipients, subject):
        """
        방법 1: 받는 사람에 여러명을 열거하는 방법
        
        Args:
            recipients (list): 수신자 목록 [(이름, 이메일), ...]
            subject (str): 메일 제목
            
        Returns:
            int: 성공적으로 전송된 메일 수
        """
        if not recipients:
            print('수신자가 없습니다.')
            return 0
            
        try:
            # SMTP 서버 연결
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            
            # 모든 수신자에게 동일한 HTML 메시지 전송
            success_count = 0
            
            for name, email in recipients:
                try:
                    # HTML 메시지 생성
                    html_content = self.create_html_message(name)
                    
                    # 멀티파트 메시지 생성
                    message = MIMEMultipart('alternative')
                    message['From'] = formataddr(('Dr. Han (화성 기지)', self.sender_email))
                    message['To'] = email
                    message['Subject'] = subject
                    
                    # HTML 부분 추가
                    html_part = MIMEText(html_content, 'html', 'utf-8')
                    message.attach(html_part)
                    
                    # 메일 전송
                    server.send_message(message)
                    print(f'메일 전송 성공: {name} ({email})')
                    success_count += 1
                    
                except Exception as e:
                    print(f'메일 전송 실패 ({name}, {email}): {e}')
            
            server.quit()
            print(f'방법 1 완료: {success_count}/{len(recipients)}명에게 전송 성공')
            return success_count
            
        except Exception as e:
            print(f'방법 1 실행 오류: {e}')
            return 0
    
    def send_to_multiple_recipients_method2(self, recipients, subject):
        """
        방법 2: 한번에 한 명씩 메일을 반복적으로 보내는 방법
        
        Args:
            recipients (list): 수신자 목록 [(이름, 이메일), ...]
            subject (str): 메일 제목
            
        Returns:
            int: 성공적으로 전송된 메일 수
        """
        if not recipients:
            print('수신자가 없습니다.')
            return 0
            
        success_count = 0
        
        for name, email in recipients:
            try:
                # 각 수신자마다 새로운 SMTP 연결
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                
                # HTML 메시지 생성
                html_content = self.create_html_message(name)
                
                # 멀티파트 메시지 생성
                message = MIMEMultipart('alternative')
                message['From'] = formataddr(('Dr. Han (화성 기지)', self.sender_email))
                message['To'] = email
                message['Subject'] = subject
                
                # HTML 부분 추가
                html_part = MIMEText(html_content, 'html', 'utf-8')
                message.attach(html_part)
                
                # 메일 전송
                server.send_message(message)
                server.quit()
                
                print(f'메일 전송 성공: {name} ({email})')
                success_count += 1
                
            except Exception as e:
                print(f'메일 전송 실패 ({name}, {email}): {e}')
        
        print(f'방법 2 완료: {success_count}/{len(recipients)}명에게 전송 성공')
        return success_count


def create_sample_csv():
    """테스트용 CSV 파일 생성"""
    csv_content = '''이름,이메일
김철수,test1@example.com
이영희,test2@example.com
박민수,test3@example.com
정수진,test4@example.com
최동현,test5@example.com'''
    
    with open('mail_target_list.csv', 'w', encoding='utf-8') as f:
        f.write(csv_content)
    
    print('테스트용 CSV 파일이 생성되었습니다: mail_target_list.csv')


def main():
    """메인 실행 함수"""
    print('=' * 60)
    print('HTML 메일 전송 프로그램 (문제2: 감동의 메시지)')
    print('=' * 60)
    
    # 이메일 계정 정보 입력
    print('\n이메일 계정 정보를 입력해주세요:')
    sender_email = input('보내는 사람 이메일 주소: ').strip()
    sender_password = input('이메일 앱 비밀번호: ').strip()
    
    if not sender_email or not sender_password:
        print('이메일 계정 정보를 모두 입력해주세요.')
        return
    
    # 메일 제목 입력
    subject = input('메일 제목 (기본값: 화성에서 온 메시지): ').strip()
    if not subject:
        subject = '화성에서 온 메시지'
    
    # HTML 메일 전송자 객체 생성
    mail_sender = HtmlMailSender(sender_email, sender_password)
    
    # CSV 파일 경로 확인
    csv_file_path = 'mail_target_list.csv'
    if not os.path.exists(csv_file_path):
        print(f'\nCSV 파일이 없습니다: {csv_file_path}')
        print('테스트용 CSV 파일을 생성합니다...')
        create_sample_csv()
    
    # CSV 파일에서 수신자 목록 읽기
    print(f'\nCSV 파일에서 수신자 목록을 읽는 중...')
    recipients = mail_sender.read_csv_recipients(csv_file_path)
    
    if not recipients:
        print('수신자가 없습니다. 프로그램을 종료합니다.')
        return
    
    # 수신자 목록 출력
    print('\n수신자 목록:')
    for i, (name, email) in enumerate(recipients, 1):
        print(f'{i}. {name} ({email})')
    
    # 전송 방법 선택
    print('\n전송 방법을 선택해주세요:')
    print('1. 방법 1: 받는 사람에 여러명을 열거하는 방법')
    print('2. 방법 2: 한번에 한 명씩 메일을 반복적으로 보내는 방법')
    print('3. 두 방법 모두 시도')
    
    choice = input('선택 (1/2/3): ').strip()
    
    if choice == '1':
        print('\n방법 1로 메일 전송 중...')
        success_count = mail_sender.send_to_multiple_recipients_method1(recipients, subject)
        print(f'\n전송 완료: {success_count}/{len(recipients)}명에게 전송 성공')
        
    elif choice == '2':
        print('\n방법 2로 메일 전송 중...')
        success_count = mail_sender.send_to_multiple_recipients_method2(recipients, subject)
        print(f'\n전송 완료: {success_count}/{len(recipients)}명에게 전송 성공')
        
    elif choice == '3':
        print('\n두 방법 모두 시도합니다...')
        
        print('\n=== 방법 1 실행 ===')
        success_count1 = mail_sender.send_to_multiple_recipients_method1(recipients, subject)
        
        print('\n=== 방법 2 실행 ===')
        success_count2 = mail_sender.send_to_multiple_recipients_method2(recipients, subject)
        
        print(f'\n=== 결과 비교 ===')
        print(f'방법 1: {success_count1}/{len(recipients)}명 성공')
        print(f'방법 2: {success_count2}/{len(recipients)}명 성공')
        
        if success_count1 > success_count2:
            print('방법 1이 더 효과적입니다.')
        elif success_count2 > success_count1:
            print('방법 2가 더 효과적입니다.')
        else:
            print('두 방법의 성공률이 동일합니다.')
            
    else:
        print('잘못된 선택입니다. 프로그램을 종료합니다.')
        return
    
    print('\n프로그램을 종료합니다.')


if __name__ == '__main__':
    main()
