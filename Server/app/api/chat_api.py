import logging 
from fastapi import APIRouter, Depends, HTTPException 

logger = logging.getLogger(__name__) 

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/send_message")
async def send_message(message: str):
    try:
        pass
    except Exception as e:
        logger.error("Error sending message", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error sending message: {e}") 