from datetime import datetime

from pydantic import BaseModel, ConfigDict


class QuestionCreate(BaseModel):
    '''질문 생성 스키마'''
    subject: str
    content: str


class Question(BaseModel):
    '''
    질문 응답 스키마

    orm_mode (from_attributes) 설명:
    - True: ORM 객체(SQLAlchemy 모델)를 Pydantic 모델로 자동 변환 가능
            obj.attribute 형태로 속성에 접근하여 데이터를 읽음
    - False: dict 형태의 데이터만 허용
            obj['key'] 형태로만 데이터를 읽음

    SQLAlchemy 모델을 반환할 때는 from_attributes=True 필요
    '''
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str
    content: str
    create_date: datetime

