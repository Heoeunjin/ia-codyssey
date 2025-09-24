#!/usr/bin/env python3
"""
우주 해적 웹서버
HTTP 통신을 담당하는 서버로 8080 포트에서 웹페이지를 제공합니다.
"""

import http.server
import socketserver
import socket
import datetime
import os
import json
import urllib.request
import urllib.parse


class SpacePirateHandler(http.server.SimpleHTTPRequestHandler):
    """우주 해적 웹서버 핸들러 클래스"""
    
    def do_GET(self):
        """GET 요청 처리"""
        # 접속 정보 로깅
        self.log_access_info()
        
        # index.html 파일 요청 처리
        if self.path == '/' or self.path == '/index.html':
            self.serve_index_page()
        else:
            # 다른 파일 요청은 기본 처리
            super().do_GET()
    
    def serve_index_page(self):
        """index.html 페이지 제공"""
        try:
            # index.html 파일 읽기
            with open('index.html', 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            # HTTP 응답 헤더 전송 (200 OK)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(html_content.encode('utf-8'))))
            self.end_headers()
            
            # HTML 내용 전송
            self.wfile.write(html_content.encode('utf-8'))
            
        except FileNotFoundError:
            # index.html 파일이 없는 경우 404 에러
            self.send_error(404, 'File not found: index.html')
        except Exception as e:
            # 기타 오류 처리
            self.send_error(500, f'Server error: {str(e)}')
    
    def log_access_info(self):
        """접속 정보 로깅"""
        # 현재 시간
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 클라이언트 IP 주소
        client_ip = self.client_address[0]
        
        # 위치 정보 확인 (보너스 과제)
        location_info = self.get_location_info(client_ip)
        
        # 로그 출력
        print(f'[{current_time}] 접속 - IP: {client_ip}')
        if location_info:
            print(f'  위치 정보: {location_info}')
        print(f'  요청 경로: {self.path}')
        print('-' * 50)
    
    def get_location_info(self, ip_address):
        """IP 주소 기반 위치 정보 확인 (보너스 과제)"""
        try:
            # 로컬 IP 주소는 위치 정보를 가져올 수 없음
            if ip_address.startswith('127.') or ip_address.startswith('192.168.') or ip_address.startswith('10.'):
                return '로컬 네트워크'
            
            # 외부 IP 주소의 경우 위치 정보 API 사용
            url = f'http://ip-api.com/json/{ip_address}'
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if data['status'] == 'success':
                    country = data.get('country', 'Unknown')
                    region = data.get('regionName', 'Unknown')
                    city = data.get('city', 'Unknown')
                    return f'{country}, {region}, {city}'
                else:
                    return '위치 정보를 가져올 수 없음'
                    
        except Exception as e:
            return f'위치 정보 오류: {str(e)}'


def start_server():
    """웹서버 시작"""
    PORT = 8080
    
    # 서버 소켓 생성
    with socketserver.TCPServer(("", PORT), SpacePirateHandler) as httpd:
        print(f'우주 해적 웹서버가 시작되었습니다!')
        print(f'서버 주소: http://localhost:{PORT}')
        print(f'서버 주소: http://127.0.0.1:{PORT}')
        print('서버를 중지하려면 Ctrl+C를 누르세요.')
        print('=' * 50)
        
        try:
            # 서버 실행
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\n서버가 중지되었습니다.')


if __name__ == '__main__':
    start_server()

