import random
from datetime import datetime

class DummySensor:
   # DummySensor 클래스는 화성 기지의 환경 센서 데이터를 임의로 생성하여 저장하는 클래스
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None,
        }

    def set_env(self):
        #각 센서 값을 지정된 범위 내에서 랜덤으로 생성하여 env_values에 저장
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        
        #현재의 센서 데이터 반환
        #보너스 과제로, 현재 날짜와 시간 및 각 센서 값을 개별 줄에 출력하고,
        #'sensor_log.txt' 파일에 로그로 남기기
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 각 센서 항목을 "키: 값" 형식으로 변환하여 개별 줄로 만듬
        sensor_lines = [f'{key}: {value}' for key, value in self.env_values.items()]
        output = f'{now}\n' + "\n".join(sensor_lines)
        print(output)
        
        # 로그 파일에 출력 내용 추가
        try:
            with open('sensor_log.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(output + "\n")
        except Exception as e:
            print('로그 파일 저장 중 오류:', e)
            
        return self.env_values

# DummySensor 클래스 인스턴스를 생성
ds = DummySensor()

# 센서 데이터를 임의로 생성
ds.set_env()

# 생성된 센서 데이터를 개별 줄에 출력하고, 로그 파일에 기록
ds.get_env()
