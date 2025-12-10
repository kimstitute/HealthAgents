import logging
from typing import Optional
from app.schemas.fcm_data import RequestedHealthData
from app.services import device_service

logger = logging.getLogger(__name__)


def get_latest_health_data_by_device(device_id: str) -> Optional[RequestedHealthData]:
    """
    특정 device_id의 최근 건강 데이터를 조회합니다.
    현재는 메모리 기반이므로 모든 응답을 확인합니다.
    
    Args:
        device_id: 기기 ID
    
    Returns:
        최근 건강 데이터 또는 None
    """
    try:
        from app.services.device_service import _data_responses
        
        latest_response = None
        latest_timestamp = None
        
        for request_id, response_data in _data_responses.items():
            if response_data.get("data"):
                request = device_service.get_data_request(request_id)
                if request and request.get("device_id") == device_id:
                    received_at = response_data.get("received_at")
                    if not latest_timestamp or (received_at and received_at > latest_timestamp):
                        latest_timestamp = received_at
                        latest_response = response_data
        
        if latest_response:
            data = latest_response.get("data")
            if data:
                try:
                    return RequestedHealthData(**data)
                except Exception as e:
                    logger.error(f"Failed to parse health data: {e}", exc_info=True)
                    return None
        
        logger.warning(f"No health data found for device: {device_id}")
        return None
    except Exception as e:
        logger.error(f"Failed to get health data by device: {e}", exc_info=True)
        return None


def get_latest_health_data() -> Optional[RequestedHealthData]:
    """
    가장 최근 건강 데이터를 조회합니다 (단일 사용자 시스템용).
    device_id 구분 없이 가장 최근 데이터를 반환합니다.
    
    Returns:
        최근 건강 데이터 또는 None
    """
    try:
        from app.services.device_service import _data_responses
        
        if not _data_responses:
            logger.warning("No health data responses found")
            return None
        
        latest_response = None
        latest_timestamp = None
        
        for request_id, response_data in _data_responses.items():
            if response_data.get("data"):
                received_at = response_data.get("received_at")
                if not latest_timestamp or (received_at and received_at > latest_timestamp):
                    latest_timestamp = received_at
                    latest_response = response_data
        
        if latest_response:
            data = latest_response.get("data")
            if data:
                try:
                    return RequestedHealthData(**data)
                except Exception as e:
                    logger.error(f"Failed to parse health data: {e}", exc_info=True)
                    return None
        
        logger.warning("No valid health data found")
        return None
    except Exception as e:
        logger.error(f"Failed to get latest health data: {e}", exc_info=True)
        return None

