from __future__ import annotations

# 표준 라이브러리만 사용 (CSV 저장/불러오기용)
import csv
import os
from datetime import datetime
from typing import Dict, List

# 웹 프레임워크 (FastAPI) 컴포넌트 사용
from fastapi import APIRouter, FastAPI, HTTPException


# 애플리케이션 및 라우터 설정
app = FastAPI(title='Week 8 - Simple TODO with FastAPI')
router = APIRouter(prefix='/todos', tags=['todos'])


# 데이터 저장 위치 정의 (CSV 파일)
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
CSV_FILE_PATH = os.path.join(DATA_DIR, 'todos.csv')


# 메모리 내 TODO 리스트 (서버 시작 시 CSV에서 로딩)
todo_list: List[Dict[str, str]] = []


def ensure_data_dir() -> None:
    """데이터 디렉터리가 없다면 생성한다."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)


def csv_exists_and_has_header(file_path: str) -> bool:
    """CSV가 존재하고 헤더가 있으면 True를 반환한다."""
    if not os.path.exists(file_path):
        return False
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            sample = f.read(1024)
            return bool(sample.strip())
    except OSError:
        return False


def read_all_todos(file_path: str) -> List[Dict[str, str]]:
    """CSV에서 모든 TODO를 읽어 리스트로 반환한다. 없으면 빈 리스트."""
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows: List[Dict[str, str]] = []
        for row in reader:
            # None 값은 빈 문자열로 통일
            normalized = {k: (v if v is not None else '') for k, v in row.items()}
            rows.append(normalized)
        return rows


def write_header_if_needed(file_path: str, fieldnames: List[str]) -> None:
    """CSV가 비어 있으면 헤더를 쓴다."""
    if not csv_exists_and_has_header(file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()


def append_todo_to_csv(file_path: str, fieldnames: List[str], item: Dict[str, str]) -> None:
    """단일 TODO 항목을 CSV 맨 아래에 추가한다."""
    write_header_if_needed(file_path, fieldnames)
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(item)


def generate_todo_id(existing: List[Dict[str, str]]) -> str:
    """현재 개수 기반으로 증가하는 문자열 ID를 생성한다."""
    # 하드코딩 없이 길이 기반 증가 방식 사용
    return str(len(existing) + 1)


def now_iso() -> str:
    """마이크로초 제외 ISO 8601 UTC 시각 문자열을 반환한다."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'


@router.post('/add_todo')
def add_todo(payload: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    """새 TODO 항목 추가

    - 입력: 빈 값이 아닌 Dict
    - 출력: 생성된 TODO를 감싼 Dict
    - 동작: 메모리와 CSV에 동시에 반영
    """
    if not isinstance(payload, dict) or len(payload) == 0:
        # 보너스 과제: 빈 Dict 경고 처리
        raise HTTPException(status_code=400, detail='payload must be a non-empty object')

    # 기본 필드 정규화 + 서버 생성 필드(id, created_at) 부여
    todo_id = generate_todo_id(todo_list)
    created_at = now_iso()

    # CSV 단순화를 위해 모든 값을 문자열로 변환
    normalized: Dict[str, str] = {str(k): str(v) for k, v in payload.items()}
    normalized['id'] = todo_id
    normalized['created_at'] = created_at

    # 컬럼(헤더)은 입력 키의 합집합을 이용해 동적으로 계산 (하드코딩 회피)
    existing_keys = set()
    if todo_list:
        for item in todo_list:
            existing_keys.update(item.keys())
    all_keys = sorted(existing_keys.union(normalized.keys()))

    # 새 키가 생겨 헤더가 늘어나면, CSV를 안전하게 재작성해 일관성 유지
    # (외부 라이브러리 없이 구현)
    ensure_data_dir()
    current_rows = read_all_todos(CSV_FILE_PATH)
    if current_rows:
        # 기존 데이터의 모든 키 수집
        current_keys = set()
        for row in current_rows:
            current_keys.update(row.keys())
        if not set(all_keys).issubset(current_keys):
            merged_keys = sorted(current_keys.union(all_keys))
            with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=merged_keys)
                writer.writeheader()
                for row in current_rows:
                    writer.writerow({k: row.get(k, '') for k in merged_keys})
            append_todo_to_csv(CSV_FILE_PATH, merged_keys, {k: normalized.get(k, '') for k in merged_keys})
        else:
            append_todo_to_csv(CSV_FILE_PATH, sorted(current_keys), {k: normalized.get(k, '') for k in sorted(current_keys)})
    else:
        # 첫 기록: 현재 입력 키를 그대로 헤더로 사용
        append_todo_to_csv(CSV_FILE_PATH, all_keys, {k: normalized.get(k, '') for k in all_keys})

    # 최종적으로 메모리 리스트에 반영 (CSV와 동일 상태)
    todo_list.append(normalized)
    return {'todo': normalized}


@router.get('/retrieve_todo')
def retrieve_todo() -> Dict[str, List[Dict[str, str]]]:
    """모든 TODO를 Dict 형태로 반환한다."""
    return {'todos': list(todo_list)}


@app.get('/')
def read_root() -> Dict[str, str]:
    # 간단한 헬스 체크 및 사용 안내 메시지
    return {'message': 'TODO service is running. Use /todos/add_todo and /todos/retrieve_todo'}


def load_at_startup() -> None:
    """서버 시작 시 CSV의 기존 데이터를 메모리로 로딩한다."""
    ensure_data_dir()
    rows = read_all_todos(CSV_FILE_PATH)
    if rows:
        # 모든 값을 문자열로 통일
        normalized_rows: List[Dict[str, str]] = []
        for row in rows:
            normalized_rows.append({str(k): str(v) for k, v in row.items()})
        todo_list.extend(normalized_rows)


load_at_startup()
app.include_router(router)


