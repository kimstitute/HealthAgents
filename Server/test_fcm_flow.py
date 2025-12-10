import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_fcm_flow():
    """FCM 방식 데이터 요청 플로우 테스트"""
    print_section("FCM 방식 데이터 요청 테스트")
    
    # 서버 연결 확인
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code != 200:
            print("❌ 서버에 연결할 수 없습니다.")
            return
    except:
        print("❌ 서버에 연결할 수 없습니다.")
        print("서버가 실행 중인지 확인하세요.")
        return
    
    print("✅ 서버 연결 성공\n")
    
    # 디바이스 정보 입력
    device_id = input("Device ID를 입력하세요: ").strip()
    if not device_id:
        print("❌ Device ID는 필수입니다.")
        return
    
    fcm_token = input("FCM 토큰을 입력하세요 (선택사항, Enter로 건너뛰기): ").strip()
    user_id = input("User ID (선택사항, Enter로 건너뛰기): ").strip() or None
    
    # FCM 토큰이 있으면 디바이스 등록
    if fcm_token:
        print("\n[Step 1] 디바이스 등록")
        print("-" * 60)
        response = requests.post(
            f"{BASE_URL}/devices/register",
            json={
                "device_id": device_id,
                "fcm_token": fcm_token,
                "user_id": user_id
            }
        )
        if response.status_code == 200:
            print("✅ 디바이스 등록 성공")
        else:
            print(f"⚠️ 디바이스 등록 실패: {response.text}")
    else:
        print("\n⚠️ FCM 토큰이 없어 디바이스 등록을 건너뜁니다.")
        print("   (FCM 토큰 없이도 요청은 생성되지만 FCM 전송은 실패합니다)")
    
    # 데이터 요청 생성
    print("\n[Step 2] 데이터 요청 생성")
    print("-" * 60)
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    request_data = {
        "device_id": device_id,
        "data_types": ["steps", "heart_rate", "sleep"],
        "start_date": start_date,
        "end_date": end_date
    }
    
    print(f"요청 정보:")
    print(f"  - Device ID: {device_id}")
    print(f"  - 기간: {start_date} ~ {end_date}")
    print(f"  - 데이터 타입: {request_data['data_types']}")
    
    response = requests.post(f"{BASE_URL}/health/data/request", json=request_data)
    
    if response.status_code != 200:
        print(f"\n❌ 요청 생성 실패: {response.text}")
        return
    
    result = response.json()
    request_id = result.get("request_id")
    
    print(f"\n✅ 요청 생성 성공")
    print(f"   Request ID: {request_id}")
    print(f"   상태: {result.get('status')}")
    print(f"   메시지: {result.get('message')}")
    
    # 요청 상태 확인
    print("\n[Step 3] 요청 상태 확인")
    print("-" * 60)
    
    response = requests.get(f"{BASE_URL}/health/data/request/{request_id}")
    if response.status_code == 200:
        status_info = response.json()
        print(f"요청 상태: {status_info['status']}")
        print(f"생성 시각: {status_info['created_at']}")
        if status_info.get('error_message'):
            print(f"⚠️ 에러 메시지: {status_info['error_message']}")
    
    # 안드로이드 앱 확인 안내
    print("\n[Step 4] 안드로이드 앱 확인")
    print("-" * 60)
    print("안드로이드 앱에서 다음을 확인하세요:")
    print("  1. FCM 알림 수신 여부")
    print("  2. Health Connect 데이터 조회")
    print("  3. 백엔드로 데이터 전송")
    
    input("\n안드로이드 앱에서 데이터 전송을 완료한 후 Enter를 누르세요...")
    
    # 최종 상태 확인
    print("\n[Step 5] 최종 상태 확인")
    print("-" * 60)
    
    response = requests.get(f"{BASE_URL}/health/data/request/{request_id}")
    if response.status_code == 200:
        status_info = response.json()
        print(f"요청 상태: {status_info['status']}")
        print(f"생성 시각: {status_info['created_at']}")
        if status_info.get('completed_at'):
            print(f"완료 시각: {status_info['completed_at']}")
        if status_info.get('error_message'):
            print(f"에러 메시지: {status_info['error_message']}")
        
        print(f"\n전체 응답:")
        print(json.dumps(status_info, indent=2, ensure_ascii=False))
        
        if status_info['status'] == 'completed':
            print("\n✅ 통합 테스트 성공!")
        else:
            print(f"\n⚠️ 요청 상태: {status_info['status']}")
            print("   안드로이드 앱 로그를 확인하세요.")
    else:
        print(f"❌ 상태 조회 실패: {response.text}")

if __name__ == "__main__":
    test_fcm_flow()

