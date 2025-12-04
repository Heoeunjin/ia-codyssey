from fastapi import FastAPI

from domain.question import question_router

app = FastAPI()

app.include_router(question_router.router)


@app.get('/')
def root():
    '''루트 경로 - API 정보 반환'''
    return {'message': '화성 기지 API 서버', 'docs': '/docs'}

