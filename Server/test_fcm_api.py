import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_register_device():
    """FCM 토큰 등록 테스트"""
    print("\n=== 1. 디바이스 등록 테스트 ===")
    url = f"{BASE_URL}/devices/register"
    data = {
        "device_id": "test_device_001",
        "fcm_token": "test_fcm_token_12345",
        "user_id": "test_user_001"
    }
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200

def test_create_data_request():
    """데이터 요청 생성 테스트"""
    print("\n=== 2. 데이터 요청 생성 테스트 ===")
    url = f"{BASE_URL}/health/data/request"
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    data = {
        "device_id": "test_device_001",
        "data_types": ["steps", "heart_rate", "sleep"],
        "start_date": start_date,
        "end_date": end_date
    }
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        return response.json().get("request_id")
    return None

def test_get_request_status(request_id):
    """요청 상태 조회 테스트"""
    print(f"\n=== 3. 요청 상태 조회 테스트 (request_id: {request_id}) ===")
    url = f"{BASE_URL}/health/data/request/{request_id}"
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200

def test_receive_data_response(request_id):
    """데이터 응답 수신 테스트 (안드로이드에서 보낼 데이터 시뮬레이션)"""
    print(f"\n=== 4. 데이터 응답 수신 테스트 (request_id: {request_id}) ===")
    url = f"{BASE_URL}/health/data/response"
    
    data = {
        "request_id": request_id,
        "device_id": "test_device_001",
        "timestamp": datetime.now().isoformat() + "Z",
        "data": {
            "steps": [
                {"date": "2025-12-10", "count": 8500, "source": "samsung_health"},
                {"date": "2025-12-09", "count": 7200, "source": "google_fit"}
            ],
            "heart_rate": [
                {"timestamp": "2025-12-10T12:30:00Z", "bpm": 72},
                {"timestamp": "2025-12-10T18:00:00Z", "bpm": 85}
            ],
            "sleep": [
                {
                    "date": "2025-12-10",
                    "start_time": "2025-12-09T23:00:00Z",
                    "end_time": "2025-12-10T06:30:00Z",
                    "hours": 7.5
                }
            ]
        }
    }
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200

if __name__ == "__main__":
    print("FCM API 테스트 시작")
    print("=" * 50)
    
    try:
        # 1. 디바이스 등록
        if not test_register_device():
            print("디바이스 등록 실패")
            exit(1)
        
        # 2. 데이터 요청 생성
        request_id = test_create_data_request()
        if not request_id:
            print("데이터 요청 생성 실패")
            exit(1)
        
        # 3. 요청 상태 조회
        test_get_request_status(request_id)
        
        # 4. 데이터 응답 수신 (안드로이드 시뮬레이션)
        test_receive_data_response(request_id)
        
        # 5. 최종 상태 확인
        print("\n=== 5. 최종 요청 상태 확인 ===")
        test_get_request_status(request_id)
        
        print("\n" + "=" * 50)
        print("모든 테스트 완료!")
        
    except requests.exceptions.ConnectionError:
        print("\n오류: 서버에 연결할 수 없습니다.")
        print("서버가 실행 중인지 확인하세요: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()

