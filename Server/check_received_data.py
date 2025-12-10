import requests
import json
import sys

BASE_URL = "http://localhost:8000"

# 요청 ID를 인자로 받거나 기본값 사용
REQUEST_ID = sys.argv[1] if len(sys.argv) > 1 else "req_20251210_043941_547c1772"

def check_received_data():
    """받은 데이터 확인"""
    print("=" * 60)
    print("받은 데이터 확인")
    print("=" * 60)
    
    # 요청 상태 확인
    print("\n[1] 요청 상태 확인")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/health/data/request/{REQUEST_ID}")
    if response.status_code == 200:
        status_info = response.json()
        print(f"요청 ID: {status_info['request_id']}")
        print(f"상태: {status_info['status']}")
        print(f"요청한 데이터 타입: {status_info['data_types']}")
        print(f"기간: {status_info['start_date']} ~ {status_info['end_date']}")
        print(f"생성 시각: {status_info['created_at']}")
        if status_info.get('completed_at'):
            print(f"완료 시각: {status_info['completed_at']}")
    else:
        print(f"오류: {response.text}")
        return
    
    # 받은 데이터 확인
    print("\n[2] 받은 데이터 확인")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/health/data/response/{REQUEST_ID}")
    if response.status_code == 200:
        data_response = response.json()
        print(f"요청 ID: {data_response['request_id']}")
        print(f"수신 시각: {data_response['received_at']}")
        print(f"\n받은 데이터:")
        print(json.dumps(data_response['data'], indent=2, ensure_ascii=False))
        
        # 데이터 요약
        data = data_response['data']
        print("\n[3] 데이터 요약")
        print("-" * 60)
        if data.get('steps'):
            print(f"걸음 수 데이터: {len(data['steps'])}개")
            for step in data['steps'][:3]:
                print(f"  - {step.get('date')}: {step.get('count')}보")
        if data.get('heart_rate'):
            print(f"심박수 데이터: {len(data['heart_rate'])}개")
            for hr in data['heart_rate'][:3]:
                print(f"  - {hr.get('timestamp')}: {hr.get('bpm')}bpm")
        if data.get('sleep'):
            print(f"수면 데이터: {len(data['sleep'])}개")
            for sleep in data['sleep'][:3]:
                print(f"  - {sleep.get('date')}: {sleep.get('hours')}시간")
    else:
        print(f"오류: {response.text}")
        print("데이터가 아직 수신되지 않았거나 저장되지 않았습니다.")

if __name__ == "__main__":
    check_received_data()

