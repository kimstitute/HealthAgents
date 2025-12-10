import logging
import json
from app.agents.health_state import HealthState
from app.agents.prompts import AgentPrompts
from app.agents.utils.data_formatter import format_health_analysis_for_llm
from app.agents.health_tools import HEALTH_TOOLS
from langchain_core.messages import SystemMessage, HumanMessage
from app.schemas.agent_data import AnalysisResult

logger = logging.getLogger(__name__)


def create_analysis_agent(llm):
    """
    Analysis Agent 노드 생성
    
    HealthAnalysis를 받아 LLM으로 종합 분석을 수행합니다.
    Tools를 사용하여 필요한 정보를 조회할 수 있습니다.
    """
    llm_with_tools = llm.bind_tools(HEALTH_TOOLS)
    
    def analysis_agent(state: HealthState) -> HealthState:
        logger.info("Analysis Agent started")
        
        health_analysis = state.get("health_analysis")
        if not health_analysis:
            logger.warning("No health_analysis in state")
            return {
                "analysis_result": AnalysisResult(
                    summary="건강 데이터 분석 결과가 없습니다.",
                    insights=[],
                    recommendations=[],
                    concerns=[]
                )
            }
        
        messages = state.get("messages", [])
        user_message = messages[-1].content if messages else ""
        
        try:
            formatted_analysis = format_health_analysis_for_llm(health_analysis)
            
            user_info_parts = []
            basic_info = state.get("basic_info")
            lifestyle = state.get("lifestyle")
            followup_answers = state.get("followup_answers")
            
            if basic_info:
                user_info_parts.append(f"기본 정보: {basic_info.age}세 {basic_info.gender}, {basic_info.height}cm, {basic_info.weight}kg")
                user_info_parts.append(f"목표: {basic_info.period}주 동안 {basic_info.targetLoss}kg 감량")
            
            if lifestyle:
                user_info_parts.append(f"운동 빈도: 주 {lifestyle.exerciseFreq}회")
                user_info_parts.append(f"식사 패턴: 하루 {lifestyle.mealsPerDay}회, 야식 {lifestyle.nightSnackFreq}, 외식 {lifestyle.eatingOutFreq}")
                if lifestyle.healthNotes:
                    user_info_parts.append(f"건강 특이사항: {lifestyle.healthNotes}")
            
            if followup_answers:
                user_info_parts.append(f"추가 정보:")
                user_info_parts.append(f"- 식습관 목표: {followup_answers.q1}")
                user_info_parts.append(f"- 운동 선호도: {followup_answers.q2}")
                user_info_parts.append(f"- 절대 포기할 수 없는 부분: {followup_answers.q3}")
            
            user_info = "\n".join(user_info_parts) if user_info_parts else "사용자 정보 없음"
            
            system_prompt = AgentPrompts.ANALYSIS_AGENT_SYSTEM.format(
                user_info=user_info,
                health_analysis=formatted_analysis,
                user_message=user_message
            )
            
            messages_to_send = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = llm_with_tools.invoke(messages_to_send)
            
            tool_calls = response.tool_calls if hasattr(response, 'tool_calls') else []
            tool_results = []
            
            for tool_call in tool_calls:
                tool_name = tool_call.get("name", "")
                tool_args = tool_call.get("args", {})
                
                if tool_name == "get_health_analysis_summary":
                    from app.agents.health_tools import get_health_analysis_summary
                    result = get_health_analysis_summary.invoke(health_analysis)
                    tool_results.append({
                        "tool": tool_name,
                        "result": result
                    })
                elif tool_name == "get_anomalies":
                    from app.agents.health_tools import get_anomalies
                    result = get_anomalies.invoke(health_analysis)
                    tool_results.append({
                        "tool": tool_name,
                        "result": result
                    })
                elif tool_name == "get_trends":
                    from app.agents.health_tools import get_trends
                    result = get_trends.invoke(health_analysis)
                    tool_results.append({
                        "tool": tool_name,
                        "result": result
                    })
            
            if tool_results:
                logger.debug(f"Tool results: {tool_results}")
                tool_context = "\n".join([f"{tr['tool']}: {tr['result']}" for tr in tool_results])
                follow_up_prompt = f"도구 실행 결과:\n{tool_context}\n\n위 정보를 참고하여 최종 분석을 완성하세요."
                final_response = llm.invoke([
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_message),
                    response,
                    HumanMessage(content=follow_up_prompt)
                ])
                analysis_text = final_response.content
            else:
                analysis_text = response.content
            
            analysis_result = AnalysisResult(
                summary=analysis_text,
                insights=[],
                recommendations=[],
                concerns=[]
            )
            
            logger.info("Analysis Agent completed")
            return {
                "messages": [response],
                "analysis_result": analysis_result
            }
            
        except Exception as e:
            logger.error(f"Error in analysis agent: {e}", exc_info=True)
            return {
                "analysis_result": AnalysisResult(
                    summary=f"분석 중 오류가 발생했습니다: {str(e)}",
                    insights=[],
                    recommendations=[],
                    concerns=[]
                )
            }
    
    return analysis_agent

