import logging
from fastapi import APIRouter, HTTPException
from app.schemas.health_data import HealthDataRequest, HealthDataResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.post("/data", response_model=HealthDataResponse)
async def receive_health_data(request: HealthDataRequest):
    try:
        logger.info(f"Received health data from user: {request.user_id}, device: {request.device_id}")
        logger.debug(f"Health data: steps={request.steps}, heart_rate={request.heart_rate}, sleep={request.sleep}, calories={request.calories}")
        
        return HealthDataResponse(
            status="success",
            message="Data received"
        )
    except Exception as e:
        logger.error("Error receiving health data", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error receiving health data: {e}")

