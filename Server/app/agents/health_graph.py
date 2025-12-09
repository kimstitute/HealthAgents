from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI 
from app.config import settings
from app.agents.health_state import HealthState
from app.agents.nodes.report_agent import create_report_agent


class HealthGraph:
    def __init__(self):
        self.config = settings 
        self.llm = self._init_llms() 
        self.graph = self._build_graph() 

    def _build_graph(self):
        graph = StateGraph(HealthState)
        report_node = create_report_agent(self.llm)
        graph.add_node("report", report_node)
        graph.add_edge(START, "report")
        graph.add_edge("report", END)
        
        return graph.compile()

    def _init_llms(self):
        llm = ChatOpenAI(
            model=self.config.llm_model,
            temperature=self.config.llm_temperature,
            api_key=self.config.openai_api_key
        )
        return llm

    def invoke(self, input_data):
        return self.graph.invoke(input_data)
