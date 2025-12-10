import logging
from typing import Optional
from datetime import datetime
from app.services.fcm_service import send_data_request_notification, initialize_fcm

logger = logging.getLogger(__name__)

initialize_fcm()

_device_tokens: dict[str, dict] = {}
_data_requests: dict[str, dict] = {}
_data_responses: dict[str, dict] = {}


def register_device(device_id: str, fcm_token: str, user_id: Optional[str] = None) -> bool:
    """
    디바이스 FCM 토큰 등록
    
    Args:
        device_id: 기기 ID
        fcm_token: FCM 토큰
        user_id: 사용자 ID (선택)
    
    Returns:
        등록 성공 여부
    """
    try:
        _device_tokens[device_id] = {
            "fcm_token": fcm_token,
            "user_id": user_id,
            "last_active": datetime.utcnow().isoformat(),
            "created_at": _device_tokens.get(device_id, {}).get("created_at") or datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        logger.info(f"Device registered: {device_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to register device: {e}", exc_info=True)
        return False


def get_device_token(device_id: str) -> Optional[str]:
    """
    디바이스의 FCM 토큰 조회
    
    Args:
        device_id: 기기 ID
    
    Returns:
        FCM 토큰 또는 None
    """
    device = _device_tokens.get(device_id)
    if device:
        return device.get("fcm_token")
    return None


def create_data_request(
    device_id: str,
    data_types: list[str],
    start_date: str,
    end_date: str
) -> Optional[str]:
    """
    데이터 요청 생성 및 FCM 전송
    
    Args:
        device_id: 기기 ID
        data_types: 요청할 데이터 타입 목록
        start_date: 시작 날짜 (YYYY-MM-DD)
        end_date: 종료 날짜 (YYYY-MM-DD)
    
    Returns:
        요청 ID 또는 None (실패 시)
    """
    try:
        fcm_token = get_device_token(device_id)
        if not fcm_token:
            logger.error(f"Device token not found: {device_id}")
            return None

        request_id = f"req_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{device_id[:8]}"
        
        request_data = {
            "request_id": request_id,
            "device_id": device_id,
            "data_types": data_types,
            "start_date": start_date,
            "end_date": end_date,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
            "completed_at": None,
            "error_message": None
        }
        
        _data_requests[request_id] = request_data
        
        success = send_data_request_notification(
            fcm_token=fcm_token,
            request_id=request_id,
            data_types=data_types,
            start_date=start_date,
            end_date=end_date
        )
        
        if success:
            request_data["status"] = "sent"
            logger.info(f"Data request created and sent: {request_id}")
        else:
            request_data["status"] = "sent"
            request_data["error_message"] = "FCM send failed (but request created)"
            logger.warning(f"FCM send failed but request created: {request_id}")
        
        return request_id

    except Exception as e:
        logger.error(f"Failed to create data request: {e}", exc_info=True)
        return None


def get_data_request(request_id: str) -> Optional[dict]:
    """
    데이터 요청 조회
    
    Args:
        request_id: 요청 ID
    
    Returns:
        요청 데이터 또는 None
    """
    return _data_requests.get(request_id)


def update_data_request_status(
    request_id: str,
    status: str,
    error_message: Optional[str] = None
) -> bool:
    """
    데이터 요청 상태 업데이트
    
    Args:
        request_id: 요청 ID
        status: 새 상태
        error_message: 에러 메시지 (선택)
    
    Returns:
        업데이트 성공 여부
    """
    try:
        request = _data_requests.get(request_id)
        if not request:
            logger.error(f"Data request not found: {request_id}")
            return False
        
        request["status"] = status
        if status == "completed":
            request["completed_at"] = datetime.utcnow().isoformat()
        if error_message:
            request["error_message"] = error_message
        
        logger.info(f"Data request status updated: {request_id} -> {status}")
        return True
    except Exception as e:
        logger.error(f"Failed to update data request status: {e}", exc_info=True)
        return False


def save_data_response(request_id: str, response_data: dict) -> bool:
    """
    받은 데이터 응답 저장
    
    Args:
        request_id: 요청 ID
        response_data: 받은 데이터
    
    Returns:
        저장 성공 여부
    """
    try:
        _data_responses[request_id] = {
            "request_id": request_id,
            "data": response_data,
            "received_at": datetime.utcnow().isoformat()
        }
        logger.info(f"Data response saved for request: {request_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to save data response: {e}", exc_info=True)
        return False


def get_data_response(request_id: str) -> Optional[dict]:
    """
    저장된 데이터 응답 조회
    
    Args:
        request_id: 요청 ID
    
    Returns:
        저장된 데이터 응답 또는 None
    """
    return _data_responses.get(request_id)

