from langchain_core.tools import tool
from typing import Optional, List, Dict, Any
from app.schemas.agent_data import HealthAnalysis, Anomaly


@tool
def get_health_analysis_summary(health_analysis: Dict[str, Any]) -> str:
    """
    건강 분석 결과의 요약을 반환합니다.
    
    Args:
        health_analysis: HealthAnalysis 딕셔너리
    
    Returns:
        요약 텍스트
    """
    summary_parts = []
    
    if health_analysis.get("steps_summary"):
        ss = health_analysis["steps_summary"]
        summary_parts.append(f"걸음 수: 평균 {ss.get('average', 0):.0f}보, 목표 달성률 {ss.get('goal_achievement', 0) * 100:.0f}%")
    
    if health_analysis.get("heart_rate_summary"):
        hrs = health_analysis["heart_rate_summary"]
        summary_parts.append(f"심박수: 평균 {hrs.get('average', 0):.0f}bpm")
    
    if health_analysis.get("sleep_summary"):
        sls = health_analysis["sleep_summary"]
        summary_parts.append(f"수면: 평균 {sls.get('average_hours', 0):.1f}시간")
    
    return " | ".join(summary_parts) if summary_parts else "분석 데이터 없음"


@tool
def get_anomalies(health_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    건강 분석 결과에서 이상 징후를 반환합니다.
    
    Args:
        health_analysis: HealthAnalysis 딕셔너리
    
    Returns:
        이상 징후 목록
    """
    anomalies = health_analysis.get("anomalies", [])
    return [
        {
            "type": a.get("type", ""),
            "date": a.get("date", ""),
            "severity": a.get("severity", ""),
            "description": a.get("description", "")
        }
        for a in anomalies
    ]


@tool
def get_trends(health_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    건강 분석 결과에서 트렌드를 반환합니다.
    
    Args:
        health_analysis: HealthAnalysis 딕셔너리
    
    Returns:
        트렌드 목록
    """
    trends = health_analysis.get("trends", [])
    return [
        {
            "metric": t.get("metric", ""),
            "direction": t.get("direction", ""),
            "change_percent": t.get("change_percent", 0),
            "period": t.get("period", "")
        }
        for t in trends
    ]


HEALTH_TOOLS = [
    get_health_analysis_summary,
    get_anomalies,
    get_trends,
]