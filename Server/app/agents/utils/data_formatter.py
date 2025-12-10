import logging
from typing import Optional, List, Dict, Any
from app.schemas.fcm_data import (
    RequestedHealthData,
    DailyStepsData,
    HeartRateDataPoint,
    SleepDataPoint
)
from app.schemas.agent_data import (
    HealthAnalysis,
    StepsSummary,
    HeartRateSummary,
    SleepSummary,
    Anomaly,
    Trend
)

logger = logging.getLogger(__name__)


def filter_data_by_date(data: RequestedHealthData, target_date: str = "2025-12-10") -> RequestedHealthData:
    """
    12월 10일 데이터만 필터링
    
    Args:
        data: 원본 건강 데이터
        target_date: 필터링할 날짜 (기본값: 2025-12-10)
    
    Returns:
        필터링된 건강 데이터
    """
    filtered = RequestedHealthData()
    
    if data.steps:
        filtered.steps = [s for s in data.steps if s.date == target_date]
    
    if data.heart_rate:
        filtered.heart_rate = [
            hr for hr in data.heart_rate 
            if hr.timestamp.startswith(target_date)
        ]
    
    if data.sleep:
        filtered.sleep = [s for s in data.sleep if s.date == target_date]
    
    if data.weight:
        filtered.weight = [w for w in data.weight if w.date == target_date]
    
    return filtered


def analyze_steps(steps_data: Optional[List[DailyStepsData]]) -> Optional[StepsSummary]:
    """걸음 수 데이터 분석"""
    if not steps_data or len(steps_data) == 0:
        return None
    
    counts = [s.count for s in steps_data]
    total = sum(counts)
    average = total / len(counts) if counts else 0
    
    goal = 10000
    goal_achievement = (average / goal) if goal > 0 else 0
    
    trend = "stable"
    if len(counts) >= 2:
        if counts[-1] > counts[0] * 1.1:
            trend = "increasing"
        elif counts[-1] < counts[0] * 0.9:
            trend = "decreasing"
    
    anomaly_days = []
    if len(counts) > 1:
        mean = average
        std = (sum((x - mean) ** 2 for x in counts) / len(counts)) ** 0.5
        for i, count in enumerate(counts):
            if count < mean - 2 * std:
                anomaly_days.append(steps_data[i].date)
    
    return StepsSummary(
        total=total,
        average=round(average, 1),
        days_with_data=len(steps_data),
        trend=trend,
        goal_achievement=round(goal_achievement, 2),
        anomaly_days=anomaly_days
    )


def analyze_heart_rate(heart_rate_data: Optional[List[HeartRateDataPoint]]) -> Optional[HeartRateSummary]:
    """심박수 데이터 분석"""
    if not heart_rate_data or len(heart_rate_data) == 0:
        return None
    
    bpms = [hr.bpm for hr in heart_rate_data]
    average = sum(bpms) / len(bpms)
    max_bpm = max(bpms)
    min_bpm = min(bpms)
    
    resting_threshold = 100
    resting_bpms = [bpm for bpm in bpms if bpm < resting_threshold]
    active_bpms = [bpm for bpm in bpms if bpm >= resting_threshold]
    
    resting_avg = sum(resting_bpms) / len(resting_bpms) if resting_bpms else average
    active_avg = sum(active_bpms) / len(active_bpms) if active_bpms else average
    
    variability = "normal"
    if len(bpms) > 1:
        std = (sum((x - average) ** 2 for x in bpms) / len(bpms)) ** 0.5
        if std > 30:
            variability = "high"
        elif std < 10:
            variability = "low"
    
    return HeartRateSummary(
        average=round(average, 1),
        max=max_bpm,
        min=min_bpm,
        resting_avg=round(resting_avg, 1),
        active_avg=round(active_avg, 1),
        variability=variability
    )


def analyze_sleep(sleep_data: Optional[List[SleepDataPoint]]) -> Optional[SleepSummary]:
    """수면 데이터 분석"""
    if not sleep_data or len(sleep_data) == 0:
        return None
    
    hours_list = [s.hours for s in sleep_data]
    average_hours = sum(hours_list) / len(hours_list)
    
    insufficient_threshold = 7.0
    insufficient_nights = sum(1 for h in hours_list if h < insufficient_threshold)
    
    consistency = 1.0
    if len(hours_list) > 1:
        mean = average_hours
        variance = sum((x - mean) ** 2 for x in hours_list) / len(hours_list)
        consistency = max(0, 1 - (variance / (mean ** 2)))
    
    return SleepSummary(
        average_hours=round(average_hours, 1),
        total_nights=len(sleep_data),
        consistency=round(consistency, 2),
        insufficient_nights=insufficient_nights
    )


