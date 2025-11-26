from pydantic import BaseModel, ConfigDict
from datetime import datetime


class QuestionCreate(BaseModel):
    subject: str
    content: str


class Question(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str
    content: str
    create_date: datetime

