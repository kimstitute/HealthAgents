from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum


class DataType(str, Enum):
    STEPS = "steps"
    HEART_RATE = "heart_rate"
    SLEEP = "sleep"
    CALORIES = "calories"
    WEIGHT = "weight"
    DISTANCE = "distance"


class RequestStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    COMPLETED = "completed"
    FAILED = "failed"


class DeviceRegisterRequest(BaseModel):
    device_id: str = Field(..., description="기기 ID")
    fcm_token: str = Field(..., description="FCM 토큰")
    user_id: Optional[str] = Field(None, description="사용자 ID")


class DeviceRegisterResponse(BaseModel):
    status: str = Field(..., description="상태")
    message: str = Field(..., description="메시지")


class DataRequestRequest(BaseModel):
    device_id: str = Field(..., description="기기 ID")
    data_types: List[str] = Field(..., description="요청할 데이터 타입 목록")
    start_date: str = Field(..., description="시작 날짜 (YYYY-MM-DD)")
    end_date: str = Field(..., description="종료 날짜 (YYYY-MM-DD)")


class DataRequestResponse(BaseModel):
    request_id: str = Field(..., description="요청 ID")
    status: str = Field(..., description="상태")
    message: str = Field(..., description="메시지")


class DailyStepsData(BaseModel):
    date: str = Field(..., description="날짜 (YYYY-MM-DD)")
    count: int = Field(..., description="걸음 수")
    source: Optional[str] = Field(None, description="데이터 소스")


class HeartRateDataPoint(BaseModel):
    timestamp: str = Field(..., description="측정 시각 (ISO 8601)")
    bpm: int = Field(..., description="심박수 (bpm)")


class SleepDataPoint(BaseModel):
    date: str = Field(..., description="날짜 (YYYY-MM-DD)")
    start_time: str = Field(..., description="수면 시작 시각 (ISO 8601)")
    end_time: str = Field(..., description="수면 종료 시각 (ISO 8601)")
    hours: float = Field(..., description="수면 시간 (시간)")


class WeightDataPoint(BaseModel):
    date: str = Field(..., description="날짜 (YYYY-MM-DD)")
    kg: float = Field(..., description="체중 (kg)")


class RequestedHealthData(BaseModel):
    steps: Optional[List[DailyStepsData]] = Field(None, description="걸음 수 데이터 목록")
    heart_rate: Optional[List[HeartRateDataPoint]] = Field(None, description="심박수 데이터 목록")
    sleep: Optional[List[SleepDataPoint]] = Field(None, description="수면 데이터 목록")
    weight: Optional[List[WeightDataPoint]] = Field(None, description="체중 데이터 목록")
    calories: Optional[List[dict]] = Field(None, description="칼로리 데이터 목록")
    distance: Optional[List[dict]] = Field(None, description="거리 데이터 목록")


class DataResponseRequest(BaseModel):
    request_id: str = Field(..., description="요청 ID")
    device_id: str = Field(..., description="기기 ID")
    timestamp: str = Field(..., description="응답 시각 (ISO 8601)")
    data: RequestedHealthData = Field(..., description="요청된 건강 데이터")


class DataResponseAck(BaseModel):
    status: str = Field(..., description="상태")
    message: str = Field(..., description="메시지")


class DataRequestStatusResponse(BaseModel):
    request_id: str = Field(..., description="요청 ID")
    device_id: str = Field(..., description="기기 ID")
    status: RequestStatus = Field(..., description="요청 상태")
    data_types: List[str] = Field(..., description="요청한 데이터 타입 목록")
    start_date: str = Field(..., description="시작 날짜")
    end_date: str = Field(..., description="종료 날짜")
    created_at: str = Field(..., description="생성 시각 (ISO 8601)")
    completed_at: Optional[str] = Field(None, description="완료 시각 (ISO 8601)")
    error_message: Optional[str] = Field(None, description="에러 메시지")