def detect_anomalies(health_data: RequestedHealthData) -> List[Anomaly]:
    """이상 징후 탐지"""
    anomalies = []
    
    if health_data.steps:
        steps_summary = analyze_steps(health_data.steps)
        if steps_summary and steps_summary.get("anomaly_days"):
            for date in steps_summary["anomaly_days"]:
                step_data = next((s for s in health_data.steps if s.date == date), None)
                if step_data:
                    avg = steps_summary.get("average", 0)
                    deviation = ((step_data.count - avg) / avg * 100) if avg > 0 else 0
                    anomalies.append(Anomaly(
                        type="low_steps",
                        date=date,
                        severity="medium" if abs(deviation) < 50 else "high",
                        description=f"걸음 수가 평균보다 {abs(deviation):.1f}% {'낮음' if deviation < 0 else '높음'}"
                    ))
    
    if health_data.heart_rate:
        heart_rate_summary = analyze_heart_rate(health_data.heart_rate)
        if heart_rate_summary:
            max_bpm = heart_rate_summary.get("max", 0)
            if max_bpm > 180:
                anomalies.append(Anomaly(
                    type="high_heart_rate",
                    date="2025-12-10",
                    severity="high",
                    description=f"최고 심박수가 {max_bpm}bpm으로 매우 높음"
                ))
    
    if health_data.sleep:
        sleep_summary = analyze_sleep(health_data.sleep)
        if sleep_summary and sleep_summary.get("insufficient_nights", 0) > 0:
            anomalies.append(Anomaly(
                type="insufficient_sleep",
                date="2025-12-10",
                severity="medium",
                description=f"수면 시간이 부족함 (평균 {sleep_summary.get('average_hours', 0)}시간)"
            ))
    
    return anomalies


def analyze_trends(health_data: RequestedHealthData) -> List[Trend]:
    """트렌드 분석"""
    trends = []
    
    if health_data.steps and len(health_data.steps) >= 2:
        counts = [s.count for s in health_data.steps]
        if counts[-1] > counts[0]:
            change = ((counts[-1] - counts[0]) / counts[0] * 100) if counts[0] > 0 else 0
            trends.append(Trend(
                metric="steps",
                direction="increasing",
                change_percent=round(change, 1),
                period="day"
            ))
        elif counts[-1] < counts[0]:
            change = ((counts[0] - counts[-1]) / counts[0] * 100) if counts[0] > 0 else 0
            trends.append(Trend(
                metric="steps",
                direction="decreasing",
                change_percent=round(change, 1),
                period="day"
            ))
    
    return trends


def format_health_analysis_for_llm(health_analysis: Optional[HealthAnalysis]) -> str:
    """
    HealthAnalysis를 LLM에 전달할 형식으로 포맷팅
    
    원본 데이터가 아닌 구조화된 요약만 전달하여 토큰 절약
    """
    if not health_analysis:
        return "건강 데이터 분석 결과가 없습니다."
    
    lines = []
    
    if health_analysis.get("steps_summary"):
        ss = health_analysis["steps_summary"]
        lines.append("걸음 수 분석:")
        lines.append(f"- 총합: {ss.get('total', 0):,}보")
        lines.append(f"- 평균: {ss.get('average', 0):.1f}보")
        lines.append(f"- 트렌드: {ss.get('trend', 'stable')}")
        lines.append(f"- 목표 달성률: {ss.get('goal_achievement', 0) * 100:.0f}%")
        lines.append("")
    
    if health_analysis.get("heart_rate_summary"):
        hrs = health_analysis["heart_rate_summary"]
        lines.append("심박수 분석:")
        lines.append(f"- 평균: {hrs.get('average', 0):.1f}bpm")
        lines.append(f"- 최고: {hrs.get('max', 0)}bpm")
        lines.append(f"- 최저: {hrs.get('min', 0)}bpm")
        lines.append(f"- 안정 심박수: {hrs.get('resting_avg', 0):.1f}bpm")
        lines.append(f"- 활동 심박수: {hrs.get('active_avg', 0):.1f}bpm")
        lines.append(f"- 변동성: {hrs.get('variability', 'normal')}")
        lines.append("")
    
    if health_analysis.get("sleep_summary"):
        sls = health_analysis["sleep_summary"]
        lines.append("수면 분석:")
        lines.append(f"- 평균 수면 시간: {sls.get('average_hours', 0):.1f}시간")
        lines.append(f"- 수면 패턴 일정성: {sls.get('consistency', 0) * 100:.0f}%")
        lines.append(f"- 수면 부족한 날: {sls.get('insufficient_nights', 0)}일")
        lines.append("")
    
    if health_analysis.get("anomalies"):
        lines.append("이상 징후:")
        for anomaly in health_analysis["anomalies"]:
            lines.append(f"- {anomaly.get('date')}: {anomaly.get('description')} ({anomaly.get('severity')} 심각도)")
        lines.append("")
    
    if health_analysis.get("trends"):
        lines.append("트렌드:")
        for trend in health_analysis["trends"]:
            lines.append(f"- {trend.get('metric')}: {trend.get('direction')} ({trend.get('change_percent', 0):.1f}% 변화)")
    
    return "\n".join(lines)

