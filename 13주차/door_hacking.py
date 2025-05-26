import sys

def caesar_cipher_decode(target_text):
    '''
    ✅ 문제 조건 충족:
    - caesar_cipher_decode 함수 이름 사용
    - target_text를 파라미터로 받음
    - 1~25까지 모든 자리수로 해독 시도
    - 사람이 직접 눈으로 보고 번호 입력
    - 최종 결과를 result.txt에 저장
    '''

    decoded_list = []  # ✅ 각 시프트 결과 저장

    for shift in range(1, 26):  # ✅ 1~25까지 자리수 반복
        result = ''

        for char in target_text:
            if 'A' <= char <= 'Z':
                # ✅ 대문자 해독 처리
                shifted = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                result += shifted
            elif 'a' <= char <= 'z':
                # ✅ 소문자 해독 처리
                shifted = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                result += shifted
            else:
                # ✅ 공백, 특수문자, 숫자는 그대로
                result += char

        decoded_list.append(result)
        print(f'{shift:>2}: {result}')  # ✅ 자리수별 해독 결과 출력 (반복마다 눈으로 확인 가능)

    # ✅ 사용자가 눈으로 보고 맞는 결과 번호를 선택
    try:
        choice = int(input('\n맞는 문장의 번호를 입력하세요 (1~25): '))
        if 1 <= choice <= 25:
            final_result = decoded_list[choice - 1]

            # ✅ 최종 결과를 result.txt에 저장 (조건 충족)
            with open('result.txt', 'w', encoding='utf-8') as f:
                f.write(final_result)
            print(f'[✔] result.txt에 저장 완료: {final_result}')
        else:
            print('[오류] 1~25 사이의 숫자를 입력하세요.')  # ✅ 유효 범위 검사
    except ValueError:
        print('[오류] 숫자를 입력해야 합니다.')  # ✅ 예외처리 포함

def read_password():
    '''
    ✅ password.txt에서 암호문 읽기
    - 파일 읽기 시도
    - 예외 처리 포함
    '''
    try:
        with open('password.txt', 'r', encoding='utf-8') as f:
            return f.read().strip()  # ✅ 줄바꿈 제거 후 반환
    except FileNotFoundError:
        print('[오류] password.txt 파일이 없습니다.')  # ✅ 조건: 파일 없을 경우 예외처리
    except Exception as e:
        print(f'[오류] 파일 읽기 실패: {e}')
    return None

if __name__ == '__main__':
    '''
    ✅ 전체 실행 흐름:
    - password.txt 읽고
    - 암호문이 있으면 해독 시도
    '''
    encrypted_text = read_password()
    if encrypted_text:
        caesar_cipher_decode(encrypted_text)
