# 2학기-13주차: 질문 등록 기능

## 📌 과제 개요

질문 등록(POST) 기능을 추가하여 질문 CRUD 기능을 완성합니다.

## ✅ 구현 사항

| 요구사항 | 구현 위치 | 설명 |
|---------|----------|------|
| QuestionCreate 스키마 작성 | `question_schema.py` | ✅ 제목, 내용 필드 정의 |
| 빈 값 검증 | `question_schema.py:14-20` | ✅ `@field_validator`로 빈 문자열 차단 |
| question_create() 메소드 | `question_router.py:71-89` | ✅ POST 엔드포인트 구현 |
| ORM 사용 | `question_crud.py:22-39` | ✅ SQLAlchemy로 데이터 저장 |
| POST 메소드 사용 | `question_router.py:71` | ✅ `@router.post` 데코레이터 |
| Depends로 DB 연결 관리 | `question_router.py:73` | ✅ 의존성 주입 |
| PEP 8 준수 | 전체 코드 | ✅ 작은따옴표, 공백, 네이밍 규칙 |

## 🚀 실행 방법

### 1. 가상환경 생성 및 패키지 설치

```bash
cd 2학기-13주차

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 데이터베이스 마이그레이션

```bash
# 데이터베이스 테이블 생성
alembic upgrade head
```

### 3. 테스트 데이터 추가 (선택)

```bash
# 5개의 테스트 질문 추가
python add_test_data.py
```

### 4. 서버 실행

```bash
uvicorn main:app --reload
```

서버가 실행되면: http://127.0.0.1:8000

## 🧪 테스트 방법

### 방법 1: Swagger UI (권장)

1. 브라우저에서 http://127.0.0.1:8000/docs 접속
2. **POST /api/question/create** 섹션 클릭
3. **Try it out** 버튼 클릭
4. Request body 입력:
   ```json
   {
     "subject": "테스트 질문",
     "content": "테스트 내용입니다"
   }
   ```
5. **Execute** 버튼 클릭
6. Response 확인:
   - Status Code: `201 Created`
   - Response Body: 생성된 질문 데이터 (id, subject, content, create_date 포함)

### 방법 2: curl 명령어

```bash
# 정상 케이스: 질문 등록 성공
curl -X POST "http://127.0.0.1:8000/api/question/create" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "테스트 질문",
    "content": "테스트 내용입니다"
  }'

# 예상 결과 (201 Created):
{
  "id": 6,
  "subject": "테스트 질문",
  "content": "테스트 내용입니다",
  "create_date": "2025-12-05T10:30:00"
}
```

### 방법 3: Python requests

```python
import requests

# 질문 등록
response = requests.post(
    'http://127.0.0.1:8000/api/question/create',
    json={
        'subject': '테스트 질문',
        'content': '테스트 내용입니다'
    }
)

print(f'Status Code: {response.status_code}')  # 201
print(f'Response: {response.json()}')
```

## ✅ 검증 항목

### 1. 정상 케이스 테스트

**테스트:** 제목과 내용을 정상적으로 입력
```json
{
  "subject": "화성 탐사 계획",
  "content": "다음 달 화성 탐사 일정을 알려주세요"
}
```

**예상 결과:**
- ✅ Status Code: `201 Created`
- ✅ Response에 `id`, `create_date` 포함
- ✅ 터미널에 "데이터베이스 연결됨" / "데이터베이스 연결 종료됨" 출력

### 2. 빈 값 검증 테스트

**테스트 A:** 제목이 빈 문자열
```json
{
  "subject": "",
  "content": "내용입니다"
}
```

**예상 결과:**
- ✅ Status Code: `422 Unprocessable Entity`
- ✅ Error Message: "빈 값은 허용되지 않습니다"

**테스트 B:** 내용이 공백만 있는 경우
```json
{
  "subject": "제목",
  "content": "   "
}
```

**예상 결과:**
- ✅ Status Code: `422 Unprocessable Entity`
- ✅ Error Message: "빈 값은 허용되지 않습니다"

### 3. DB 연결 자동 관리 확인

**테스트:** 질문 등록 API 호출 시 터미널 로그 확인

**예상 터미널 출력:**
```
데이터베이스 연결됨: <sqlalchemy.orm.session.Session object at 0x...>
INFO:     127.0.0.1:xxxxx - "POST /api/question/create HTTP/1.1" 201 Created
데이터베이스 연결 종료됨
```

✅ 요청마다 자동으로 연결/종료되는 것을 확인

### 4. 등록된 질문 조회

**테스트:** 등록 후 목록 조회
```bash
curl http://127.0.0.1:8000/api/question/list
```

**예상 결과:**
- ✅ 방금 등록한 질문이 목록 맨 위에 표시 (최신순)

## 📁 프로젝트 구조

```
2학기-13주차/
├── main.py                          # FastAPI 앱 진입점
├── database.py                      # DB 연결 (contextmanager)
├── models.py                        # SQLAlchemy ORM 모델
├── requirements.txt                 # 패키지 의존성
├── alembic.ini                      # Alembic 설정
├── add_test_data.py                # 테스트 데이터 스크립트
├── domain/
│   └── question/
│       ├── question_schema.py      # ✨ 빈 값 검증 추가
│       ├── question_crud.py        # ✨ create_question 구현
│       └── question_router.py      # ✨ POST 엔드포인트 추가
└── alembic/
    ├── env.py
    └── versions/
        └── c6606c3aebeb_create_question_table.py
