import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

# 실제 디바이스 정보
DEVICE_ID = "547c177250466685"
FCM_TOKEN = "eCkBmt7CRqeFB-A0fvQ6EY:APA91bHBwaNU67NxZYVBrPS-o2DVUGUYlb9gOae2BKcjtu_psWeMU_fbHc_B5ieTJ0n15ZbXrFmbuDCPKQlKlG6ckwY3z-z3q9C7t_Zg4QiduPq69jaDXF4"

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_real_fcm():
    """실제 FCM 토큰으로 테스트"""
    print_section("실제 FCM 토큰 테스트")
    
    # 서버 연결 확인
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code != 200:
            print("❌ 서버에 연결할 수 없습니다.")
            return
    except Exception as e:
        print(f"❌ 서버에 연결할 수 없습니다: {e}")
        return
    
    print("✅ 서버 연결 성공")
    print(f"Device ID: {DEVICE_ID}")
    print(f"FCM Token: {FCM_TOKEN[:50]}...")
    
    # Step 1: 디바이스 등록
    print_section("Step 1: 디바이스 등록")
    response = requests.post(
        f"{BASE_URL}/devices/register",
        json={
            "device_id": DEVICE_ID,
            "fcm_token": FCM_TOKEN,
            "user_id": None
        }
    )
    
    if response.status_code == 200:
        print("✅ 디바이스 등록 성공")
        print(f"응답: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"❌ 디바이스 등록 실패: {response.status_code}")
        print(f"응답: {response.text}")
        return
    
    # Step 2: 데이터 요청 생성
    print_section("Step 2: 데이터 요청 생성")
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    request_data = {
        "device_id": DEVICE_ID,
        "data_types": ["steps", "heart_rate", "sleep"],
        "start_date": start_date,
        "end_date": end_date
    }
    
    print(f"요청 정보:")
    print(f"  - Device ID: {DEVICE_ID}")
    print(f"  - 기간: {start_date} ~ {end_date}")
    print(f"  - 데이터 타입: {request_data['data_types']}")
    
    response = requests.post(f"{BASE_URL}/health/data/request", json=request_data)
    
    if response.status_code != 200:
        print(f"❌ 요청 생성 실패: {response.status_code}")
        print(f"응답: {response.text}")
        return
    
    result = response.json()
    request_id = result.get("request_id")
    
    print(f"\n✅ 요청 생성 성공")
    print(f"   Request ID: {request_id}")
    print(f"   상태: {result.get('status')}")
    print(f"   메시지: {result.get('message')}")
    
    # Step 3: 요청 상태 확인 (즉시)
    print_section("Step 3: 요청 상태 확인 (즉시)")
    response = requests.get(f"{BASE_URL}/health/data/request/{request_id}")
    if response.status_code == 200:
        status_info = response.json()
        print(f"요청 상태: {status_info['status']}")
        print(f"생성 시각: {status_info['created_at']}")
        if status_info.get('error_message'):
            print(f"⚠️ 에러 메시지: {status_info['error_message']}")
    
    # Step 4: 안드로이드 앱 확인 안내
    print_section("Step 4: 안드로이드 앱 확인")
    print("📱 안드로이드 앱에서 다음을 확인하세요:")
    print("  1. FCM 알림 수신 여부")
    print("  2. Health Connect 데이터 조회")
    print("  3. 백엔드로 데이터 전송")
    print(f"\n⏳ 안드로이드 앱에서 데이터 전송을 완료할 때까지 대기 중...")
    print("   (최대 60초 대기, Ctrl+C로 중단 가능)")
    
    # Step 5: 요청 완료 대기
    print_section("Step 5: 요청 완료 대기")
    max_wait = 60
    start_time = time.time()
    check_interval = 3
    
    while time.time() - start_time < max_wait:
        response = requests.get(f"{BASE_URL}/health/data/request/{request_id}")
        if response.status_code == 200:
            status_info = response.json()
            current_status = status_info['status']
            
            if current_status == 'completed':
                print(f"\n✅ 요청이 완료되었습니다!")
                print(f"완료 시각: {status_info.get('completed_at')}")
                print(f"\n전체 응답:")
                print(json.dumps(status_info, indent=2, ensure_ascii=False))
                return
            elif current_status == 'failed':
                print(f"\n❌ 요청이 실패했습니다.")
                print(f"에러 메시지: {status_info.get('error_message')}")
                return
        
        elapsed = int(time.time() - start_time)
        print(f"\r대기 중... ({elapsed}초 / {max_wait}초)", end="", flush=True)
        time.sleep(check_interval)
    
    print(f"\n⏱️ 타임아웃: {max_wait}초 내에 요청이 완료되지 않았습니다.")
    print("안드로이드 앱 로그를 확인하세요.")
    
    # 최종 상태 확인
    response = requests.get(f"{BASE_URL}/health/data/request/{request_id}")
    if response.status_code == 200:
        status_info = response.json()
        print(f"\n최종 상태: {status_info['status']}")
        print(json.dumps(status_info, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    try:
        test_real_fcm()
    except KeyboardInterrupt:
        print("\n\n테스트가 중단되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()

