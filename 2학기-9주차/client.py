#!/usr/bin/env python3
"""
TODO 클라이언트 앱 (보너스 과제)

서버의 모든 TODO 기능을 호출하여 동작을 확인하는 간단한 클라이언트입니다.
"""

from __future__ import annotations

import json
from typing import Dict, Any

import requests


# 서버 기본 URL
BASE_URL = 'http://127.0.0.1:8000'


def print_response(title: str, response: requests.Response) -> None:
    """응답을 보기 좋게 출력한다."""
    print(f'\n=== {title} ===')
    print(f'Status Code: {response.status_code}')
    try:
        data = response.json()
        print(f'Response: {json.dumps(data, indent=2, ensure_ascii=False)}')
    except Exception:
        print(f'Response: {response.text}')


def add_todo(data: Dict[str, str]) -> Dict[str, Any] | None:
    """TODO 추가"""
    try:
        response = requests.post(f'{BASE_URL}/todos/add_todo', json=data)
        print_response('TODO 추가', response)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f'에러 발생: {e}')
    return None


def retrieve_all_todos() -> Dict[str, Any] | None:
    """모든 TODO 조회"""
    try:
        response = requests.get(f'{BASE_URL}/todos/retrieve_todo')
        print_response('모든 TODO 조회', response)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f'에러 발생: {e}')
    return None


def get_single_todo(todo_id: str) -> Dict[str, Any] | None:
    """단일 TODO 조회"""
    try:
        response = requests.get(f'{BASE_URL}/todos/get_single_todo/{todo_id}')
        print_response(f'단일 TODO 조회 (ID: {todo_id})', response)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f'에러 발생: {e}')
    return None


def update_todo(todo_id: str, data: Dict[str, str]) -> Dict[str, Any] | None:
    """TODO 수정"""
    try:
        response = requests.put(f'{BASE_URL}/todos/update_todo/{todo_id}', json=data)
        print_response(f'TODO 수정 (ID: {todo_id})', response)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f'에러 발생: {e}')
    return None


def delete_todo(todo_id: str) -> Dict[str, Any] | None:
    """TODO 삭제"""
    try:
        response = requests.delete(f'{BASE_URL}/todos/delete_single_todo/{todo_id}')
        print_response(f'TODO 삭제 (ID: {todo_id})', response)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f'에러 발생: {e}')
    return None


def main() -> None:
    """메인 함수: 모든 기능을 순차적으로 테스트"""
    print('=' * 60)
    print('TODO 클라이언트 앱 - 모든 기능 테스트')
    print('=' * 60)
    
    # 1. TODO 추가
    print('\n[1] TODO 추가 테스트')
    todo1 = add_todo({
        'title': '클라이언트 테스트 1',
        'description': '첫 번째 테스트 항목',
        'status': 'open'
    })
    
    todo2 = add_todo({
        'title': '클라이언트 테스트 2',
        'description': '두 번째 테스트 항목',
        'status': 'in_progress'
    })
    
    # 추가된 TODO의 ID 추출
    todo1_id = todo1.get('todo', {}).get('id') if todo1 else None
    todo2_id = todo2.get('todo', {}).get('id') if todo2 else None
    
    # 2. 모든 TODO 조회
    print('\n[2] 모든 TODO 조회 테스트')
    retrieve_all_todos()
    
    # 3. 단일 TODO 조회
    if todo1_id:
        print('\n[3] 단일 TODO 조회 테스트')
        get_single_todo(todo1_id)
    
    # 4. TODO 수정
    if todo1_id:
        print('\n[4] TODO 수정 테스트')
        update_todo(todo1_id, {
            'title': '수정된 제목',
            'description': '수정된 설명',
            'status': 'completed'
        })
    
    # 5. 수정 후 다시 조회
    if todo1_id:
        print('\n[5] 수정 후 단일 TODO 조회')
        get_single_todo(todo1_id)
    
    # 6. 모든 TODO 다시 조회 (수정 반영 확인)
    print('\n[6] 수정 후 모든 TODO 조회')
    retrieve_all_todos()
    
    # 7. TODO 삭제
    if todo2_id:
        print('\n[7] TODO 삭제 테스트')
        delete_todo(todo2_id)
    
    # 8. 삭제 후 모든 TODO 조회 (삭제 반영 확인)
    print('\n[8] 삭제 후 모든 TODO 조회')
    retrieve_all_todos()
    
    # 9. 존재하지 않는 ID로 조회 (404 테스트)
    print('\n[9] 존재하지 않는 ID 조회 테스트 (404 예상)')
    get_single_todo('99999')
    
    print('\n' + '=' * 60)
    print('모든 테스트 완료!')
    print('=' * 60)


if __name__ == '__main__':
    main()

