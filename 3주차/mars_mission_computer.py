import random
from datetime import datetime

class DummySensor:
    """
    DummySensor 클래스는 화성 기지의 환경 센서 데이터를 임의로 생성하여 저장하는 클래스입니다.
    
    멤버 변수:
        env_values (dict): 센서 데이터가 저장된 사전. 포함되는 항목은 다음과 같습니다.
            - mars_base_internal_temperature
            - mars_base_external_temperature
            - mars_base_internal_humidity
            - mars_base_external_illuminance
            - mars_base_internal_co2
            - mars_base_internal_oxygen
    """

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
        """
        각 센서 값을 지정된 범위 내에서 랜덤으로 생성하여 env_values에 저장합니다.
        - 내부 온도: 18 ~ 30도
        - 외부 온도: 0 ~ 21도
        - 내부 습도: 50 ~ 60%
        - 외부 광량: 500 ~ 715 W/m²
        - 내부 CO2: 0.02 ~ 0.1%
        - 내부 산소: 4 ~ 7%
        """
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        """
        현재의 센서 데이터를 반환합니다.
        보너스 과제로, 현재 날짜와 시간 및 각 센서 값을 개별 줄에 출력하고,
        'sensor_log.txt' 파일에 로그로 남깁니다.
        """
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 각 센서 항목을 "키: 값" 형식으로 변환하여 개별 줄로 만듭니다.
        sensor_lines = [f'{key}: {value}' for key, value in self.env_values.items()]
        output = f'{now}\n' + "\n".join(sensor_lines)
        print(output)
        
        # 로그 파일에 출력 내용을 추가합니다.
        try:
            with open('sensor_log.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(output + "\n")
        except Exception as e:
            print('로그 파일 저장 중 오류:', e)
            
        return self.env_values

# DummySensor 클래스 인스턴스를 생성합니다.
ds = DummySensor()

# 센서 데이터를 임의로 생성합니다.
ds.set_env()

# 생성된 센서 데이터를 개별 줄에 출력하고, 로그 파일에 기록합니다.
ds.get_env()
