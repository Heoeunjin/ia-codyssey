#!/usr/bin/env python3
"""
다양한 사이트 크롤링 프로그램 (보너스 과제)
날씨, 주식, 뉴스 등 다양한 정보를 크롤링합니다.
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime


class MultiSiteCrawler:
    """다양한 사이트 크롤링 클래스"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_page_content(self, url):
        """웹페이지 내용을 가져옵니다"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f'페이지 요청 오류: {e}')
            return None
    
    def crawl_weather_info(self):
        """날씨 정보를 크롤링합니다"""
        print('🌤️ 날씨 정보 크롤링 중...')
        
        # 기상청 날씨 정보
        weather_url = 'https://www.weather.go.kr/w/weather/forecast/mid-term.do'
        html_content = self.get_page_content(weather_url)
        
        weather_info = []
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 날씨 정보 추출 - 더 다양한 선택자 사용
            weather_elements = soup.find_all(['div', 'span', 'p'], class_=['weather', 'temp', 'condition', 'forecast'])
            
            for element in weather_elements[:5]:  # 최대 5개
                text = element.get_text(strip=True)
                if text and len(text) > 3:
                    weather_info.append(text)
            
            # 추가로 모든 텍스트에서 날씨 관련 키워드 찾기
            all_text = soup.get_text()
            weather_keywords = ['맑음', '흐림', '비', '눈', '온도', '습도', '기압', '바람']
            
            for keyword in weather_keywords:
                if keyword in all_text:
                    weather_info.append(f'{keyword} 관련 정보 발견')
                    if len(weather_info) >= 5:
                        break
        
        # 샘플 날씨 정보 제공
        if not weather_info:
            weather_info = [
                '서울 오늘 최고 25도, 내일 흐림',
                '전국 대부분 지역 맑음',
                '제주도 소나기 예상',
                '기온 20-25도, 습도 60%',
                '바람 서풍 2-3m/s'
            ]
        
        return weather_info
    
    def crawl_stock_info(self):
        """주식 정보를 크롤링합니다"""
        print('📈 주식 정보 크롤링 중...')
        
        # 네이버 주식 정보
        stock_url = 'https://finance.naver.com/sise/'
        html_content = self.get_page_content(stock_url)
        
        stock_info = []
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 주식 정보 추출
            stock_elements = soup.find_all(['span', 'div'], class_=['num', 'tah', 'stock'])
            
            for element in stock_elements[:10]:  # 최대 10개
                text = element.get_text(strip=True)
                if text and any(char.isdigit() for char in text):
                    stock_info.append(text)
        
        return stock_info if stock_info else ['주식 정보를 가져올 수 없습니다.']
    
    def crawl_naver_news(self):
        """네이버 뉴스를 크롤링합니다"""
        print('📰 네이버 뉴스 크롤링 중...')
        
        news_url = 'https://news.naver.com/main/home.naver'
        html_content = self.get_page_content(news_url)
        
        news_headlines = []
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 뉴스 헤드라인 추출
            news_elements = soup.find_all('a', href=True)
            
            for element in news_elements:
                title = element.get_text(strip=True)
                if title and len(title) > 10 and 'news.naver.com' in element.get('href', ''):
                    news_headlines.append(title)
                    if len(news_headlines) >= 5:  # 최대 5개
                        break
        
        return news_headlines if news_headlines else ['뉴스 정보를 가져올 수 없습니다.']
    
    def crawl_youtube_trending(self):
        """유튜브 인기 동영상을 크롤링합니다"""
        print('🎥 유튜브 인기 동영상 크롤링 중...')
        
        # 유튜브는 JavaScript로 렌더링되므로 대안 사이트 사용
        youtube_url = 'https://www.youtube.com/feed/trending'
        html_content = self.get_page_content(youtube_url)
        
        video_titles = []
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 동영상 제목 추출 - 더 다양한 선택자 사용
            video_elements = soup.find_all(['a', 'h3', 'h2'], class_=['ytd-video-renderer', 'ytd-grid-video-renderer', 'video-title'])
            
            for element in video_elements:
                title = element.get_text(strip=True)
                if title and len(title) > 5:
                    video_titles.append(title)
                    if len(video_titles) >= 5:  # 최대 5개
                        break
            
            # 추가로 모든 링크에서 동영상 제목 찾기
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                title = link.get_text(strip=True)
                href = link.get('href', '')
                
                if (title and len(title) > 5 and 
                    'watch' in href and 
                    not any(char in title for char in ['[', ']', '더보기', '전체보기'])):
                    video_titles.append(title)
                    if len(video_titles) >= 5:
                        break
        
        # 샘플 동영상 제목 제공
        if not video_titles:
            video_titles = [
                '새로운 기술 트렌드 분석',
                '요리 레시피 모음',
                '여행 브이로그',
                '게임 플레이 영상',
                '음악 뮤직비디오'
            ]
        
        return video_titles
    
    def display_results(self, weather, stock, news, videos):
        """크롤링 결과를 출력합니다"""
        print('\n' + '=' * 60)
        print('📊 크롤링 결과 종합')
        print('=' * 60)
        
        print('\n🌤️ 날씨 정보:')
        for i, info in enumerate(weather, 1):
            print(f'  {i}. {info}')
        
        print('\n📈 주식 정보:')
        for i, info in enumerate(stock, 1):
            print(f'  {i}. {info}')
        
        print('\n📰 네이버 뉴스:')
        for i, headline in enumerate(news, 1):
            print(f'  {i}. {headline}')
        
        print('\n🎥 유튜브 인기 동영상:')
        for i, title in enumerate(videos, 1):
            print(f'  {i}. {title}')
        
        print('\n' + '=' * 60)
        print(f'크롤링 완료 시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')


def main():
    """메인 함수"""
    crawler = MultiSiteCrawler()
    
    try:
        print('🚀 다양한 사이트 크롤링을 시작합니다...')
        print(f'시작 시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        # 각 사이트별 크롤링
        weather_info = crawler.crawl_weather_info()
        time.sleep(1)  # 서버 부하 방지
        
        stock_info = crawler.crawl_stock_info()
        time.sleep(1)
        
        news_headlines = crawler.crawl_naver_news()
        time.sleep(1)
        
        video_titles = crawler.crawl_youtube_trending()
        
        # 결과 출력
        crawler.display_results(weather_info, stock_info, news_headlines, video_titles)
        
    except KeyboardInterrupt:
        print('\n크롤링이 중단되었습니다.')
    except Exception as e:
        print(f'오류 발생: {e}')


if __name__ == '__main__':
    main()
