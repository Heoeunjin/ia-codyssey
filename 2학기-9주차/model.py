from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel


class TodoItem(BaseModel):
    """TODO 항목을 표현하는 Pydantic 모델
    
    BaseModel을 상속받아 FastAPI에서 자동 검증 및 직렬화를 지원한다.
    모든 필드는 선택적(Optional)이며, 동적 필드 추가를 허용한다.
    """
    
    # Pydantic v1/v2 호환: Config 클래스 사용
    class Config:
        extra = 'allow'
    
    def to_dict(self) -> Dict[str, str]:
        """모델을 Dict[str, str] 형태로 변환한다."""
        result: Dict[str, str] = {}
        # Pydantic v2 호환: model_dump() 사용
        try:
            data = self.model_dump()
        except AttributeError:
            # Pydantic v1 호환: dict() 사용
            data = self.dict()
        
        for key, value in data.items():
            # 모든 값을 문자열로 변환 (CSV 저장 호환)
            result[str(key)] = str(value) if value is not None else ''
        return result