```

## 🔑 핵심 코드

### 1. 빈 값 검증 (question_schema.py)

```python
class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator('subject', 'content')
    @classmethod
    def check_not_empty(cls, v):
        '''빈 문자열 검증'''
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다')
        return v
```

### 2. 질문 생성 함수 (question_crud.py)

```python
def create_question(db: Session, question_create: QuestionCreate):
    '''새로운 질문 생성'''
    db_question = Question(
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.now()
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)  # 생성된 ID를 가져오기 위해
    return db_question
```

### 3. POST 엔드포인트 (question_router.py)

```python
@router.post('/create', status_code=status.HTTP_201_CREATED)
def question_create(
    question_create: question_schema.QuestionCreate,
    db: Session = Depends(get_db_session)
):
    '''질문 등록 API'''
    created_question = question_crud.create_question(db, question_create)
    return created_question
```

## 📊 API 엔드포인트

| Method | Endpoint | 설명 | Status Code |
|--------|----------|------|-------------|
| GET | `/` | 루트 페이지 | 200 |
| GET | `/docs` | Swagger UI | 200 |
| GET | `/api/question/list` | 질문 목록 조회 | 200 |
| GET | `/api/question/{id}` | 질문 상세 조회 | 200 / 404 |
| **POST** | **/api/question/create** | **질문 등록** ✨ | **201 / 422** |

## 🎯 학습 포인트

1. **Pydantic field_validator**: 입력 데이터 검증
2. **POST 메소드**: RESTful API에서 생성 작업
3. **status_code 명시**: HTTP 201 Created 반환
4. **db.refresh()**: 생성된 객체의 ID 가져오기
5. **의존성 주입**: Depends로 일관된 DB 세션 관리

## 🐛 트러블슈팅

### 문제: 422 에러 - "field required"

**원인:** Request body에 `subject` 또는 `content` 누락

**해결:** 두 필드 모두 반드시 포함

### 문제: 빈 값 검증이 작동하지 않음

**원인:** `@field_validator` 데코레이터 순서 오류

**해결:** `@classmethod` 위에 `@field_validator` 작성

### 문제: DB 연결이 종료되지 않음

**확인:** 터미널에 "데이터베이스 연결 종료됨" 메시지 출력 여부

**해결:** `get_db_session()`에서 `with get_db() as db` 사용 확인

## 📝 과제 완료 체크리스트

- [x] QuestionCreate 스키마에 빈 값 검증 추가
- [x] question_crud.py에 create_question() 함수 구현
- [x] question_router.py에 POST 엔드포인트 추가
- [x] Depends로 DB 연결 자동 관리
- [x] PEP 8 코딩 스타일 준수
- [x] Swagger UI에서 정상 동작 확인
- [x] 빈 값 입력 시 422 에러 확인
- [x] 터미널에서 DB 연결/종료 로그 확인

