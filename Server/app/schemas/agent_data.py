from typing import TypedDict, Optional, List, Dict, Any

class StepsSummary(TypedDict, total=False):
    total: int
    average: float
    days_with_data: int
    trend: str
    goal_achievement: float
    anomaly_days: List[str]

class HeartRateSummary(TypedDict, total=False):
    average: float
    max: int
    min: int
    resting_avg: float
    active_avg: float
    variability: str

class SleepSummary(TypedDict, total=False):
    average_hours: float
    total_nights: int
    consistency: float
    insufficient_nights: int

class Anomaly(TypedDict, total=False):
    type: str
    date: str
    severity: str
    description: str

class Trend(TypedDict, total=False):
    metric: str
    direction: str
    change_percent: float
    period: str

class HealthAnalysis(TypedDict, total=False):
    steps_summary: Optional[StepsSummary]
    heart_rate_summary: Optional[HeartRateSummary]
    sleep_summary: Optional[SleepSummary]
    anomalies: List[Anomaly]
    trends: List[Trend]

class AnalysisResult(TypedDict, total=False):
    summary: str
    insights: List[str]
    recommendations: List[str]
    concerns: List[str]

