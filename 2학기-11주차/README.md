# 2학기-11주차: 화성 기지 질문 기능 구현

## 📌 프로젝트 개요
FastAPI와 ORM(SQLAlchemy)을 사용하여 화성 기지의 질문 기능을 구현한 프로젝트입니다.
데이터베이스 연동을 통해 질문 목록을 조회할 수 있는 RESTful API를 제공합니다.

## 🎯 학습 목표
- FastAPI의 APIRouter를 활용한 라우팅 구현
- ORM(SQLAlchemy)을 사용한 데이터베이스 작업
- RESTful API 설계 및 구현
- Dependency Injection 패턴 이해

## 📁 프로젝트 구조
```
2학기-11주차/
├── main.py                          # FastAPI 애플리케이션 진입점
├── database.py                      # 데이터베이스 연결 및 세션 관리
├── models.py                        # SQLAlchemy ORM 모델 정의
├── requirements.txt                 # 프로젝트 의존성 패키지
├── alembic.ini                      # Alembic 마이그레이션 설정
├── myapi.db                         # SQLite 데이터베이스 파일 (생성됨)
├── domain/
│   └── question/
│       ├── __init__.py
│       ├── question_router.py       # 질문 관련 API 라우터
│       ├── question_crud.py         # 질문 CRUD 작업 함수
│       └── question_schema.py       # Pydantic 스키마 정의
├── alembic/
│   ├── env.py                       # Alembic 환경 설정
│   ├── script.py.mako              # 마이그레이션 템플릿
│   └── versions/                    # 마이그레이션 버전 파일들
└── frontend/                        # 프론트엔드 파일 (향후 개발)
```

## 🛠 기술 스택
- **언어**: Python 3.x
- **웹 프레임워크**: FastAPI 0.115.6
- **ORM**: SQLAlchemy 2.0.36
- **마이그레이션 도구**: Alembic 1.14.0
- **웹 서버**: Uvicorn 0.34.0
- **데이터베이스**: SQLite

## 📦 설치 방법

### 1. 가상환경 생성 및 활성화
```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate

# 가상환경 활성화 (Windows)
venv\Scripts\activate
```

### 2. 의존성 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 마이그레이션

#### 마이그레이션 파일 생성
```bash
alembic revision --autogenerate -m "Create question table"
```

#### 마이그레이션 실행
```bash
alembic upgrade head
```

## 🚀 실행 방법

### 서버 실행
```bash
uvicorn main:app --reload
```

서버가 시작되면 다음 주소로 접속할 수 있습니다:
- **API 문서 (Swagger)**: http://127.0.0.1:8000/docs
- **API 문서 (ReDoc)**: http://127.0.0.1:8000/redoc

## 🔌 API 엔드포인트

### 질문 목록 조회
- **Method**: `GET`
- **URL**: `/api/question/list`
- **설명**: 모든 질문을 최신순으로 조회합니다.
- **Response**:
```json
[
  {
    "id": 1,
    "subject": "질문 제목",
    "content": "질문 내용",
    "create_date": "2025-11-26T10:30:00"
  }
]
```

## 💾 데이터베이스 스키마

### Question 테이블
| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
|--------|------------|----------|------|
| id | Integer | Primary Key | 질문 고유번호 (자동 증가) |
| subject | String | NOT NULL | 질문 제목 |
| content | Text | NOT NULL | 질문 내용 |
| create_date | DateTime | NOT NULL | 질문 작성일시 |

## 📝 코드 설명

### 1. main.py
FastAPI 애플리케이션의 진입점으로, 라우터를 등록합니다.

```python
from fastapi import FastAPI
from domain.question import question_router

app = FastAPI()
app.include_router(question_router.router)
```

### 2. question_router.py
질문 관련 API 라우터를 정의합니다.
- `prefix='/api/question'`로 기본 경로 설정
- `GET /list` 엔드포인트로 질문 목록 조회
- Dependency Injection으로 데이터베이스 세션 관리

