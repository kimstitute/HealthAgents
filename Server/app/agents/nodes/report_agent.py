from app.agents.health_state import HealthState
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
import logging

logger = logging.getLogger(__name__)

def report_agent(state: HealthState) -> HealthState:
    pass