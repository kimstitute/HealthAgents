import logging
import json
from app.agents.health_state import HealthState
from app.agents.prompts import AgentPrompts
from app.agents.utils.data_formatter import (
    filter_data_by_date,
    analyze_steps,
    analyze_heart_rate,
    analyze_sleep,
    detect_anomalies,
    analyze_trends,
    format_health_analysis_for_llm
)
from app.schemas.agent_data import HealthAnalysis
from langchain_core.messages import SystemMessage, HumanMessage

logger = logging.getLogger(__name__)


def create_health_agent(llm):
    """
    Health Agent 노드 생성
    
    건강 데이터를 계산하고, LLM으로 해석하여 구조화된 분석 결과를 생성합니다.
    """
    def health_agent(state: HealthState) -> HealthState:
        logger.info("Health Agent started")
        
        health_data = state.get("health_data")
        if not health_data:
            logger.warning("No health_data in state")
            return {"health_analysis": None}
        
        try:
            filtered_data = filter_data_by_date(health_data, target_date="2025-12-10")
            logger.info("Filtered data for 2025-12-10")
            
            steps_summary = analyze_steps(filtered_data.steps)
            heart_rate_summary = analyze_heart_rate(filtered_data.heart_rate)
            sleep_summary = analyze_sleep(filtered_data.sleep)
            
            anomalies = detect_anomalies(filtered_data)
            trends = analyze_trends(filtered_data)
            
            calculated_stats = {
                "steps": steps_summary,
                "heart_rate": heart_rate_summary,
                "sleep": sleep_summary,
                "anomalies": anomalies,
                "trends": trends
            }
            
            data_summary = format_health_analysis_for_llm(calculated_stats)
            
            system_prompt = AgentPrompts.HEALTH_AGENT_SYSTEM.format(
                calculated_stats=json.dumps(calculated_stats, ensure_ascii=False, indent=2),
                data_summary=data_summary
            )
            
            llm_response = llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content="계산된 통계를 바탕으로 구조화된 건강 분석 결과를 생성하세요.")
            ])
            
            health_analysis = HealthAnalysis(
                steps_summary=steps_summary,
                heart_rate_summary=heart_rate_summary,
                sleep_summary=sleep_summary,
                anomalies=anomalies,
                trends=trends
            )
            
            logger.info(f"Health analysis completed: steps={bool(steps_summary)}, heart_rate={bool(heart_rate_summary)}, sleep={bool(sleep_summary)}, anomalies={len(anomalies)}")
            logger.debug(f"LLM interpretation: {llm_response.content[:200]}...")
            
            return {
                "health_analysis": health_analysis,
                "messages": [llm_response]
            }
            
        except Exception as e:
            logger.error(f"Error in health agent: {e}", exc_info=True)
            return {"health_analysis": None}
    
    return health_agent

