import sounddevice as sd
import soundfile as sf
import os
from datetime import datetime

def create_records_folder():
    '''✅ records 폴더가 없으면 생성'''
    if not os.path.exists('records'):
        os.makedirs('records')

def record_audio(duration=5, samplerate=44100):
    '''🎙️ 음성 녹음 함수 (기본: 5초)'''
    print('[녹음 시작] 말을 하세요...')
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print('[녹음 완료] 파일 저장 중...')

    timestamp = datetime.now().strftime('%Y년%m월%d일-%H시%M분%S초')
    filename = f'records/{timestamp}.wav'
    sf.write(filename, audio, samplerate)
    print(f'[✔] 저장 완료: {filename}')

def show_records_between(start_date, end_date):
    '''📁 날짜 범위 내 녹음 파일 확인 기능 (보너스 과제)'''
    print(f'[{start_date} ~ {end_date}] 사이의 녹음 파일 목록:')
    for file in os.listdir('records'):
        if file.endswith('.wav'):
            name, _ = os.path.splitext(file)
            try:
                file_time = datetime.strptime(name, '%Y년%m월%d일-%H시%M분%S초')
                if start_date <= file_time.date() <= end_date:
                    print(' -', file)
            except ValueError:
                continue

if __name__ == '__main__':
    create_records_folder()          # ✅ 저장 폴더 생성
    record_audio()                   # ✅ 기본 5초 녹음

    # 보너스 기능 실행 예시 (주석 해제 시 사용 가능)
    # from datetime import date
    # show_records_between(date(2025, 5, 25), date(2025, 5, 26))
