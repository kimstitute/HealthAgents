import logging
from fastapi import APIRouter, HTTPException
from app.schemas.health_data import HealthDataRequest, HealthDataResponse
from app.services import device_service
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.post("/data", response_model=HealthDataResponse)
async def receive_health_data(request: HealthDataRequest):
    """
    안드로이드로부터 직접 받은 건강 데이터 저장
    
    FCM 플로우가 아닌 직접 전송 방식도 지원합니다.
    """
    try:
        logger.info(f"Received health data from user: {request.user_id}, device: {request.device_id}")
        logger.debug(f"Health data: steps={request.steps}, heart_rate={request.heart_rate}, sleep={request.sleep}, calories={request.calories}")
        
        from app.schemas.fcm_data import (
            RequestedHealthData,
            DailyStepsData,
            HeartRateDataPoint,
            SleepDataPoint
        )
        
        requested_data = RequestedHealthData()
        
        if request.steps:
            requested_data.steps = [
                DailyStepsData(
                    date=request.steps.date,
                    count=request.steps.count
                )
            ]
        
        if request.heart_rate:
            requested_data.heart_rate = [
                HeartRateDataPoint(
                    timestamp=request.heart_rate.timestamp,
                    bpm=request.heart_rate.bpm
                )
            ]
        
        if request.sleep:
            sleep_date = request.sleep.start_time.split('T')[0] if request.sleep.start_time else datetime.utcnow().strftime('%Y-%m-%d')
            requested_data.sleep = [
                SleepDataPoint(
                    date=sleep_date,
                    start_time=request.sleep.start_time,
                    end_time=request.sleep.end_time,
                    hours=request.sleep.hours
                )
            ]
        
        if request.calories:
            requested_data.calories = [
                {
                    "date": request.calories.date,
                    "active": request.calories.active
                }
            ]
        
        request_id = f"direct_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{request.device_id[:8] if request.device_id else 'unknown'}"
        
        device_service.save_data_response(
            request_id=request_id,
            response_data=requested_data.model_dump()
        )
        
        if request.device_id:
            fake_request = {
                "request_id": request_id,
                "device_id": request.device_id,
                "data_types": [],
                "start_date": "",
                "end_date": "",
                "status": "completed",
                "created_at": datetime.utcnow().isoformat(),
                "completed_at": datetime.utcnow().isoformat(),
                "error_message": None
            }
            from app.services.device_service import _data_requests
            _data_requests[request_id] = fake_request
        
        logger.info(f"Health data saved with request_id: {request_id}")
        
        return HealthDataResponse(
            status="success",
            message="Data received and saved"
        )
    except Exception as e:
        logger.error("Error receiving health data", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error receiving health data: {e}")

