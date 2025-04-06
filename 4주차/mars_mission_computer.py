import random
import json
import time
import sys
import select
from datetime import datetime

class DummySensor:
    """
    DummySensor 클래스는 화성 기지의 환경 센서 데이터를 임의로 생성하여 저장하는 클래스입니다.
    환경 데이터는 다음 항목들을 포함합니다:
      - mars_base_internal_temperature (화성 기지 내부 온도)
      - mars_base_external_temperature (화성 기지 외부 온도)
      - mars_base_internal_humidity (화성 기지 내부 습도)
      - mars_base_external_illuminance (화성 기지 외부 광량)
      - mars_base_internal_co2 (화성 기지 내부 이산화탄소 농도)
      - mars_base_internal_oxygen (화성 기지 내부 산소 농도)
    """
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
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
        만약 센서 데이터가 초기화되지 않은 경우, 경고 메시지를 출력하고 자동으로 set_env()를 호출합니다.
        보너스 과제로, 현재 날짜와 시간 및 각 센서 값을 개별 줄에 출력하고,
        'sensor_log.txt' 파일에 로그로 기록합니다.
        """
        # 센서 데이터가 초기화되지 않은 경우 자동으로 설정
        if any(value is None for value in self.env_values.values()):
            print('경고: 센서 데이터가 초기화되지 않았습니다. set_env()를 호출합니다.')
            self.set_env()
        
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sensor_lines = [f'{key}: {value}' for key, value in self.env_values.items()]
        output = f'{now}\n' + "\n".join(sensor_lines)
        print(output)
  
        try:
            with open('sensor_log.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(output + "\n")
        except Exception as e:
            print(f'로그 파일 저장 중 오류: {e}')
            
        return self.env_values

class MissionComputer:
    """
    MissionComputer 클래스는 미션 컴퓨터의 환경 센서 데이터를 주기적으로 수집하여 출력하고,
    JSON 형식으로 시스템 정보를 제공하는 기능을 갖습니다.
    
    - DummySensor 인스턴스를 사용하여 센서 데이터를 갱신합니다.
    - 5초마다 센서 데이터를 출력하며, 5분마다 각 센서의 평균값을 계산하여 출력합니다.
    - 보너스: 사용자가 'q'를 입력하면 반복을 멈추고 'System stopped….' 메시지를 출력합니다.
    """
    def __init__(self):
        self.env_values = {}
        self.ds = DummySensor()
        # 센서 데이터 히스토리를 저장하여 5분 평균을 계산하기 위한 딕셔너리
        self.readings_history = {key: [] for key in self.ds.env_values.keys()}
        self.last_avg_time = time.time()

    def get_sensor_data(self):
        """
        5초마다 센서 데이터를 갱신하고, JSON 형식으로 출력하며 로그 파일에 기록합니다.
        또한, 5분마다 센서 데이터의 평균값을 계산하여 출력합니다.
        사용자가 'q'를 입력하면 출력 반복을 중단합니다.
        """
        print("센서 데이터 출력 시작 (종료하려면 'q' 입력):")
        while True:
            # 비차단식으로 사용자 입력 확인 (q 입력 시 종료)
            rlist, _, _ = select.select([sys.stdin], [], [], 0)
            if rlist:
                user_input = sys.stdin.readline().strip()
                if user_input.lower() == 'q':
                    print("System stopped....")
                    break
            
            # 센서 데이터를 갱신
            self.ds.set_env()
            current_data = self.ds.get_env()
            self.env_values = current_data
            
            # 각 센서 값들을 히스토리에 추가 (5분 평균 계산 용)
            for key, value in current_data.items():
                self.readings_history[key].append(value)
            
            # 현재 날짜 및 시간과 센서 데이터를 JSON 형식으로 출력
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            output = {"timestamp": now, **current_data}
            print(json.dumps(output, indent=4))
            
            # 5분마다 평균값 계산 및 출력
            current_time = time.time()
            if current_time - self.last_avg_time >= 300:  # 300초 = 5분
                avg_data = {}
                for key, values in self.readings_history.items():
                    if values:
                        avg_data[key] = round(sum(values) / len(values), 2)
                    else:
                        avg_data[key] = None
                print("\n5분 평균 값:")
                print(json.dumps(avg_data, indent=4))
                # 히스토리 초기화 및 마지막 평균 계산 시간 갱신
                self.readings_history = {key: [] for key in self.ds.env_values.keys()}
                self.last_avg_time = current_time
            
            time.sleep(5)

if __name__ == '__main__':
    # MissionComputer 클래스 인스턴스를 RunComputer라는 이름으로 생성하고, 
    # get_sensor_data() 메소드를 호출하여 지속적으로 센서 데이터를 출력합니다.
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()
