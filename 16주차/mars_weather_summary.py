import csv 
import mysql.connector  # MySQL 관련 외부 라이브러리만 사용 가능
from datetime import datetime  

# ✅ [보너스 과제] MySQLHelper 클래스를 만들어 DB 연결과 쿼리를 쉽게 수행
class MySQLHelper:
    def __init__(self, host='localhost', user='root', password='', database='mars_db'):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def insert_weather(self, mars_date, temp, storm):
        # ✅ [요구사항] 테이블 mars_weather에 데이터 삽입하는 INSERT 쿼리 사용
        query = 'INSERT INTO mars_weather (mars_date, temp, storm) VALUES (%s, %s, %s)'
        self.cursor.execute(query, (mars_date, temp, storm))

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

# ✅ CSV 파일을 읽고 DB에 insert하는 메인 함수
def load_csv_and_insert(csv_path):
    # ✅ [주의] 여기에 본인 MySQL root 비밀번호 입력 필요
    helper = MySQLHelper(password='1234')

    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # ✅ [조건 만족] 첫 줄 header 건너뜀
        for row in reader:
            # ✅ 날짜를 datetime 객체로 변환 (str → datetime)
            mars_date = datetime.strptime(row[1], '%Y-%m-%d')
            temp = float(row[2])  # 원래는 실수형이지만 테이블에 int면 int(temp)
            storm = int(row[3])
            helper.insert_weather(mars_date, temp, storm)

    helper.commit()
    helper.close()
    print('[✅] CSV 데이터를 MySQL에 저장 완료')

# ✅ 메인 진입점에서 함수 실행
if __name__ == '__main__':
    load_csv_and_insert('mars_weathers_data.csv')
