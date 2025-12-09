import logging
from fastapi import APIRouter, HTTPException
from app.schemas.chat_data import (
    ChatRequest,
    ChatResponse,
    MarkdownBlock,
    ChartBlock,
    ChartData,
    TableBlock
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        blocks = [
            MarkdownBlock(
                content=f"**'{request.message}'**에 대한 분석 결과입니다.\n\n이번 주 평균 걸음 수는 **8,957보**로 목표 대비 89%를 달성했습니다."
            ),
            ChartBlock(
                chartType="bar",
                title="일별 걸음 수",
                data=ChartData(
                    labels=["월", "화", "수", "목", "금", "토", "일"],
                    values=[8500, 7200, 9100, 6800, 10200, 12000, 8900]
                ),
                description="수요일과 토요일에 활동량이 높았습니다."
            ),
            TableBlock(
                title="주간 요약",
                headers=["항목", "값", "목표", "달성률"],
                rows=[
                    ["평균 걸음 수", "8,957보", "10,000보", "89%"],
                    ["평균 수면", "7.2시간", "8시간", "90%"],
                    ["평균 심박수", "72bpm", "-", "정상"]
                ]
            ),
            MarkdownBlock(
                content="목요일 활동량이 다소 부족했어요. 내일은 점심 산책 어떠세요?"
            )
        ]

        return ChatResponse(blocks=blocks)
    except Exception as e:
        logger.error("Error processing chat", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing chat: {e}")
