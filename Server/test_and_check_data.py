import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"
DEVICE_ID = "547c177250466685"
FCM_TOKEN = "eCkBmt7CRqeFB-A0fvQ6EY:APA91bHBwaNU67NxZYVBrPS-o2DVUGUYlb9gOae2BKcjtu_psWeMU_fbHc_B5ieTJ0n15ZbXrFmbuDCPKQlKlG6ckwY3z-z3q9C7t_Zg4QiduPq69jaDXF4"

def test_and_check():
    print("=" * 60)
    print("데이터 요청 및 수신 확인")
    print("=" * 60)
    
    # 디바이스 등록
    print("\n[1] 디바이스 등록")
    requests.post(
        f"{BASE_URL}/devices/register",
        json={"device_id": DEVICE_ID, "fcm_token": FCM_TOKEN}
    )
    print("✅ 등록 완료")
    
    # 데이터 요청 생성
    print("\n[2] 데이터 요청 생성")
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    response = requests.post(
        f"{BASE_URL}/health/data/request",
        json={
            "device_id": DEVICE_ID,
            "data_types": ["steps", "heart_rate", "sleep"],
            "start_date": start_date,
            "end_date": end_date
        }
    )
    
    result = response.json()
    request_id = result["request_id"]
    print(f"✅ 요청 생성: {request_id}")
    print(f"   요청한 데이터: steps, heart_rate, sleep")
    print(f"   기간: {start_date} ~ {end_date}")
    
    # 완료 대기
    print("\n[3] 안드로이드 앱 응답 대기 중...")
    max_wait = 60
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        response = requests.get(f"{BASE_URL}/health/data/request/{request_id}")
        if response.status_code == 200:
            status = response.json()["status"]
            if status == "completed":
                print("✅ 데이터 수신 완료!")
                break
        time.sleep(2)
        elapsed = int(time.time() - start_time)
        print(f"\r대기 중... ({elapsed}초)", end="", flush=True)
    
    print("\n")
    
    # 받은 데이터 확인
    print("\n[4] 받은 데이터 확인")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/health/data/response/{request_id}")
    
    if response.status_code == 200:
        data_response = response.json()
        data = data_response['data']
        
        print(f"수신 시각: {data_response['received_at']}")
        print(f"\n받은 데이터 내용:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        print("\n[5] 데이터 요약")
        print("-" * 60)
        if data.get('steps'):
            print(f"✅ 걸음 수: {len(data['steps'])}개")
            for step in data['steps'][:5]:
                print(f"   - {step.get('date')}: {step.get('count')}보")
        else:
            print("❌ 걸음 수 데이터 없음")
            
        if data.get('heart_rate'):
            print(f"\n✅ 심박수: {len(data['heart_rate'])}개")
            for hr in data['heart_rate'][:5]:
                print(f"   - {hr.get('timestamp')}: {hr.get('bpm')}bpm")
        else:
            print("\n❌ 심박수 데이터 없음")
            
        if data.get('sleep'):
            print(f"\n✅ 수면: {len(data['sleep'])}개")
            for sleep in data['sleep'][:5]:
                print(f"   - {sleep.get('date')}: {sleep.get('hours')}시간")
        else:
            print("\n❌ 수면 데이터 없음")
            
        # 요청한 데이터와 비교
        print("\n[6] 요청 대비 확인")
        print("-" * 60)
        requested = ["steps", "heart_rate", "sleep"]
        received = []
        if data.get('steps'): received.append("steps")
        if data.get('heart_rate'): received.append("heart_rate")
        if data.get('sleep'): received.append("sleep")
        
        print(f"요청한 데이터: {requested}")
        print(f"받은 데이터: {received}")
        
        missing = set(requested) - set(received)
        if missing:
            print(f"⚠️ 누락된 데이터: {missing}")
        else:
            print("✅ 모든 요청한 데이터가 수신되었습니다!")
            
    else:
        print(f"❌ 데이터를 찾을 수 없습니다: {response.text}")

if __name__ == "__main__":
    try:
        test_and_check()
    except KeyboardInterrupt:
        print("\n\n테스트 중단")
    except Exception as e:
        print(f"\n오류: {e}")
        import traceback
        traceback.print_exc()

