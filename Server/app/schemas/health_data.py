from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StepsData(BaseModel):
    count: int = Field(..., description="걸음 수")
    date: str = Field(..., description="날짜 (YYYY-MM-DD)")


class HeartRateData(BaseModel):
    bpm: int = Field(..., description="심박수 (bpm)")
    timestamp: str = Field(..., description="측정 시각 (ISO 8601)")


class SleepData(BaseModel):
    hours: float = Field(..., description="수면 시간 (시간)")
    start_time: str = Field(..., description="수면 시작 시각 (ISO 8601)")
    end_time: str = Field(..., description="수면 종료 시각 (ISO 8601)")


class CaloriesData(BaseModel):
    active: int = Field(..., description="활동 칼로리")
    date: str = Field(..., description="날짜 (YYYY-MM-DD)")


class HealthDataRequest(BaseModel):
    user_id: str = Field(..., description="사용자 ID")
    device_id: str = Field(..., description="기기 ID")
    timestamp: str = Field(..., description="데이터 수집 시각 (ISO 8601)")
    steps: Optional[StepsData] = Field(None, description="걸음 수 데이터")
    heart_rate: Optional[HeartRateData] = Field(None, description="심박수 데이터")
    sleep: Optional[SleepData] = Field(None, description="수면 데이터")
    calories: Optional[CaloriesData] = Field(None, description="칼로리 데이터")


class HealthDataResponse(BaseModel):
    status: str = Field(..., description="상태")
    message: str = Field(..., description="메시지")

