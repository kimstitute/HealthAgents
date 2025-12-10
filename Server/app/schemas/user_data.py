from pydantic import BaseModel, Field
from typing import Optional


class BasicInfo(BaseModel):
    age: str = Field(..., description="나이")
    gender: str = Field(..., description="성별")
    height: str = Field(..., description="키 (cm)")
    weight: str = Field(..., description="현재 체중 (kg)")
    period: str = Field(..., description="다이어트 기간 (주)")
    targetLoss: str = Field(..., description="목표 감량 체중 (kg)")


class Lifestyle(BaseModel):
    exerciseFreq: str = Field(..., description="운동 빈도")
    mealsPerDay: str = Field(..., description="하루 식사 횟수")
    nightSnackFreq: str = Field(..., description="야식 빈도")
    eatingOutFreq: str = Field(..., description="외식 빈도")
    healthNotes: Optional[str] = Field(None, description="건강 특이사항")


class FollowupAnswers(BaseModel):
    q1: str = Field(..., description="추가 질문 1 답변")
    q2: str = Field(..., description="추가 질문 2 답변")
    q3: str = Field(..., description="추가 질문 3 답변")


class PlanRequest(BaseModel):
    user_name: str = Field(..., description="사용자 이름")
    basicInfo: BasicInfo = Field(..., description="기본 정보")
    lifestyle: Lifestyle = Field(..., description="라이프스타일 정보")
    followup: FollowupAnswers = Field(..., description="추가 질문 답변")
    device_id: Optional[str] = Field(None, description="기기 ID (선택)")


class PlanResponse(BaseModel):
    status: str = Field(..., description="상태")
    message: str = Field(..., description="메시지")
    session_id: Optional[str] = Field(None, description="세션 ID")

