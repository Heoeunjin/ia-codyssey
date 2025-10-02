#!/usr/bin/env python3
"""
네이버 로그인 크롤링 프로그램
Selenium을 사용하여 네이버에 로그인하고 로그인 후에만 보이는 콘텐츠를 크롤링합니다.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from datetime import datetime
import subprocess
import os
import pickle
import json
from config import NAVER_USERNAME, NAVER_PASSWORD

# webdriver-manager 설치 필요: pip install webdriver-manager
try:
    from webdriver_manager.chrome import ChromeDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False


class NaverLoginCrawler:
    """네이버 로그인 크롤링 클래스"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.login_content = []
        self.cookies_file = 'naver_cookies.pkl'
    
    def setup_driver(self):
        """Chrome 드라이버 설정"""
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 브라우저 창을 띄우지 않음 (첫 로그인 시 주석 처리)
        # 첫 로그인 시에는 브라우저 창을 보이게 해서 수동 로그인
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        
        try:
            # webdriver-manager 사용 (권장)
            if WEBDRIVER_MANAGER_AVAILABLE:
                print('webdriver-manager를 사용하여 Chrome 드라이버를 자동으로 관리합니다...')
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                # 수동으로 chromedriver 경로 찾기
                chromedriver_path = self.find_chromedriver()
                
                if chromedriver_path:
                    print(f'Chrome 드라이버를 찾았습니다: {chromedriver_path}')
                    service = Service(chromedriver_path)
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                else:
                    print('Chrome 드라이버를 찾을 수 없습니다. 시스템 PATH에서 시도합니다...')
                    self.driver = webdriver.Chrome(options=chrome_options)
            
            self.wait = WebDriverWait(self.driver, 10)
            return True
        except Exception as e:
            print(f'드라이버 설정 오류: {e}')
            print('해결 방법:')
            print('1. pip install webdriver-manager')
            print('2. 또는 brew install chromedriver')
            print('3. 또는 시스템 환경설정에서 chromedriver 허용')
            return False
    
    def find_chromedriver(self):
        """Chrome 드라이버 경로 찾기"""
        possible_paths = [
            '/usr/local/bin/chromedriver',
            '/opt/homebrew/bin/chromedriver',
            '/usr/bin/chromedriver',
            './chromedriver'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def save_cookies(self):
        """현재 세션의 쿠키를 파일에 저장"""
        try:
            cookies = self.driver.get_cookies()
            with open(self.cookies_file, 'wb') as f:
                pickle.dump(cookies, f)
            print('로그인 쿠키가 저장되었습니다.')
            return True
        except Exception as e:
            print(f'쿠키 저장 오류: {e}')
            return False
    
    def load_cookies(self):
        """저장된 쿠키를 로드하여 로그인 상태 복원"""
        try:
            if os.path.exists(self.cookies_file):
                with open(self.cookies_file, 'rb') as f:
                    cookies = pickle.load(f)
                
                # 네이버 메인 페이지로 이동
                self.driver.get('https://www.naver.com')
                time.sleep(2)
                
                # 쿠키 추가
                for cookie in cookies:
                    try:
                        self.driver.add_cookie(cookie)
                    except Exception as e:
                        continue
                
                # 페이지 새로고침하여 로그인 상태 확인
                self.driver.refresh()
                time.sleep(3)
                
                # 로그인 상태 확인
                if self.check_login_status():
                    print('저장된 쿠키로 로그인 상태가 복원되었습니다.')
                    return True
                else:
                    print('저장된 쿠키가 만료되었습니다.')
                    return False
            else:
                print('저장된 쿠키가 없습니다.')
                return False
        except Exception as e:
            print(f'쿠키 로드 오류: {e}')
            return False
    
    def navigate_to_naver(self):
        """네이버 메인 페이지로 이동"""
        try:
            self.driver.get('https://www.naver.com')
            print('네이버 메인 페이지 접속 완료')
            return True
        except Exception as e:
            print(f'네이버 접속 오류: {e}')
            return False
    
    def check_login_status(self):
        """로그인 상태 확인"""
        try:
            # 현재 페이지 URL 확인
            current_url = self.driver.current_url
            print(f'현재 페이지 URL: {current_url}')
            
            # 로그인된 상태를 확인하는 다양한 방법들
            login_indicators = [
                # 사용자 정보 관련
                '.MyView-module__link_login___HpHMW',
                '.MyView-module__my_area___iYtgU',
                '.gnb_my',
                '.area_links',
                # 로그아웃 버튼
                'a[href*="logout"]',
                'a[href*="nid.naver.com/user2/help/myInfo"]',
                # 프로필 관련
                '.profile_thumb',
                '.user_info',
                # 메일 관련
                'a[href*="mail.naver.com"]',
                '.mail_area'
            ]
            
            for selector in login_indicators:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f'로그인된 상태를 확인했습니다: {selector}')
                    return True
                except NoSuchElementException:
                    continue
            
            # 로그인 버튼이 있으면 로그인되지 않은 상태
            login_button_selectors = [
                'a[href*="nid.naver.com"]',
                '.link_login',
                '.btn_login',
                'a[href*="login"]'
            ]
            
            for selector in login_button_selectors:
                try:
                    login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f'로그인 버튼이 발견되었습니다 ({selector}). 로그인되지 않은 상태입니다.')
                    return False
                except NoSuchElementException:
                    continue
            
            # 페이지 제목으로 확인
            page_title = self.driver.title
            print(f'페이지 제목: {page_title}')
            
            if '네이버' in page_title and '로그인' not in page_title:
                print('페이지 제목으로 로그인된 상태로 판단합니다.')
                return True
            
            print('로그인 상태를 확인할 수 없습니다.')
            return False
            
        except Exception as e:
            print(f'로그인 상태 확인 오류: {e}')
            return False
    
    def get_public_content(self):
        """로그인 전 공개 콘텐츠 수집"""
        print('로그인 전 공개 콘텐츠 수집 중...')
        
        public_content = []
        
        try:
            # 페이지 로드 대기
            time.sleep(3)
            
            # 실시간 검색어 찾기
            search_selectors = [
                '.ah_k',
                '.ah_item .ah_k',
                '.ah_list .ah_k',
                '.search_keyword'
            ]
            
            for selector in search_selectors:
                search_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in search_elements[:5]:  # 최대 5개
                    keyword = element.text.strip()
                    if keyword and len(keyword) > 1:
                        public_content.append(f'실시간 검색어: {keyword}')
                        if len(public_content) >= 5:
                            break
                if len(public_content) >= 5:
                    break
            
            # 메인 페이지의 기본 정보
            public_content.append('네이버 메인 페이지 접속 완료')
                        
        except Exception as e:
            print(f'공개 콘텐츠 수집 오류: {e}')
        
        # 실제 크롤링이 실패한 경우
        if not public_content:
            print('실제 콘텐츠를 가져올 수 없습니다.')
        
        return public_content
    
    def manual_login(self):
        """수동 로그인 (사용자가 직접 로그인)"""
        print('수동 로그인을 진행합니다...')
        print('브라우저에서 직접 로그인해주세요.')
        
        try:
            # 직접 로그인 페이지로 이동
            self.driver.get('https://nid.naver.com/nidlogin.login')
            print('로그인 페이지로 이동했습니다.')
            print('브라우저에서 아이디와 비밀번호를 입력하고 로그인해주세요.')
            print('reCAPTCHA나 2단계 인증이 있다면 처리해주세요.')
            
            # 사용자가 수동으로 로그인할 때까지 대기
            input('로그인 완료 후 Enter를 눌러주세요...')
            
            # 네이버 메인 페이지로 돌아가기
            self.driver.get('https://www.naver.com')
            time.sleep(3)
            
            # 로그인 상태 확인
            print('로그인 상태를 확인합니다...')
            if self.check_login_status():
                print('로그인 성공!')
                # 로그인 성공 시 쿠키 저장
                self.save_cookies()
                return True
            else:
                print('로그인 실패')
                return False
                
        except Exception as e:
            print(f'수동 로그인 오류: {e}')
            return False
    
    def get_private_content(self):
        """로그인 후 개인 콘텐츠 수집 (메일 제목)"""
        print('로그인 후 개인 콘텐츠 수집 중...')
        
        private_content = []
        
        try:
            # 네이버 메일 페이지로 이동
            print('네이버 메일 페이지로 이동 중...')
            self.driver.get('https://mail.naver.com')
            time.sleep(5)  # 페이지 로딩 대기 시간 증가
            
            # 현재 페이지 URL 확인
            current_url = self.driver.current_url
            print(f'메일 페이지 URL: {current_url}')
            
            # 페이지 제목 확인
            page_title = self.driver.title
            print(f'메일 페이지 제목: {page_title}')
            
            # 메일 리스트에서 제목 추출 - 다양한 선택자 시도
            mail_selectors = [
                # 실제 네이버 메일 페이지에서 작동하는 선택자들
                '.mail_list .mail_title',
                '.mail_list a',
                '.mail_list a[href*="read"]',
                # 메일 제목이 있는 링크들
                'a[href*="mail.naver.com/v2/read"]',
                'a[href*="/read/"]',
                # 메일 리스트의 각 행에서 제목 찾기
                '.mail_list tr a',
                '.mail_list .mail_item a',
                '.mail_list .subject',
                # 테이블 형태의 메일 리스트
                'table.mail_list tr td a',
                'table.mail_list a[href*="read"]',
                # 기타 가능한 선택자들
                '.list_mail .subject',
                '.mail_item .subject',
                'tr[onclick] .subject',
                '.mail_list tr .subject',
                '.mail_list tr td:nth-child(2)',
                '.mail_list tr td:nth-child(3)',
                '.mail_list .mail_subject',
                '.mail_list .title',
                'table tr td a',
                '.mail_list table tr td',
                'a[href*="mail.naver.com"]',
                'tr[onclick*="read"] td'
            ]
            
            mail_titles = []
            for selector in mail_selectors:
                try:
                    mail_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in mail_elements[:3]:  # 최대 3개
                        title = element.text.strip()
                        if title and len(title) > 2 and '메일' not in title and '더보기' not in title:
                            mail_titles.append(f'메일: {title}')
                            if len(mail_titles) >= 3:
                                break
                    if mail_titles:
                        break
                except Exception as e:
                    continue
            
            # 메일 제목을 찾지 못한 경우 다른 방법 시도
            if not mail_titles:
                print('기본 선택자로 메일을 찾지 못했습니다. 대체 방법 시도 중...')
                try:
                    # 모든 링크에서 메일 관련 제목 찾기
                    all_links = self.driver.find_elements(By.TAG_NAME, 'a')
                    for link in all_links[:30]:  # 더 많은 링크 확인
                        href = link.get_attribute('href') or ''
                        title = link.text.strip()
                        # 메일 읽기 링크이면서 제목이 있는 경우
                        if ('/read/' in href or 'mail.naver.com/v2/read' in href) and title and len(title) > 2:
                            # 불필요한 텍스트 제거
                            if not any(word in title for word in ['더보기', '전체보기', '메뉴', '설정', '삭제', '이동']):
                                mail_titles.append(f'메일: {title}')
                                if len(mail_titles) >= 3:
                                    break
                except Exception as e:
                    print(f'링크 기반 메일 검색 오류: {e}')
                
                # 여전히 메일을 찾지 못한 경우 메일 리스트 구조 분석
                if not mail_titles:
                    print('메일 리스트 구조를 분석합니다...')
                    try:
                        # 메일 리스트 컨테이너 찾기
                        mail_containers = self.driver.find_elements(By.CSS_SELECTOR, '.mail_list, .list_mail, table')
                        for container in mail_containers:
                            # 컨테이너 내의 모든 링크 확인
                            links = container.find_elements(By.TAG_NAME, 'a')
                            for link in links[:10]:
                                href = link.get_attribute('href') or ''
                                title = link.text.strip()
                                if title and len(title) > 2 and ('read' in href or 'mail' in href):
                                    if not any(word in title for word in ['더보기', '전체보기', '메뉴', '설정', '삭제', '이동']):
                                        mail_titles.append(f'메일: {title}')
                                        if len(mail_titles) >= 3:
                                            break
                            if mail_titles:
                                break
                    except Exception as e:
                        print(f'메일 리스트 구조 분석 오류: {e}')
            
            # 여전히 메일을 찾지 못한 경우 로그인 상태 확인
            if not mail_titles:
                print('메일 제목을 찾을 수 없습니다. 로그인 상태를 다시 확인합니다...')
                # 메일 페이지에서 로그인 상태 확인
                try:
                    login_indicators = [
                        'a[href*="nid.naver.com"]',
                        '.login_area',
                        '.btn_login'
                    ]
                    
                    for indicator in login_indicators:
                        try:
                            element = self.driver.find_element(By.CSS_SELECTOR, indicator)
                            print(f'로그인 필요 요소 발견: {indicator}')
                            private_content.append('메일 접근을 위해 로그인이 필요합니다.')
                            break
                        except NoSuchElementException:
                            continue
                    else:
                        private_content.append('메일 페이지에 접근했지만 메일 목록을 찾을 수 없습니다.')
                except Exception as e:
                    print(f'로그인 상태 확인 오류: {e}')
                    private_content.append('메일 페이지 접근 중 오류가 발생했습니다.')
            else:
                private_content = mail_titles
            
        except Exception as e:
            print(f'개인 콘텐츠 수집 오류: {e}')
            private_content.append('메일 페이지 접근 중 오류가 발생했습니다.')
        
        # 실제 크롤링이 실패한 경우
        if not private_content:
            print('실제 개인 콘텐츠를 가져올 수 없습니다.')
        
        return private_content
    
    def crawl_naver_content(self, username=None, password=None):
        """네이버 로그인 크롤링 메인 함수"""
        print('네이버 로그인 크롤링을 시작합니다...')
        print(f'크롤링 시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print('=' * 60)
        
        # 드라이버 설정
        if not self.setup_driver():
            return []
        
        try:
            # 네이버 접속
            if not self.navigate_to_naver():
                return []
            
            # 먼저 저장된 쿠키로 로그인 시도
            login_success = self.load_cookies()
            
            # 쿠키 로그인이 실패한 경우 수동 로그인 시도
            if not login_success:
                print('쿠키 로그인 실패, 수동 로그인을 시도합니다...')
                login_success = self.manual_login()
            
            # 로그인 전 공개 콘텐츠 수집
            public_content = self.get_public_content()
            
            # 로그인 성공 시 개인 콘텐츠 수집 (메일 제목)
            if login_success:
                print('로그인 상태로 개인 콘텐츠를 수집합니다...')
                private_content = self.get_private_content()
                all_content = public_content + private_content
            else:
                print('로그인되지 않아 공개 콘텐츠만 수집')
                all_content = public_content
            
            return all_content
            
        except Exception as e:
            print(f'크롤링 오류: {e}')
            return []
        
        finally:
            if self.driver:
                self.driver.quit()
    
    
    def display_content(self, content_list):
        """수집된 콘텐츠 출력"""
        print('\n📧 네이버 로그인 크롤링 결과')
        print('=' * 60)
        
        for i, content in enumerate(content_list, 1):
            print(f'{i:2d}. {content}')
        
        print(f'\n총 {len(content_list)}개의 콘텐츠를 수집했습니다.')


def main():
    """메인 함수"""
    crawler = NaverLoginCrawler()
    
    try:
        # 쿠키 파일이 있으면 자동 로그인, 없으면 수동 로그인
        if os.path.exists('naver_cookies.pkl'):
            print('저장된 쿠키가 있습니다. 자동 로그인을 시도합니다...')
            content_list = crawler.crawl_naver_content()
        else:
            print('저장된 쿠키가 없습니다. 수동 로그인을 진행합니다...')
            content_list = crawler.crawl_naver_content()
        
        # 결과 출력
        crawler.display_content(content_list)
        
    except KeyboardInterrupt:
        print('\n크롤링이 중단되었습니다.')
    except Exception as e:
        print(f'오류 발생: {e}')


if __name__ == '__main__':
    main()
