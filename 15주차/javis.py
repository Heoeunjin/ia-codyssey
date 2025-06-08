#14주차 recoders/ 확인해 주시면 됩니다.
import os
import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime
import glob
import csv
import speech_recognition as sr
from pydub import AudioSegment

#문제 7에서 녹음된 음성파일들
RECORD_FOLDER = '../14주차/records'
os.makedirs(RECORD_FOLDER, exist_ok=True)

# ✅ 음성 녹음 함수 (문제 7, PEP8 스타일 적용)
def record_voice(duration=10, sample_rate=44100):
    print(f'{duration}초간 녹음 시작...')
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    filename = datetime.now().strftime('%Y%m%d-%H%M%S') + '.wav'
    filepath = os.path.join(RECORD_FOLDER, filename)
    write(filepath, sample_rate, audio_data)
    print(f'녹음 완료! 저장 위치: {filepath}')
    return filepath

# ✅ 날짜 범위 내 파일 검색 기능 (보너스 과제)
def list_records_by_date(start_date, end_date):
    print(f'녹음 파일 검색: {start_date} ~ {end_date}')
    start_dt = datetime.strptime(start_date, '%Y%m%d')
    end_dt = datetime.strptime(end_date, '%Y%m%d')
    matched_files = []
    for filepath in glob.glob(os.path.join(RECORD_FOLDER, '*.wav')):
        filename = os.path.basename(filepath)
        try:
            file_dt = datetime.strptime(filename[:8], '%Y%m%d')
            if start_dt <= file_dt <= end_dt:
                matched_files.append(filename)
        except ValueError:
            continue
    if matched_files:
        print('검색된 녹음 파일 목록:')
        for f in sorted(matched_files):
            print(f' - {f}')
    else:
        print('해당 기간에 녹음 파일이 없습니다.')

# ✅ STT 변환 및 CSV 저장 (문제 8, 외부 라이브러리 사용 허용 범위 내)
def transcribe_audio_to_csv(wav_path):
    AudioSegment.converter = '/opt/homebrew/bin/ffmpeg'
    AudioSegment.ffprobe = '/opt/homebrew/bin/ffprobe'

    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav(wav_path)
    duration_sec = len(audio) / 1000
    chunk_length = 10
    base_filename = os.path.splitext(os.path.basename(wav_path))[0]
    csv_path = os.path.join(RECORD_FOLDER, base_filename + '.csv')

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['시작시간(초)', '인식된 텍스트'])
        for i in range(0, int(duration_sec), chunk_length):
            chunk = audio[i*1000:(i+chunk_length)*1000]
            chunk.export('temp.wav', format='wav')
            with sr.AudioFile('temp.wav') as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language='ko-KR')
                except sr.UnknownValueError:
                    text = '(인식 실패)'
                except sr.RequestError as e:
                    print(f'STT 오류 발생: {e}')
                    break
                writer.writerow([i, text])
                print(f'{i}초 ~ {i+chunk_length}초: {text}')
    os.remove('temp.wav')
    print(f'CSV 저장 완료: {csv_path}')

# ✅ 키워드 검색 (보너스 과제)
def search_keyword_in_transcripts(keyword):
    print(f'키워드 검색: "{keyword}"')
    results = []
    for csv_file in glob.glob(os.path.join(RECORD_FOLDER, '*.csv')):
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if keyword in row[1]:
                    results.append((os.path.basename(csv_file), row[0], row[1]))
    if results:
        print('[🔎] 검색 결과:')
        for file, time, text in results:
            print(f'📄 {file} | ⏱️ {time}초 | 🗣️ {text}')
    else:
        print('키워드를 포함하는 텍스트를 찾을 수 없습니다.')

# ✅ 메뉴 함수 매핑 방식으로 if-else 최소화

def handle_record():
    try:
        sec = int(input('녹음 시간 (초): '))
        record_voice(duration=sec)
    except ValueError:
        print('[오류] 숫자로 입력해 주세요.')

def handle_list():
    s = input('시작 날짜 (예: 20240501): ')
    e = input('종료 날짜 (예: 20240531): ')
    list_records_by_date(s, e)

def handle_transcribe():
    wav_files = sorted(glob.glob(os.path.join(RECORD_FOLDER, '*.wav')))
    if not wav_files:
        print('녹음된 파일이 없습니다.')
        return

    print('\n[📁 변환 가능한 녹음 파일 목록]')
    for idx, path in enumerate(wav_files):
        print(f'{idx + 1}. {os.path.basename(path)}')

    try:
        choice = int(input('변환할 파일 번호를 선택하세요: '))
        selected_file = wav_files[choice - 1]
        transcribe_audio_to_csv(selected_file)
    except (ValueError, IndexError):
        print('[오류] 잘못된 선택입니다.')

def handle_search():
    keyword = input('검색할 키워드: ')
    search_keyword_in_transcripts(keyword)

def handle_exit():
    print('프로그램을 종료합니다.')
    exit()

menu_actions = {
    '1': handle_record,
    '2': handle_list,
    '3': handle_transcribe,
    '4': handle_search,
    '0': handle_exit
}

def main_menu():
    while True:
        print('\n=== Javis 음성 기록 시스템 ===')
        print('1. 새 음성 녹음')
        print('2. 날짜 범위로 녹음 파일 조회')
        print('3. 녹음 파일 → 텍스트 변환(STT + CSV 저장)')
        print('4. 키워드로 기록 검색 (CSV 내)')
        print('0. 종료')
        choice = input('선택 >> ')
        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print('잘못된 선택입니다.')

if __name__ == '__main__':
    main_menu()
