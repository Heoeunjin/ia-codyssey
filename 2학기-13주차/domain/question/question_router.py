from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from domain.question import question_schema, question_crud


router = APIRouter(
    prefix='/api/question',
)


def get_db_session():
    '''
    FastAPI Depends를 위한 의존성 주입 함수

    contextlib.contextmanager로 정의된 get_db()를
    FastAPI의 Depends와 함께 사용하기 위한 래퍼 함수

    with 문을 사용하여 컨텍스트 매니저를 활성화하고
    데이터베이스 세션을 yield하여 자동 정리를 보장
    '''
    with get_db() as db:
        yield db


@router.get('/list', response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db_session)):
    '''
    질문 목록 조회 API

    Depends를 사용하여 데이터베이스 세션을 의존성 주입 받음
    - 요청 시작: 데이터베이스 연결 생성
    - 요청 종료: 데이터베이스 연결 자동 종료
    '''
    _question_list = question_crud.get_question_list(db)
    return _question_list


@router.get('/{question_id}', response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db_session)):
    '''
    특정 질문 상세 조회 API

    Args:
        question_id: 조회할 질문 ID
        db: 데이터베이스 세션 (의존성 주입)

    Returns:
        질문 객체

    Raises:
        HTTPException: 질문이 존재하지 않을 경우 404 에러
    '''
    question = question_crud.get_question(db, question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='질문을 찾을 수 없습니다'
        )
    return question


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=question_schema.Question)
def question_create(
    question_create: question_schema.QuestionCreate,
    db: Session = Depends(get_db_session)
):
    '''
    질문 등록 API

    POST 메소드를 사용하여 새로운 질문을 등록
    Depends를 사용하여 데이터베이스 연결 자동 관리

    Args:
        question_create: 질문 생성 데이터 (제목, 내용)
        db: 데이터베이스 세션 (의존성 주입)

    Returns:
        생성된 질문 객체

    Raises:
        HTTPException: 빈 값이 입력된 경우 422 에러
    '''
    created_question = question_crud.create_question(db, question_create)
    return created_question

