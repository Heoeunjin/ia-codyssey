from database import SessionLocal
from models import Question
from datetime import datetime

# 데이터베이스 세션 생성
db = SessionLocal()

# 테스트 질문 1
question1 = Question(
    subject='화성 기지 온도 조절 문제',
    content='화성 기지의 온도가 너무 낮습니다. 난방 시스템을 어떻게 개선할 수 있을까요?',
    create_date=datetime.now()
)

# 테스트 질문 2
question2 = Question(
    subject='산소 생성 시스템 오류',
    content='산소 생성 장치에서 이상한 소리가 납니다. 점검이 필요한가요?',
    create_date=datetime.now()
)

# 테스트 질문 3
question3 = Question(
    subject='통신 장비 업그레이드',
    content='지구와의 통신 속도를 향상시킬 수 있는 방법이 있나요?',
    create_date=datetime.now()
)

# 테스트 질문 4
question4 = Question(
    subject='식량 재배 효율화',
    content='수경 재배 시스템의 수확량을 늘리려면 어떻게 해야 하나요?',
    create_date=datetime.now()
)

# 테스트 질문 5
question5 = Question(
    subject='우주복 점검 주기',
    content='우주복 점검은 얼마나 자주 해야 안전한가요?',
    create_date=datetime.now()
)

# 데이터베이스에 추가
db.add(question1)
db.add(question2)
db.add(question3)
db.add(question4)
db.add(question5)

# 저장
db.commit()

# 세션 종료
db.close()

