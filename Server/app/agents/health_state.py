from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages 
from app.schemas.chat_data import Block

class HealthState(TypedDict, total=False):
    messages: Annotated[List[BaseMessage], add_messages]

    blocks: Annotated[List[Block], "response blocks"] 