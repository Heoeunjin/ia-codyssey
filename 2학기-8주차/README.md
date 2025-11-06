## 2학기-8주차: FastAPI TODO 서비스

### 요구사항 요약
- FastAPI 기반 TODO API 구현
- `APIRouter` 사용: `add_todo`(POST), `retrieve_todo`(GET)
- 입출력은 Dict 타입
- CSV 파일에 저장/불러오기 (DB 사용 금지)
- venv 사용, 웹 서버는 Uvicorn 사용
- PEP 8 스타일 준수, 문자열은 기본 `'` 사용
- 보너스: 빈 Dict 입력 시 경고(400 에러)

### 프로젝트 구조
- `todo.py`: FastAPI 앱과 라우터, CSV I/O 포함
- `data/todos.csv`: TODO 데이터 저장소 (자동 생성)

### 준비 (최초 1회)
이미 venv 생성 및 FastAPI/Uvicorn 설치가 완료되어 있습니다.

### 실행

```bash
cd "$(dirname "$0")"
source venv/bin/activate
uvicorn todo:app --reload --host 0.0.0.0 --port 8000
```

브라우저로 확인: `http://127.0.0.1:8000`  
문서: `http://127.0.0.1:8000/docs`

### 테스트 (curl)

- 추가 (POST /todos/add_todo)

```bash
curl -s -X POST 'http://127.0.0.1:8000/todos/add_todo' \
  -H 'Content-Type: application/json' \
  -d '{"title": "First task", "description": "Study FastAPI", "status": "open"}' | jq
```

- 조회 (GET /todos/retrieve_todo)

```bash
curl -s 'http://127.0.0.1:8000/todos/retrieve_todo' | jq
```

- 보너스: 빈 Dict 입력 시 (400)

```bash
curl -i -s -X POST 'http://127.0.0.1:8000/todos/add_todo' \
  -H 'Content-Type: application/json' -d '{}'
```

### 참고
- CSV 컬럼은 입력 Dict의 키에 따라 동적으로 확장됩니다. 기존 데이터가 있을 때 새로운 키가 추가되면 헤더를 재작성해 데이터 일관성을 유지합니다.
- `id`와 `created_at`은 서버에서 자동으로 채워집니다.


