from typing import Annotated, List, TypedDict, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages 
from app.schemas.chat_data import Block
from app.schemas.fcm_data import RequestedHealthData
from app.schemas.agent_data import HealthAnalysis, AnalysisResult
from app.schemas.user_data import BasicInfo, Lifestyle, FollowupAnswers

class HealthState(TypedDict, total=False):
    messages: Annotated[List[BaseMessage], add_messages]
    blocks: Annotated[List[Block], "response blocks"]
    
    user_id: Optional[str]
    user_name: Optional[str]
    device_id: Optional[str]
    
    basic_info: Optional[BasicInfo]
    lifestyle: Optional[Lifestyle]
    followup_answers: Optional[FollowupAnswers]
    
    health_data: Optional[RequestedHealthData]
    health_analysis: Optional[HealthAnalysis]
    analysis_result: Optional[AnalysisResult]
    block_drafts: Optional[List[dict]]
    
    intent: Optional[str]
    required_data_types: Optional[List[str]] 