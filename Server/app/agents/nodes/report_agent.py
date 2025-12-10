from app.agents.health_state import HealthState
from app.agents.prompts import AgentPrompts
from app.agents.utils.data_formatter import format_health_analysis_for_llm
from app.schemas.chat_data import (
    MarkdownBlock,
    ChartBlock,
    TableBlock,
    ChartData
)
from app.schemas.agent_data import HealthAnalysis, AnalysisResult
from langchain_core.messages import SystemMessage, HumanMessage
import logging
import json

logger = logging.getLogger(__name__)


def create_chart_blocks(health_analysis: HealthAnalysis) -> list:
    """HealthAnalysis에서 ChartBlock 생성"""
    blocks = []
    
    if health_analysis.get("steps_summary"):
        ss = health_analysis["steps_summary"]
        blocks.append(ChartBlock(
            chartType="bar",
            title="걸음 수 (2025-12-10)",
            data=ChartData(
                labels=["걸음 수"],
                values=[float(ss.get("total", 0))]
            ),
            description=f"총 {ss.get('total', 0):,}보, 평균 {ss.get('average', 0):.0f}보"
        ))
    
    if health_analysis.get("heart_rate_summary"):
        hrs = health_analysis["heart_rate_summary"]
        blocks.append(ChartBlock(
            chartType="line",
            title="심박수 통계 (2025-12-10)",
            data=ChartData(
                labels=["평균", "최고", "최저", "안정", "활동"],
                values=[
                    float(hrs.get("average", 0)),
                    float(hrs.get("max", 0)),
                    float(hrs.get("min", 0)),
                    float(hrs.get("resting_avg", 0)),
                    float(hrs.get("active_avg", 0))
                ]
            ),
            description=f"평균 {hrs.get('average', 0):.0f}bpm"
        ))
    
    if health_analysis.get("sleep_summary"):
        sls = health_analysis["sleep_summary"]
        blocks.append(ChartBlock(
            chartType="doughnut",
            title="수면 시간 (2025-12-10)",
            data=ChartData(
                labels=["수면 시간"],
                values=[float(sls.get("average_hours", 0))]
            ),
            description=f"평균 {sls.get('average_hours', 0):.1f}시간"
        ))
    
    return blocks


def create_table_blocks(health_analysis: HealthAnalysis) -> list:
    """HealthAnalysis에서 TableBlock 생성"""
    blocks = []
    
    rows = []
    headers = ["항목", "값", "상태"]
    
    if health_analysis.get("steps_summary"):
        ss = health_analysis["steps_summary"]
        rows.append(["걸음 수 (평균)", f"{ss.get('average', 0):.0f}보", "정상" if ss.get('goal_achievement', 0) >= 0.8 else "부족"])
        rows.append(["목표 달성률", f"{ss.get('goal_achievement', 0) * 100:.0f}%", "정상" if ss.get('goal_achievement', 0) >= 0.8 else "부족"])
    
    if health_analysis.get("heart_rate_summary"):
        hrs = health_analysis["heart_rate_summary"]
        rows.append(["심박수 (평균)", f"{hrs.get('average', 0):.0f}bpm", "정상"])
        rows.append(["심박수 변동성", hrs.get('variability', 'normal'), "정상"])
    
    if health_analysis.get("sleep_summary"):
        sls = health_analysis["sleep_summary"]
        rows.append(["수면 시간 (평균)", f"{sls.get('average_hours', 0):.1f}시간", "정상" if sls.get('average_hours', 0) >= 7.0 else "부족"])
        rows.append(["수면 일정성", f"{sls.get('consistency', 0) * 100:.0f}%", "정상" if sls.get('consistency', 0) >= 0.7 else "불규칙"])
    
    if rows:
        blocks.append(TableBlock(
            title="건강 데이터 요약 (2025-12-10)",
            headers=headers,
            rows=rows
        ))
    
    return blocks


def create_report_agent(llm):
    def report_agent(state: HealthState) -> HealthState:
        logger.info("Report agent started")
        
        analysis_result = state.get("analysis_result")
        health_analysis = state.get("health_analysis")
        messages = state.get("messages", [])
        user_message = messages[0].content if messages else ""
        
        blocks = []
        llm_response = None
        
        try:
            if analysis_result and health_analysis:
                formatted_analysis = format_health_analysis_for_llm(health_analysis)
                
                system_prompt = AgentPrompts.REPORT_AGENT_SYSTEM_DETAILED.format(
                    analysis_result=analysis_result.get("summary", ""),
                    health_analysis=formatted_analysis,
                    user_message=user_message
                )
                
                llm_response = llm.invoke([
                    SystemMessage(content=system_prompt),
                    HumanMessage(content="분석 결과를 바탕으로 리포트 블록을 JSON 형식으로 생성하세요.")
                ])
                
                try:
                    response_json = json.loads(llm_response.content)
                    
                    if response_json.get("markdown"):
                        blocks.append(MarkdownBlock(content=response_json["markdown"]))
                    
                    if response_json.get("charts"):
                        for chart in response_json["charts"]:
                            blocks.append(ChartBlock(
                                chartType=chart.get("type", "bar"),
                                title=chart.get("title", ""),
                                data=ChartData(
                                    labels=chart.get("labels", []),
                                    values=chart.get("values", [])
                                ),
                                description=chart.get("description")
                            ))
                    
                    if response_json.get("tables"):
                        for table in response_json["tables"]:
                            blocks.append(TableBlock(
                                title=table.get("title", ""),
                                headers=table.get("headers", []),
                                rows=table.get("rows", [])
                            ))
                    
                    logger.info(f"LLM generated {len(blocks)} blocks")
                    
                except json.JSONDecodeError:
                    logger.warning("Failed to parse LLM JSON response, using fallback")
                    if analysis_result:
                        blocks.append(MarkdownBlock(content=analysis_result.get("summary", "")))
                    if health_analysis:
                        chart_blocks = create_chart_blocks(health_analysis)
                        blocks.extend(chart_blocks)
                        table_blocks = create_table_blocks(health_analysis)
                        blocks.extend(table_blocks)
            
            elif analysis_result:
                blocks.append(MarkdownBlock(content=analysis_result.get("summary", "")))
            
            elif health_analysis:
                chart_blocks = create_chart_blocks(health_analysis)
                blocks.extend(chart_blocks)
                table_blocks = create_table_blocks(health_analysis)
                blocks.extend(table_blocks)
            
            if not blocks:
                blocks.append(MarkdownBlock(content="분석 결과가 없습니다."))
            
            logger.info(f"Report agent completed: {len(blocks)} blocks created")
            
            result = {"blocks": blocks}
            if llm_response:
                result["messages"] = [llm_response]
            
            return result
            
        except Exception as e:
            logger.error(f"Error in report agent: {e}", exc_info=True)
            blocks = []
            if analysis_result:
                blocks.append(MarkdownBlock(content=analysis_result.get("summary", "분석 결과 처리 중 오류가 발생했습니다.")))
            else:
                blocks.append(MarkdownBlock(content="리포트 생성 중 오류가 발생했습니다."))
            
            return {"blocks": blocks}
    
    return report_agent 
