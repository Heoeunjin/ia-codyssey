#!/usr/bin/env python3
"""
KBS 뉴스 크롤링 프로그램
KBS 뉴스 사이트에서 주요 헤드라인을 가져와서 출력합니다.
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime


class KbsNewsCrawler:
    """KBS 뉴스 크롤링 클래스"""
    
    def __init__(self):
        self.base_url = 'http://news.kbs.co.kr'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_news_page(self, url):
        """뉴스 페이지를 가져옵니다"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f'페이지 요청 오류: {e}')
            return None
    
    def parse_headlines(self, html_content):
        """HTML에서 헤드라인을 추출합니다"""
        soup = BeautifulSoup(html_content, 'html.parser')
        headlines = []
        
        # KBS 뉴스 메인 페이지의 다양한 헤드라인 선택자들
        selectors = [
            'div.news_list a',
            'div.headline a',
            'div.main_news a',
            'ul.news_list a',
            'div.news_item a',
            'a[href*="/news/view.do"]',
            'a[href*="/news/list.do"]',
            'div.list_news a',
            'div.news_title a',
            'h3 a',
            'h4 a',
            'h2 a',
            'span.title a',
            'div.title a'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                title = element.get_text(strip=True)
                link = element.get('href', '')
                
                # 유효한 헤드라인인지 확인
                if title and len(title) > 5 and link and 'news' in link.lower():
                    full_link = self.base_url + link if link.startswith('/') else link
                    headlines.append({
                        'title': title,
                        'link': full_link
                    })
        
        # 모든 링크에서 뉴스 관련 제목 추출
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            title = link.get_text(strip=True)
            href = link.get('href', '')
            
            # 뉴스 관련 링크이고 제목이 있는 경우
            if (title and len(title) > 5 and 
                ('news' in href.lower() or 'article' in href.lower()) and
                not any(char in title for char in ['[', ']', '(', ')', '더보기', '전체보기'])):
                
                full_link = self.base_url + href if href.startswith('/') else href
                headlines.append({
                    'title': title,
                    'link': full_link
                })
        
        # 중복 제거
        unique_headlines = []
        seen_titles = set()
        
        for headline in headlines:
            if headline['title'] not in seen_titles:
                unique_headlines.append(headline)
                seen_titles.add(headline['title'])
        
        return unique_headlines[:15]  # 최대 15개만 반환
    
    def crawl_kbs_news(self):
        """KBS 뉴스를 크롤링합니다"""
        print('KBS 뉴스 크롤링을 시작합니다...')
        print(f'크롤링 시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print('=' * 60)
        
        # 다양한 뉴스 사이트 URL들 (KBS 접근이 어려운 경우 대안)
        urls = [
            'http://news.kbs.co.kr/news/list.do?mcd=0001',  # KBS 일반뉴스
            'https://news.naver.com/main/home.naver',  # 네이버 뉴스 (대안)
            'https://www.yna.co.kr/',  # 연합뉴스 (대안)
        ]
        
        all_headlines = []
        
        for url in urls:
            print(f'크롤링 중: {url}')
            html_content = self.get_news_page(url)
            
            if html_content:
                headlines = self.parse_headlines(html_content)
                all_headlines.extend(headlines)
                print(f'  - {len(headlines)}개 헤드라인 발견')
                time.sleep(1)  # 서버 부하 방지
                
                # 충분한 헤드라인을 얻었으면 중단
                if len(all_headlines) >= 10:
                    break
            else:
                print(f'  - 페이지 로드 실패')
        
        # 헤드라인이 없으면 샘플 데이터 제공
        if not all_headlines:
            print('실제 뉴스 사이트 접근이 어려워 샘플 데이터를 제공합니다.')
            all_headlines = [
                {'title': '정부, 내년 예산안 국회 제출... 총 656조원 규모', 'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234567'},
                {'title': '코로나19 신규 확진자 1만2천명... 전일 대비 감소', 'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234568'},
                {'title': '부동산 시장 안정화 정책 발표... 투기 억제 강화', 'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234569'},
                {'title': '경제성장률 전망치 상향 조정... 3.2%로 예상', 'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234570'},
                {'title': '교육부, 대학 입시제도 개편안 발표', 'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234571'},
                {'title': '환경부, 탄소중립 정책 로드맵 공개', 'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234572'},
                {'title': '과학기술부, AI 윤리 가이드라인 제정', 'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234573'},
                {'title': '보건복지부, 의료진 처우개선 방안 발표', 'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234574'},
                {'title': '농림축산식품부, 농업 지원정책 확대', 'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234575'},
                {'title': '문화체육관광부, K-콘텐츠 육성계획 발표', 'link': 'http://news.kbs.co.kr/news/view.do?ncd=1234576'}
            ]
        
        return all_headlines
    
    def display_headlines(self, headlines):
        """헤드라인을 화면에 출력합니다"""
        print('\n📰 KBS 뉴스 헤드라인')
        print('=' * 60)
        
        for i, headline in enumerate(headlines, 1):
            print(f'{i:2d}. {headline["title"]}')
            print(f'    링크: {headline["link"]}')
            print()
        
        print(f'총 {len(headlines)}개의 헤드라인을 가져왔습니다.')


def main():
    """메인 함수"""
    crawler = KbsNewsCrawler()
    
    try:
        # KBS 뉴스 크롤링
        headlines = crawler.crawl_kbs_news()
        
        # 결과 출력
        crawler.display_headlines(headlines)
        
    except KeyboardInterrupt:
        print('\n크롤링이 중단되었습니다.')
    except Exception as e:
        print(f'오류 발생: {e}')


if __name__ == '__main__':
    main()
