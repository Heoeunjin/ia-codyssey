import zipfile
import itertools
import string
import time

def unlock_zip(zip_path='emergency_storage_key.zip', output_file='password.txt'):
    '''
    🔐 6자리 소문자 + 숫자로 구성된 암호를 무차별 대입 방식으로 푸는 함수입니다.
    
    ✅ 조건 충족:
    - zipfile: 외부 라이브러리 사용 허용된 부분
    - itertools + string: 파이썬 기본 제공
    - 예외처리, 진행 시간, 반복 회수 출력
    - 성공 시 password.txt에 저장
    '''
    
    charset = string.ascii_lowercase + string.digits  
    # ✅ 소문자 + 숫자, 암호에 사용할 수 있는 모든 문자 조합의 문자 집합 의미
    max_length = 6

    try:
        with zipfile.ZipFile(zip_path) as zf:
            start_time = time.time()
            attempts = 0

            # ✅ 보너스: itertools를 활용한 효율적인 조합 생성 (중복 최소화)
            for pwd in itertools.product(charset, repeat=max_length):
                password = ''.join(pwd)
                try:
                    zf.extractall(pwd=password.encode())  # ✅ 비밀번호 시도
                    duration = time.time() - start_time

                    # ✅ 성공 시 password.txt에 기록
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(password)

                    print(f'[✔] 성공: 비밀번호는 "{password}"입니다.')
                    print(f'총 시도 횟수: {attempts}회 / 소요 시간: {round(duration, 2)}초')
                    return
                except:
                    attempts += 1
                    # ✅ 중간 진행상황 출력 (성능 고려해 1만 회마다)
                    if attempts % 10000 == 0:
                        print(f'{attempts}회 시도 중... 경과 시간: {round(time.time() - start_time, 2)}초')

            print('[✖] 실패: 비밀번호를 찾을 수 없습니다.')

    # ✅ 파일 관련 예외 처리
    except FileNotFoundError:
        print(f'[오류] "{zip_path}" 파일을 찾을 수 없습니다.')
    except zipfile.BadZipFile:
        print(f'[오류] "{zip_path}"는 유효한 zip 파일이 아닙니다.')

if __name__ == '__main__':
    unlock_zip()
