## 2학기-9주차: 완전히 작동하는 TODO 시스템

### 요구사항 요약
- 8주차 TODO 시스템을 확장하여 완전한 CRUD 기능 구현
- 추가 기능:
  - `get_single_todo()`: GET, 경로 매개변수로 ID 받아 단일 조회
  - `update_todo()`: PUT, 경로 매개변수로 ID 받아 수정 (TodoItem 모델 사용)
  - `delete_single_todo()`: DELETE, 경로 매개변수로 ID 받아 삭제
- 모든 기능을 curl로 테스트
- 보너스: 클라이언트 앱 구현

### 프로젝트 구조
- `todo.py`: FastAPI 앱과 모든 라우터 (CRUD 기능 포함)
- `model.py`: TodoItem 클래스 (BaseModel 상속)
- `client.py`: 보너스 클라이언트 앱
- `data/todos.csv`: TODO 데이터 저장소 (자동 생성)

### 준비 (최초 1회)
```bash
cd "2학기-9주차"
source venv/bin/activate
pip install -r requirements.txt
```

### 실행

```bash
cd "2학기-9주차"
source venv/bin/activate
uvicorn todo:app --reload --host 0.0.0.0 --port 8000
```

브라우저로 확인: `http://127.0.0.1:8000`  
문서: `http://127.0.0.1:8000/docs`

### 테스트 방법 (curl)

#### 1. TODO 추가 (POST)
```bash
curl -s -X POST 'http://127.0.0.1:8000/todos/add_todo' \
  -H 'Content-Type: application/json' \
  -d '{"title": "첫 번째 작업", "description": "FastAPI 학습", "status": "open"}' | jq
```

#### 2. 모든 TODO 조회 (GET)
```bash
curl -s 'http://127.0.0.1:8000/todos/retrieve_todo' | jq
```

#### 3. 단일 TODO 조회 (GET)
```bash
# 위에서 추가한 TODO의 ID를 사용 (예: "1")
curl -s 'http://127.0.0.1:8000/todos/get_single_todo/1' | jq
```

#### 4. TODO 수정 (PUT)
```bash
# ID를 실제 TODO ID로 변경
curl -s -X PUT 'http://127.0.0.1:8000/todos/update_todo/1' \
  -H 'Content-Type: application/json' \
  -d '{"title": "수정된 제목", "description": "수정된 설명", "status": "completed"}' | jq
```

#### 5. TODO 삭제 (DELETE)
```bash
# ID를 실제 TODO ID로 변경
curl -s -X DELETE 'http://127.0.0.1:8000/todos/delete_single_todo/1' | jq
```

#### 6. 존재하지 않는 ID 조회 (404 테스트)
```bash
curl -i -s 'http://127.0.0.1:8000/todos/get_single_todo/99999'
```

### 보너스: 클라이언트 앱 실행

서버가 실행 중인 상태에서:

```bash
cd "2학기-9주차"
source venv/bin/activate
python client.py
```

클라이언트 앱이 모든 기능을 순차적으로 테스트하고 결과를 출력합니다.

### API 엔드포인트 정리

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/todos/retrieve_todo` | 모든 TODO 조회 |
| GET | `/todos/get_single_todo/{id}` | 단일 TODO 조회 |
| POST | `/todos/add_todo` | TODO 추가 |
| PUT | `/todos/update_todo/{id}` | TODO 수정 |
| DELETE | `/todos/delete_single_todo/{id}` | TODO 삭제 |

### 참고
- 모든 수정/삭제 작업은 CSV 파일에 즉시 반영됩니다.
- `id`와 `created_at`은 서버에서 자동 생성됩니다.
- 수정 시 `updated_at` 필드가 자동으로 추가됩니다.
- CSV 컬럼은 동적으로 확장되며, 하드코딩 없이 처리됩니다.

