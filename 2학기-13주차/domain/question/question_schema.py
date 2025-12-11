from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class QuestionCreate(BaseModel):
    '''
    질문 생성 스키마

    제목과 내용은 빈 값을 허용하지 않음
    '''
    subject: str
    content: str

    @field_validator('subject', 'content')
    @classmethod
    def check_not_empty(cls, v):
        '''빈 문자열 검증'''
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다')
        return v


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

