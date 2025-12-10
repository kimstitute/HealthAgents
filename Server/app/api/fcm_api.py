import logging
from fastapi import APIRouter, HTTPException
from app.schemas.fcm_data import (
    DeviceRegisterRequest,
    DeviceRegisterResponse,
    DataRequestRequest,
    DataRequestResponse,
    DataResponseRequest,
    DataResponseAck,
    DataRequestStatusResponse,
    RequestStatus
)
from app.services import device_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["devices", "health"])


@router.post("/devices/register", response_model=DeviceRegisterResponse)
async def register_device(request: DeviceRegisterRequest):
    """
    디바이스 FCM 토큰 등록
    """
    try:
        success = device_service.register_device(
            device_id=request.device_id,
            fcm_token=request.fcm_token,
            user_id=request.user_id
        )
        
        if success:
            return DeviceRegisterResponse(
                status="success",
                message="Device registered successfully"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to register device")
    except Exception as e:
        logger.error("Error registering device", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error registering device: {e}")


@router.post("/health/data/request", response_model=DataRequestResponse)
async def create_data_request(request: DataRequestRequest):
    """
    건강 데이터 요청 생성 및 FCM 전송
    """
    try:
        request_id = device_service.create_data_request(
            device_id=request.device_id,
            data_types=request.data_types,
            start_date=request.start_date,
            end_date=request.end_date
        )
        
        if request_id:
            return DataRequestResponse(
                request_id=request_id,
                status="sent",
                message="Request sent via FCM"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to create and send data request")
    except Exception as e:
        logger.error("Error creating data request", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error creating data request: {e}")


@router.post("/health/data/response", response_model=DataResponseAck)
async def receive_data_response(request: DataResponseRequest):
    """
    안드로이드로부터 받은 건강 데이터 응답 처리
    """
    try:
        data_request = device_service.get_data_request(request.request_id)
        if not data_request:
            raise HTTPException(status_code=404, detail="Data request not found")
        
        logger.info(f"Received data response for request: {request.request_id}")
        logger.info(f"Response data: {request.data}")
        
        device_service.save_data_response(
            request_id=request.request_id,
            response_data=request.data.dict()
        )
        
        device_service.update_data_request_status(
            request_id=request.request_id,
            status="completed"
        )
        
        return DataResponseAck(
            status="success",
            message="Data received successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error receiving data response", exc_info=True)
        device_service.update_data_request_status(
            request_id=request.request_id,
            status="failed",
            error_message=str(e)
        )
        raise HTTPException(status_code=500, detail=f"Error receiving data response: {e}")


@router.get("/health/data/request/{request_id}", response_model=DataRequestStatusResponse)
async def get_data_request_status(request_id: str):
    """
    데이터 요청 상태 조회
    """
    try:
        request = device_service.get_data_request(request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Data request not found")
        
        return DataRequestStatusResponse(
            request_id=request["request_id"],
            device_id=request["device_id"],
            status=RequestStatus(request["status"]),
            data_types=request["data_types"],
            start_date=request["start_date"],
            end_date=request["end_date"],
            created_at=request["created_at"],
            completed_at=request.get("completed_at"),
            error_message=request.get("error_message")
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting data request status", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error getting data request status: {e}")


@router.get("/health/data/response/{request_id}")
async def get_data_response(request_id: str):
    """
    받은 데이터 응답 조회
    """
    try:
        response = device_service.get_data_response(request_id)
        if not response:
            raise HTTPException(status_code=404, detail="Data response not found")
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting data response", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error getting data response: {e}")

