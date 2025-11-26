# 화성 기지 게시판 프로젝트

## 프로젝트 개요
화성 기지와 지구 간의 원활한 소통을 위한 게시판 시스템입니다. FastAPI와 SQLAlchemy를 사용하여 구현되었습니다.

## 기술 스택
- **Backend Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: SQLite
- **Migration Tool**: Alembic

## 프로젝트 구조
```
├── main.py                 # FastAPI 애플리케이션 진입점
├── database.py            # 데이터베이스 연결 설정
├── models.py              # SQLAlchemy 모델 정의
├── domain/
│   └── question/
│       ├── question_router.py   # 질문 관련 API 라우터
│       ├── question_crud.py     # 질문 CRUD 작업
│       └── question_schema.py   # Pydantic 스키마
├── alembic/               # 데이터베이스 마이그레이션 파일
└── frontend/              # 프론트엔드 파일 (향후 개발)
```

## 설치 방법

### 1. 가상환경 생성 및 활성화
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 마이그레이션

#### Alembic revision 파일 생성
```bash
alembic revision --autogenerate -m "Create question table"
```

#### 마이그레이션 실행
```bash
alembic upgrade head
```

## 실행 방법

### 서버 실행
```bash
uvicorn main:app --reload
```

서버가 시작되면 다음 URL에서 접속할 수 있습니다:
- API 문서: http://127.0.0.1:8000/docs
- 대체 API 문서: http://127.0.0.1:8000/redoc

## API 엔드포인트

### 질문 목록 조회
- **GET** `/api/question/list`
- 모든 질문 목록을 최신순으로 반환합니다.

### 질문 상세 조회
- **GET** `/api/question/detail/{question_id}`
- 특정 질문의 상세 정보를 반환합니다.

### 질문 생성
- **POST** `/api/question/create`
- Request Body:
  ```json
  {
    "subject": "질문 제목",
    "content": "질문 내용"
  }
  ```

## 데이터베이스 스키마

### Question 테이블
| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | Integer | 질문 데이터의 고유번호 (Primary Key) |
| subject | String | 질문 제목 |
| content | Text | 질문 내용 |
| create_date | DateTime | 질문 작성일시 |

## 개발 가이드

### 코딩 스타일
- PEP 8 스타일 가이드를 준수합니다.
- 문자열은 작은따옴표(')를 기본으로 사용합니다.
- 함수명: 소문자 + 언더스코어 (snake_case)
- 클래스명: CapWords 방식 (PascalCase)
- 들여쓰기: 공백 4칸

## 보너스 과제

### DB Browser for SQLite로 데이터베이스 확인
1. DB Browser for SQLite를 설치합니다. (https://sqlitebrowser.org/)
2. `myapi.db` 파일을 엽니다.
3. `question` 테이블이 정상적으로 생성되었는지 확인합니다.

## 문제 해결

### 마이그레이션 오류
```bash
# 마이그레이션 히스토리 확인
alembic current

# 마이그레이션 히스토리 조회
alembic history
```

### 데이터베이스 초기화
```bash
# myapi.db 파일 삭제 후 다시 마이그레이션 실행
rm myapi.db
alembic upgrade head
```

## 참고 자료
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 공식 문서](https://www.sqlalchemy.org/)
- [Alembic 공식 문서](https://alembic.sqlalchemy.org/)
- [PEP 8 스타일 가이드](https://peps.python.org/pep-0008/)