### 3. question_crud.py
ORM을 사용하여 데이터베이스 작업을 수행합니다.
- `get_question_list()`: 질문 목록을 최신순으로 조회

### 4. database.py
SQLAlchemy 엔진과 세션을 설정합니다.
- `get_db()`: 데이터베이스 세션을 생성하고 관리하는 제너레이터 함수

## 🎓 주요 개념

### ORM (Object-Relational Mapping)
- 객체 지향 프로그래밍 언어와 관계형 데이터베이스 간의 데이터 변환 기술
- SQL 쿼리 대신 Python 코드로 데이터베이스 작업 수행
- 코드의 가독성과 유지보수성 향상

### APIRouter
- FastAPI의 라우터 기능으로 API 엔드포인트를 모듈화
- `prefix`를 사용하여 공통 경로 설정
- 각 도메인별로 라우터를 분리하여 관리

### Dependency Injection
- `Depends()`를 사용하여 의존성 주입
- 데이터베이스 세션을 자동으로 생성하고 종료
- 코드의 결합도를 낮추고 테스트 용이성 향상

## ✨ 보너스 과제

### Swagger UI로 API 테스트
1. 서버 실행 후 http://127.0.0.1:8000/docs 접속
2. `GET /api/question/list` 엔드포인트 선택
3. "Try it out" 버튼 클릭
4. "Execute" 버튼을 눌러 API 실행
5. Response body에서 질문 목록 확인

## 🔍 코딩 스타일 가이드 (PEP 8)

본 프로젝트는 PEP 8 스타일 가이드를 준수합니다:

### 문자열
- 작은따옴표(`'`)를 기본으로 사용
- 문자열 내에 `'`가 포함된 경우 큰따옴표(`"`) 사용

### 공백
- 대입문(`=`)의 앞뒤로 공백 사용
- 예: `foo = (0,)`

### 들여쓰기
- 공백 4칸 사용 (탭 사용 금지)

### 네이밍 컨벤션
- **함수명**: 소문자 + 언더스코어 (snake_case)
  - 예: `get_question_list()`, `question_create()`
- **클래스명**: CapWords 방식 (PascalCase)
  - 예: `Question`, `QuestionCreate`
- **변수명**: 소문자 + 언더스코어
  - 예: `question_list`, `db_question`

### 예약어 충돌 방지
- Python 예약어와 충돌하지 않도록 변수명 작성
- 필요시 언더스코어 접두사 사용 (예: `_question_list`)

## 🐛 문제 해결

### 마이그레이션 오류
```bash
# 현재 마이그레이션 상태 확인
alembic current

# 마이그레이션 히스토리 조회
alembic history
```

### 데이터베이스 초기화
```bash
# myapi.db 파일 삭제
rm myapi.db

# 마이그레이션 다시 실행
alembic upgrade head
```

### Import 오류
- 가상환경이 활성화되어 있는지 확인
- 필요한 패키지가 모두 설치되어 있는지 확인
```bash
pip list
```

## 📚 참고 자료
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 공식 문서](https://www.sqlalchemy.org/)
- [Alembic 공식 문서](https://alembic.sqlalchemy.org/)
- [PEP 8 – 파이썬 코드 스타일 가이드](https://peps.python.org/pep-0008/)
- [Pydantic 공식 문서](https://docs.pydantic.dev/)

## 📖 스토리
데이터베이스가 잘 연결되고 나니 많은 것을 해낸 것 같다. 한땀 한땀 데이터베이스를 작업하고 있는 한송희 박사에게 지구에 있는 엔지니어가 ORM이라는 것이 있고 이걸 사용하면 작업을 좀 더 원활하게 할 수 있다고 알려주는 메시지를 짧게 보내왔다. 엔지니어 특유의 투박한 메시지를 보자 한송희 박사는 웃음이 났지만 조금 찾아보았던 ORM의 개념은 많은 일들을 줄여주고 체계화 시키는데 도움이 될 것 같다.

---

**학습시간**: 5시간  
**분야**: 컴퓨터공학 - PYTHON  
**문제명**: 문제6 질문 기능을 추가해보자

