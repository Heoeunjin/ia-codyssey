# 전역변수 정의
FILE_PATH = 'Mars_Base_Inventory_List.csv'  # 읽을 CSV 파일 경로
DANGER_FILE_PATH = 'Mars_Base_Inventory_danger.csv'  # 필터링된 데이터를 저장할 파일 경로

def read_csv_file(file_path):
    try:
        # 파일을 읽기 모드로 열고, 파일 내용을 한 줄씩 읽어서 lines 리스트에 저장
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()  # 각 줄을 읽어서 리스트로 반환
        return lines  # 파일 내용이 담긴 리스트 반환
    except FileNotFoundError:
        # 파일이 없으면 오류 메시지 출력
        print(f'오류: 파일 "{file_path}"을 찾을 수 없습니다.')
        return None  # 파일이 없으면 None 반환
    except Exception as e:
        # 기타 다른 오류가 발생하면 오류 메시지 출력
        print(f'오류 발생: {e}')
        return None  # 오류 발생 시 None 반환

def write_csv_file(file_path, header, data):
    try:
        # 파일을 쓰기 모드로 열고, CSV 형식으로 데이터 작성
        with open(file_path, 'w', encoding='utf-8') as file:
            # 헤더를 첫 줄에 작성 (쉼표로 구분)
            file.write(','.join(header) + '\n')
            
            # data에 있는 각 row(행)를 처리
            for row in data:
                # row의 각 항목을 문자열로 변환 후 쉼표로 구분하여 파일에 작성
                file.write(','.join(map(str, row)) + '\n')
    except Exception as e:
        # 오류 발생 시 메시지 출력
        print(f'오류 발생: {e}')

def main():
    # 전역변수로 정의된 FILE_PATH를 사용하여 CSV 파일 읽기
    lines = read_csv_file(FILE_PATH)

    # 파일을 읽지 못한 경우 종료
    if lines is None:
        return

    # 첫 번째 줄(헤더)은 쉼표로 구분하여 분리
    header = lines[0].strip().split(',')
    
    # 첫 번째 줄을 제외한 나머지 줄들을 쉼표로 구분하여 데이터로 처리
    data = [line.strip().split(',') for line in lines[1:]]

    # 전체 파일 내용 출력 (디버깅 용)
    print("파일 내용:")
    for line in lines:
        print(line.strip())  # 각 줄을 출력 (공백 제거)

    # 인화성 지수(5번째 항목)를 기준으로 내림차순으로 정렬
    data.sort(key=lambda x: float(x[4]), reverse=True)

    # 인화성 지수가 0.7 이상인 항목만 필터링
    high_flammability = [row for row in data if float(row[4]) >= 0.7]

    # 필터링된 항목들 출력
    print('인화성 지수가 0.7 이상인 목록:')
    for item in high_flammability:
        print(item)

    # 필터링된 데이터를 새로운 CSV 파일에 저장
    # 전역변수 DANGER_FILE_PATH를 사용하여 새로운 CSV 파일에 저장
    write_csv_file(DANGER_FILE_PATH, header, high_flammability)

# 프로그램 실행 시작
if __name__ == '__main__':
    main()