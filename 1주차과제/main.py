import datetime

def parse_timestamp(line):
    # 제약조건: 로그 항목의 타임스탬프가 'YYYY-MM-DD HH:MM:SS' 형식임을 가정하고 파싱합니다.
    try:
        # 기본 문자열 표기는 ''를 사용 (PEP 8 준수)
        timestamp_str = line[:19]
        # datetime 모듈의 strptime 함수를 사용하여 타임스탬프 파싱
        timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        return timestamp
    except ValueError:
        # 예외 처리: 파싱 실패 시 None 반환 (파일 처리 예외를 처리하는 부분)
        return None

def read_and_print_log():
    # 파일 이름은 요구사항에 따라 mission_computer_main.log로 지정
    log_filename = 'mission_computer_main.log'
    problematic_lines = []  # 보너스 과제: 문제 이벤트를 따로 저장
    lines_with_timestamp = []
    lines_without_timestamp = []
    total_lines = []  # 전체 로그 항목 저장 (보고서 작성을 위한 데이터)

    try:
        # 파일 입출력 시 예외 처리를 통해 안전하게 파일을 읽음
        with open(log_filename, 'r', encoding='utf-8') as f:
            # 첫 번째 줄은 헤더라고 가정하여 건너뜁니다.
            header = f.readline()  # CSV 헤더: 'timestamp,event,message'
            lines = f.readlines()
    except Exception as e:
        print('로그 파일을 여는 중 오류가 발생했습니다:', e)
        return None, None

    # 각 로그 라인마다 처리: 타임스탬프 파싱 및 문제 판별
    for line in lines:
        # 문자열 내 기본 개행 문자 제거, '' 사용
        line = line.rstrip('\n')
        total_lines.append(line)
        ts = parse_timestamp(line)
        if ts is not None:
            # 타임스탬프가 파싱된 경우 리스트에 저장 (보너스: 시간 역순 정렬을 위해)
            lines_with_timestamp.append((ts, line))
        else:
            lines_without_timestamp.append(line)

        # 보너스 과제 조건: 문제가 되는 이벤트만 별도로 추출
        # 문자열 내 'unstable' 또는 'explosion'이 포함된 경우
        if 'unstable' in line.lower() or 'explosion' in line.lower():
            problematic_lines.append(line)

    # 타임스탬프를 기준으로 로그 항목을 최근 순(역순)으로 정렬 (보너스 과제)
    lines_with_timestamp.sort(key=lambda x: x[0], reverse=True)
    
    print('--- 로그 파일 출력 (시간의 역순 정렬) ---')
    for ts, line in lines_with_timestamp:
        print(line)
    # 타임스탬프 파싱 실패한 라인들도 출력
    for line in lines_without_timestamp:
        print(line)

    # 보너스 과제 조건: 문제가 되는 이벤트를 별도의 파일로 저장 (파일명: problematic.log)
    try:
        with open('problematic.log', 'w', encoding='utf-8') as pf:
            for line in problematic_lines:
                pf.write(line + '\n')
    except Exception as e:
        print('문제가 되는 부분을 저장하는 중 오류가 발생했습니다:', e)

    # 전체 로그와 문제 이벤트 데이터를 반환 (Markdown 보고서 생성에 사용)
    return total_lines, problematic_lines

def generate_markdown_report(total_lines, problematic_lines):
    # 제약조건: 보고서는 UTF-8 인코딩의 Markdown 형태의 파일로 작성되어야 하므로 log_analysis.md로 저장
    try:
        with open('log_analysis.md', 'w', encoding='utf-8') as report_file:
            report_file.write('# 로그 분석 보고서\n\n')
            report_file.write('## 개요\n')
            report_file.write('본 보고서는 mission_computer_main.log 파일의 로그 데이터를 분석한 결과를 정리한 것입니다.\n\n')
            
            report_file.write('## 로그 요약\n')
            # 파일에 저장되는 문자열은 기본적으로 '' 사용 (문자열 내에서 필요한 경우 " "도 사용)
            report_file.write('- 총 로그 항목 수: ' + str(len(total_lines)) + '\n')
            report_file.write('- 문제 발생 로그 수: ' + str(len(problematic_lines)) + '\n\n')
            
            report_file.write('## 문제 발생 이벤트\n')
            if problematic_lines:
                for line in problematic_lines:
                    report_file.write('- ' + line + '\n')
            else:
                report_file.write('문제가 되는 이벤트는 발견되지 않았습니다.\n')
            
            report_file.write('\n## 사고 원인 분석\n')
            if problematic_lines:
                report_file.write('로그 데이터를 분석한 결과, 사고의 원인은 다음과 같이 추정됩니다:\n\n')
                if any('oxygen tank unstable' in line.lower() for line in problematic_lines):
                    report_file.write('- 산소 탱크 불안정성이 확인되었습니다.\n')
                if any('oxygen tank explosion' in line.lower() for line in problematic_lines):
                    report_file.write('- 산소 탱크 폭발이 발생하였습니다.\n')
                report_file.write('\n이로 미루어 볼 때, 산소 탱크 관련 문제가 전체 미션에 치명적인 영향을 미쳤을 가능성이 높습니다.\n')
            else:
                report_file.write('문제가 되는 이벤트가 없어 추가 분석이 필요합니다.\n')
    except Exception as e:
        print('보고서를 생성하는 중 오류가 발생했습니다:', e)

def main():
    # Python 설치 확인: 'Hello Mars'를 출력 (설치 확인 및 간단한 출력 요구사항 충족)
    print('Hello Mars')
    
    # 로그 파일을 분석하고 출력하는 함수 호출 (예외 처리 포함)
    total_lines, problematic_lines = read_and_print_log()
    if total_lines is not None:
        # Markdown 보고서 자동 생성 (요구사항: log_analysis.md로 저장, UTF-8 인코딩)
        generate_markdown_report(total_lines, problematic_lines)
        print('\nlog_analysis.md 보고서가 생성되었습니다.')

# main.py 파일로 저장되어야 하며, 이 파일이 메인 실행 파일임을 명시 (PEP 8 준수)
if __name__ == '__main__':
    main()
