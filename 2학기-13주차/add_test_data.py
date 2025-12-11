from datetime import datetime

from database import get_db
from models import Question

# contextlib.contextmanager로 정의된 get_db() 사용
# with 문으로 컨텍스트 매니저 활성화
# 블록 종료 시 자동으로 데이터베이스 연결 종료
with get_db() as db:
    # 테스트 질문 데이터
    test_questions = [
        Question(
            subject='화성 기지 온도 조절 문제',
            content='화성 기지의 온도가 너무 낮습니다. 난방 시스템을 어떻게 개선할 수 있을까요?',
            create_date=datetime.now()
        ),
        Question(
            subject='산소 생성 시스템 오류',
            content='산소 생성 장치에서 이상한 소리가 납니다. 점검이 필요한가요?',
            create_date=datetime.now()
        ),
        Question(
            subject='통신 장비 업그레이드',
            content='지구와의 통신 속도를 향상시킬 수 있는 방법이 있나요?',
            create_date=datetime.now()
        ),
        Question(
            subject='식량 재배 효율화',
            content='수경 재배 시스템의 수확량을 늘리려면 어떻게 해야 하나요?',
            create_date=datetime.now()
        ),
        Question(
            subject='우주복 점검 주기',
            content='우주복 점검은 얼마나 자주 해야 안전한가요?',
            create_date=datetime.now()
        ),
    ]

    # 데이터베이스에 추가
    for question in test_questions:
        db.add(question)

    # 저장
    db.commit()
    print(f'{len(test_questions)}개의 테스트 질문이 추가되었습니다.')

# with 블록을 벗어나면 자동으로 db.close() 호출됨

