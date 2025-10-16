#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail SMTP 메일 전송 프로그램
- SMTP 프로토콜을 사용하여 Gmail 계정으로 메일 전송
- 첨부 파일 지원 (보너스 과제)
- 예외 처리 포함
- PEP 8 스타일 가이드 준수
"""

import smtplib
import os
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr


class GmailSender:
    """Gmail SMTP 메일 전송 클래스"""
    
    def __init__(self, sender_email, sender_password):
        """
        Gmail 전송자 초기화
        
        Args:
            sender_email (str): 보내는 사람의 Gmail 주소
            sender_password (str): Gmail 앱 비밀번호
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587  # SMTP 기본 포트 번호
        
    def send_simple_email(self, recipient_email, subject, body):
        """
        간단한 텍스트 메일 전송
        
        Args:
            recipient_email (str): 받는 사람의 이메일 주소
            subject (str): 메일 제목
            body (str): 메일 내용
            
        Returns:
            bool: 전송 성공 여부
        """
        try:
            # SMTP 서버 연결
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # TLS 암호화 시작
            server.login(self.sender_email, self.sender_password)
            
            # 메일 메시지 생성
            message = MIMEText(body, 'plain', 'utf-8')
            message['From'] = formataddr(('Gmail Sender', self.sender_email))
            message['To'] = recipient_email
            message['Subject'] = subject
            
            # 메일 전송
            server.send_message(message)
            server.quit()
            
            print(f'메일 전송 성공: {recipient_email}')
            return True
            
        except smtplib.SMTPAuthenticationError:
            print('인증 오류: Gmail 계정 정보를 확인해주세요.')
            print('앱 비밀번호를 사용해야 합니다.')
            return False
            
        except smtplib.SMTPRecipientsRefused:
            print('받는 사람 이메일 주소가 잘못되었습니다.')
            return False
            
        except smtplib.SMTPServerDisconnected:
            print('SMTP 서버 연결이 끊어졌습니다.')
            return False
            
        except smtplib.SMTPException as e:
            print(f'SMTP 오류: {e}')
            return False
            
        except Exception as e:
            print(f'예상치 못한 오류: {e}')
            return False
    
    def send_email_with_attachment(self, recipient_email, subject, body, attachment_path):
        """
        첨부 파일이 포함된 메일 전송 (보너스 과제)
        
        Args:
            recipient_email (str): 받는 사람의 이메일 주소
            subject (str): 메일 제목
            body (str): 메일 내용
            attachment_path (str): 첨부 파일 경로
            
        Returns:
            bool: 전송 성공 여부
        """
        try:
            # 첨부 파일 존재 확인
            if not os.path.isfile(attachment_path):
                print(f'첨부 파일을 찾을 수 없습니다: {attachment_path}')
                return False
            
            # SMTP 서버 연결
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            
            # 멀티파트 메시지 생성
            message = MIMEMultipart()
            message['From'] = formataddr(('Gmail Sender', self.sender_email))
            message['To'] = recipient_email
            message['Subject'] = subject
            
            # 메일 본문 추가
            message.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 첨부 파일 추가
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                
            # Base64 인코딩
            encoders.encode_base64(part)
            
            # 첨부 파일 헤더 설정
            filename = os.path.basename(attachment_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            
            message.attach(part)
            
            # 메일 전송
            server.send_message(message)
            server.quit()
            
            print(f'첨부 파일이 포함된 메일 전송 성공: {recipient_email}')
            print(f'첨부 파일: {filename}')
            return True
            
        except FileNotFoundError:
            print(f'첨부 파일을 찾을 수 없습니다: {attachment_path}')
            return False
            
        except smtplib.SMTPAuthenticationError:
            print('인증 오류: Gmail 계정 정보를 확인해주세요.')
            return False
            
        except smtplib.SMTPException as e:
            print(f'SMTP 오류: {e}')
            return False
            
        except Exception as e:
            print(f'예상치 못한 오류: {e}')
            return False


def create_sample_attachment():
    """테스트용 첨부 파일 생성"""
    sample_content = '''안녕하세요!

이것은 테스트용 첨부 파일입니다.

Gmail SMTP 메일 전송 프로그램 테스트 중입니다.

감사합니다.
'''
    
    with open('test_attachment.txt', 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    print('테스트용 첨부 파일이 생성되었습니다: test_attachment.txt')


def main():
    """메인 실행 함수"""
    print('=' * 50)
    print('Gmail SMTP 메일 전송 프로그램')
    print('=' * 50)
    
    # Gmail 계정 정보 입력
    print('\nGmail 계정 정보를 입력해주세요:')
    sender_email = input('보내는 사람 Gmail 주소: ').strip()
    sender_password = input('Gmail 앱 비밀번호: ').strip()
    
    if not sender_email or not sender_password:
        print('Gmail 계정 정보를 모두 입력해주세요.')
        return
    
    # 받는 사람 정보 입력
    recipient_email = input('받는 사람 이메일 주소: ').strip()
    subject = input('메일 제목: ').strip()
    body = input('메일 내용: ').strip()
    
    if not recipient_email or not subject or not body:
        print('받는 사람, 제목, 내용을 모두 입력해주세요.')
        return
    
    # Gmail 전송자 객체 생성
    gmail_sender = GmailSender(sender_email, sender_password)
    
    # 간단한 메일 전송
    print('\n1. 간단한 메일 전송 시도 중...')
    success = gmail_sender.send_simple_email(recipient_email, subject, body)
    
    if success:
        print('간단한 메일 전송이 완료되었습니다!')
        
        # 보너스 과제: 첨부 파일이 포함된 메일 전송
        print('\n2. 첨부 파일이 포함된 메일 전송 시도 중...')
        
        # 테스트용 첨부 파일 생성
        create_sample_attachment()
        
        # 첨부 파일이 포함된 메일 전송
        attachment_subject = f'[첨부파일] {subject}'
        attachment_body = f'{body}\n\n첨부 파일이 포함된 메일입니다.'
        
        attachment_success = gmail_sender.send_email_with_attachment(
            recipient_email, attachment_subject, attachment_body, 'test_attachment.txt'
        )
        
        if attachment_success:
            print('첨부 파일이 포함된 메일 전송이 완료되었습니다!')
        else:
            print('첨부 파일 메일 전송에 실패했습니다.')
    else:
        print('메일 전송에 실패했습니다.')
    
    print('\n프로그램을 종료합니다.')


if __name__ == '__main__':
    main()
