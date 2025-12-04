from fastapi import APIRouter, Depends
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
    '''특정 질문 상세 조회 API'''
    question = question_crud.get_question(db, question_id)
    return question

