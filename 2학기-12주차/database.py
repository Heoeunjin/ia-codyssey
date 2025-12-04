import contextlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./myapi.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextlib.contextmanager
def get_db():
    '''
    데이터베이스 세션을 생성하고 사용이 끝나면 자동으로 종료하는 컨텍스트 매니저

    contextlib.contextmanager 데코레이터를 사용하여 구현
    yield 이전: 데이터베이스 연결 (setup)
    yield 이후: 데이터베이스 연결 종료 (teardown)
    '''
    db = SessionLocal()
    print(f'데이터베이스 연결됨: {db}')
    try:
        yield db
    finally:
        db.close()
        print('데이터베이스 연결 종료됨')

