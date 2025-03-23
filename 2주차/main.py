def read_inventory_csv(filepath):
    # Mars_Base_Inventory_List.csv 파일의 내용을 읽어, 각 줄을 ','로 분리한 파이썬 리스트(List) 객체로 변환
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # 각 줄에서 개행 문자를 제거하고, ','로 분리하여 리스트로 변환 (첫 줄은 헤더)
        return [line.strip().split(',') for line in lines]
    except Exception as e:
        print('CSV 파일 읽는 중 오류가 발생했습니다:', e)
        return None

def print_inventory(data):
    # 리스트 형태의 인벤토리 데이터를 화면에 출력
    for row in data:
        print(','.join(row))

def filter_danger_items(data, threshold=0.7):
    # 헤더를 제외한 데이터에서 인화성 지수가 0.7 이상인 항목을 추출 (인화성 지수는 5번째 열, 인덱스 4)
    try:
        return [row for row in data[1:] if float(row[4]) >= threshold]
    except Exception as e:
        print('위험 항목 필터링 중 오류가 발생했습니다:', e)
        return []

def save_csv(data, filepath):
    # 리스트 데이터를 CSV 포맷으로 지정된 파일에 저장
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for row in data:
                f.write(','.join(row) + '\n')
    except Exception as e:
        print('CSV 파일 저장 중 오류가 발생했습니다:', e)

def save_binary(data, filepath):
    # 리스트 데이터를 문자열로 변환 후, 이진 파일 형태로 저장
    try:
        #이진 쓰기 모드 ='wb'
        with open(filepath, 'wb') as f:
            text = "\n".join([','.join(row) for row in data])
            f.write(text.encode('utf-8'))
    except Exception as e:
        print('이진 파일 저장 중 오류가 발생했습니다:', e)

def read_binary(filepath):
    # 이진 파일을 읽어 UTF-8 디코딩한 문자열로 반환
    try:
        #이진 읽기 모드 ='rb'
        with open(filepath, 'rb') as f:
            content = f.read()
        return content.decode('utf-8')
    except Exception as e:
        print('이진 파일 읽는 중 오류가 발생했습니다:', e)
        return None

def main():
    # 1. CSV 파일을 읽어 출력
    inventory = read_inventory_csv('Mars_Base_Inventory_List.csv')
    if inventory is None:
        return
    print('--- Mars_Base_Inventory_List.csv 내용 ---')
    print_inventory(inventory)
    
    # 2. 인벤토리 데이터를 인화성 지수 기준(5번째 열, float 값)으로 내림차순 정렬 (헤더 제외)
    header = inventory[0]
    sorted_inventory = [header] + sorted(inventory[1:], key=lambda row: float(row[4]), reverse=True)
    print('\n--- 인화성 순으로 정렬된 목록 ---')
    print_inventory(sorted_inventory)
    
    # 3. 인화성 지수가 0.7 이상인 항목 추출 (헤더 포함)
    danger_items = [header] + filter_danger_items(inventory, 0.7)
    print('\n--- 인화성 지수 0.7 이상인 위험 항목 ---')
    print_inventory(danger_items)
    
    # 4. 위험 항목을 CSV 포맷으로 Mars_Base_Inventory_danger.csv에 저장
    save_csv(danger_items, 'Mars_Base_Inventory_danger.csv')
    
    # 보너스 과제: 정렬된 전체 목록을 이진 파일로 저장 후 다시 읽어 출력
    save_binary(sorted_inventory, 'Mars_Base_Inventory_List.bin')
    binary_content = read_binary('Mars_Base_Inventory_List.bin')
    print('\n--- 이진 파일(Mars_Base_Inventory_List.bin) 읽은 내용 ---')
    print(binary_content)
    

if __name__ == '__main__':
    main()
