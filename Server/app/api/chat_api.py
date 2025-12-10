import logging
from fastapi import APIRouter, HTTPException, Request
from langchain_core.messages import HumanMessage
from app.schemas.chat_data import ChatRequest, ChatResponse
from app.schemas.user_data import PlanRequest, PlanResponse
from app.services.user_session_service import (
    save_user_session,
    get_user_session,
    get_user_session_by_device,
    get_latest_user_session,
    generate_session_id
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/plan/init", response_model=PlanResponse)
async def init_plan(request: PlanRequest, req: Request):
    """
    사용자 정보 초기화 및 세션 생성
    
    사전 질문 데이터를 받아 세션에 저장합니다.
    """
    try:
        session_id = generate_session_id(request.user_name, request.device_id)
        
        success = save_user_session(session_id, request)
        
        if success:
            logger.info(f"Plan initialized for user: {request.user_name}, session: {session_id}")
            return PlanResponse(
                status="success",
                message="사용자 정보가 저장되었습니다.",
                session_id=session_id
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to save user session")
            
    except Exception as e:
        logger.error("Error initializing plan", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error initializing plan: {e}")


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    try:
        health_graph = req.app.state.health_graph
        
        input_state = {
            "messages": [HumanMessage(content=request.message)]
        }
        
        user_session = None
        
        if request.device_id:
            input_state["device_id"] = request.device_id
            user_session = get_user_session_by_device(request.device_id)
            if user_session:
                logger.info(f"User session loaded by device_id: {request.device_id}")
        
        if not user_session:
            user_session = get_latest_user_session()
            if user_session:
                device_id = user_session.get("device_id")
                if device_id:
                    input_state["device_id"] = device_id
                logger.info("User session loaded (latest session, single user system)")
        
        if user_session:
            from app.schemas.user_data import BasicInfo, Lifestyle, FollowupAnswers
            
            input_state["user_name"] = user_session.get("user_name")
            input_state["basic_info"] = BasicInfo(**user_session.get("basic_info", {}))
            input_state["lifestyle"] = Lifestyle(**user_session.get("lifestyle", {}))
            input_state["followup_answers"] = FollowupAnswers(**user_session.get("followup", {}))
        
        result = health_graph.invoke(input_state)
        
        blocks = result.get("blocks", [])
        return ChatResponse(blocks=blocks)
    except Exception as e:
        logger.error("Error processing chat", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing chat: {e}")
