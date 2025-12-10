import logging
from typing import Optional, Dict, Any
from app.schemas.user_data import PlanRequest

logger = logging.getLogger(__name__)

_user_sessions: Dict[str, Dict[str, Any]] = {}


def save_user_session(session_id: str, plan_request: PlanRequest) -> bool:
    """
    사용자 세션 정보 저장
    
    Args:
        session_id: 세션 ID
        plan_request: 사용자 정보 요청
    
    Returns:
        저장 성공 여부
    """
    try:
        _user_sessions[session_id] = {
            "user_name": plan_request.user_name,
            "basic_info": plan_request.basicInfo.model_dump(),
            "lifestyle": plan_request.lifestyle.model_dump(),
            "followup": plan_request.followup.model_dump(),
            "device_id": plan_request.device_id,
        }
        logger.info(f"User session saved: {session_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to save user session: {e}", exc_info=True)
        return False


def get_user_session(session_id: str) -> Optional[Dict[str, Any]]:
    """
    사용자 세션 정보 조회
    
    Args:
        session_id: 세션 ID
    
    Returns:
        세션 정보 또는 None
    """
    return _user_sessions.get(session_id)


def get_user_session_by_device(device_id: str) -> Optional[Dict[str, Any]]:
    """
    device_id로 사용자 세션 정보 조회
    
    Args:
        device_id: 기기 ID
    
    Returns:
        세션 정보 또는 None
    """
    for session_id, session_data in _user_sessions.items():
        if session_data.get("device_id") == device_id:
            return session_data
    return None


def get_user_session_by_name(user_name: str) -> Optional[Dict[str, Any]]:
    """
    user_name으로 사용자 세션 정보 조회 (device_id 없을 때 사용)
    
    Args:
        user_name: 사용자 이름
    
    Returns:
        가장 최근 세션 정보 또는 None
    """
    matching_sessions = []
    for session_id, session_data in _user_sessions.items():
        if session_data.get("user_name") == user_name:
            matching_sessions.append((session_id, session_data))
    
    if matching_sessions:
        return matching_sessions[-1][1]
    return None


def get_latest_user_session() -> Optional[Dict[str, Any]]:
    """
    가장 최근 사용자 세션 정보 조회 (단일 사용자 시스템용)
    
    Returns:
        가장 최근 세션 정보 또는 None
    """
    if not _user_sessions:
        return None
    
    latest_session = max(_user_sessions.items(), key=lambda x: x[0])
    return latest_session[1]


def generate_session_id(user_name: str, device_id: Optional[str] = None) -> str:
    """
    세션 ID 생성
    
    Args:
        user_name: 사용자 이름
        device_id: 기기 ID (선택)
    
    Returns:
        세션 ID
    """
    import hashlib
    from datetime import datetime
    
    key = f"{user_name}_{device_id or ''}_{datetime.utcnow().isoformat()}"
    return hashlib.md5(key.encode()).hexdigest()[:16]

