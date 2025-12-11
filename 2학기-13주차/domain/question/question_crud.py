from datetime import datetime

from sqlalchemy.orm import Session

from domain.question.question_schema import QuestionCreate
from models import Question


def get_question_list(db: Session):
    '''모든 질문 목록을 생성일 기준 내림차순으로 조회'''
    question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return question_list


def get_question(db: Session, question_id: int):
    '''특정 질문을 ID로 조회'''
    question = db.query(Question).filter(Question.id == question_id).first()
    return question


def create_question(db: Session, question_create: QuestionCreate):
    '''
    새로운 질문 생성

    Args:
        db: 데이터베이스 세션
        question_create: 질문 생성 스키마

    Returns:
        생성된 질문 객체
    '''
    db_question = Question(
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.now()
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

