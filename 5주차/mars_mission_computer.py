import platform #운영체제, OS 버전, CPU 타입 등 시스템 관련 정보
import os #CPU 코어 수를 가져오거나 파일 경로의 존재 여부를 확인
import json
import subprocess #메모리 크기, CPU 사용량, 등 정보
from datetime import datetime

class MissionComputer:
    """
    MissionComputer 클래스는 미션 컴퓨터의 시스템 정보와 부하 정보를 수집하여
    JSON 형식으로 출력하는 기능을 제공합니다.
    
    기본 정보:
      - operating_system: 운영체계 (platform.system())
      - os_version: 운영체제 버전 (platform.release())
      - cpu_type: CPU의 타입 (platform.processor())
      - cpu_cores: CPU 코어 수 (os.cpu_count())
      - memory_size_gb: 물리적 메모리 크기 (GB)
    
    부하 정보:
      - cpu_usage_percent: CPU 사용량 (%)
      - memory_usage_percent: 메모리 사용량 (%)
    
    보너스 과제:
      - setting.txt 파일이 없으면 기본 설정 파일을 생성하고, 해당 파일에 명시된 항목만 출력하도록 필터링합니다.
    """
    
    DEFAULT_SETTINGS = [
        'operating_system',
        'os_version',
        'cpu_type',
        'cpu_cores',
        'memory_size_gb'
    ] #설정 파일이 존재하지 않을 때, 기본 출력 항목으로 사용할 항목들을 정의
    
    def __init__(self):
        self.info = {}
        #시스템 정보를 저장할 빈 딕셔너리 self.info를 초기화

    def _create_default_settings_file(self, setting_file):
        """설정 파일이 없을 경우, DEFAULT_SETTINGS를 포함하는 기본 설정 파일을 생성"""
        try:
            with open(setting_file, 'w', encoding='utf-8') as f:
                for item in self.DEFAULT_SETTINGS:
                    f.write(item + "\n")
                    #DEFAULT_SETTINGS 리스트의 각 항목을 파일에 한 줄씩 기록
            print(f'기본 설정 파일 "{setting_file}" 생성 완료.')
        except Exception as e:
            print(f'설정 파일 생성 오류: {e}')

    def get_mission_computer_info(self):
        """
        시스템 정보를 수집하고 JSON 형식으로 출력 및 반환합니다.
        수집 항목:
          - operating_system, os_version, cpu_type, cpu_cores, memory_size_gb
        보너스: setting.txt 파일이 있으면 해당 파일에 명시된 항목만 필터링합니다.
        """
        try:
            # 총 메모리 크기를 sysctl 명령어로 가져오고 GB 단위로 환산
            mem_bytes = int(subprocess.check_output(['sysctl', '-n', 'hw.memsize']).strip())
            self.info = {
                'operating_system': platform.system(),
                'os_version': platform.release(),
                'cpu_type': platform.processor(),
                'cpu_cores': os.cpu_count(),
                'memory_size_gb': round(mem_bytes / (1024**3), 2)
            }
        except Exception as e:
            print(f'시스템 정보 수집 중 오류: {e}')
            self.info = {}
        
        setting_file = 'setting.txt'
        if not os.path.exists(setting_file):
            self._create_default_settings_file(setting_file)
        
        try:
            with open(setting_file, 'r', encoding='utf-8') as f:
                settings = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f'setting.txt 파일 읽기 오류: {e}')
            settings = None

        filtered_info = {k: v for k, v in self.info.items() if settings is None or k in settings}
        json_info = json.dumps(filtered_info, indent=4)
        print(json_info)
        return filtered_info

    def get_cpu_usage(self):
        """
        top 명령어를 사용하여 CPU 사용량 (%)를 계산합니다.
        macOS에서 "top -l 1" 명령어로 현재 CPU idle 값을 얻고,
        100에서 idle 값을 빼서 전체 CPU 사용량을 계산합니다.
        그 후 계산된 CPU 사용률을 반환
        """
        try:
            output = subprocess.check_output(['top', '-l', '1', '-n', '0']).decode('utf-8')
            for line in output.splitlines():
                if "CPU usage:" in line:
                    # 예: "CPU usage: 7.31% user, 5.23% sys, 87.45% idle"
                    parts = line.split(',')
                    idle_str = parts[-1].strip()  # "87.45% idle"
                    idle = float(idle_str.split('%')[0])
                    cpu_usage = round(100 - idle, 2)
                    return cpu_usage
        except Exception as e:
            print(f'CPU 사용량 가져오기 오류: {e}')
        return None

    def get_memory_usage(self):
        """
        vm_stat 명령어를 사용하여 메모리 사용량 (%)를 계산합니다.
        vm_stat를 통해 여유 메모리 페이지 수를 구하고, sysctl로 총 메모리 크기를 구해 사용률을 계산합니다.
        """
        try:
            vm_output = subprocess.check_output(['vm_stat']).decode('utf-8')
            pages = {}
            for line in vm_output.splitlines():
                if ':' in line:
                    key, value = line.split(':')
                    try:
                        pages[key.strip()] = int(value.strip().strip('.').split()[0])
                    except Exception:
                        continue
            total_bytes = int(subprocess.check_output(['sysctl', '-n', 'hw.memsize']).strip())
            free_pages = pages.get("Pages free", 0)
            page_size = 4096  # 기본 페이지 크기
            free_bytes = free_pages * page_size
            used_bytes = total_bytes - free_bytes
            memory_usage = round(used_bytes / total_bytes * 100, 2)
            return memory_usage
        except Exception as e:
            print(f'Memory usage 가져오기 오류: {e}')
        return None

    def get_mission_computer_load(self):
        """
        앞서 정의한 get_cpu_usage()와 get_memory_usage() 메소드를 호출하여 
        시스템 부하 정보를 수집하고, JSON 형식으로 출력하여 반환
        수집 항목:
          - cpu_usage_percent: CPU 사용량 (%)
          - memory_usage_percent: 메모리 사용량 (%)
        """
        try:
            load = {
                'cpu_usage_percent': self.get_cpu_usage(),
                'memory_usage_percent': self.get_memory_usage()
            }
        except Exception as e:
            print(f'부하 정보 수집 중 오류: {e}')
            load = {}
        json_load = json.dumps(load, indent=4)
        print(json_load)
        return load

if __name__ == '__main__':
    runComputer = MissionComputer() #MissionComputer 클래스의 인스턴스를 runComputer라는 이름으로 생성
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
    #메소드를 차례로 호출하여 시스템 정보와 부하 정보를 출력