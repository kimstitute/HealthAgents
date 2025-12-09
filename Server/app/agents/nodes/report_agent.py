from app.agents.health_state import HealthState
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from app.schemas.chat_data import (
    ChatRequest,
    ChatResponse,
    MarkdownBlock,
    ChartBlock,
    TableBlock,
    ImageBlock
)
import logging

logger = logging.getLogger(__name__)


def create_report_agent(llm):
    def report_agent(state: HealthState) -> HealthState:
        logger.info("Report agent started")
        messages = state.get("messages", [])
        last_message = messages[-1]

        response = llm.invoke([last_message])

        blocks = [
            MarkdownBlock(content=response.content)
        ]

        return {
            "messages": [response],
            "blocks": blocks
        }
    
    return report_agent 
