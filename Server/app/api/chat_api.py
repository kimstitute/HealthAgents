import logging
from fastapi import APIRouter, HTTPException, Request
from langchain_core.messages import HumanMessage
from app.schemas.chat_data import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    try:
        health_graph = req.app.state.health_graph
        result = health_graph.invoke({
            "messages": [HumanMessage(content=request.message)]
        })
        
        blocks = result.get("blocks", [])
        return ChatResponse(blocks=blocks)
    except Exception as e:
        logger.error("Error processing chat", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing chat: {e}")
