import logging
from app.agents.health_state import HealthState
from app.agents.prompts import AgentPrompts
from app.services.health_data_service import get_latest_health_data_by_device
from langchain_core.messages import SystemMessage, HumanMessage

logger = logging.getLogger(__name__)


def create_health_collector(llm):
    """
    Health Data Collector 노드 생성
    
    FCM으로 받은 건강 데이터를 HealthState에 주입하고, LLM으로 데이터 품질을 평가합니다.
    """
    COLLECTOR_SYSTEM = """
    당신은 건강 데이터 수집 전문가입니다.
    
    수집된 건강 데이터의 품질과 완전성을 평가하고 요약하세요.
    
    중요: 워치 결측값 문제로 인해 2025-12-10일 데이터만 유효합니다.
    다른 날짜의 데이터는 무시하세요.
    
    수집된 데이터:
    {collected_data}
    
    다음을 평가하세요:
    1. 데이터 완전성 (어떤 데이터가 있고 없는지)
    2. 데이터 품질 (결측값, 이상값)
    3. 분석 가능성 (충분한 데이터가 있는지)
    
    간단히 요약하세요 (2-3문장).
    """
    
    def health_collector(state: HealthState) -> HealthState:
        logger.info("Health Data Collector started")
        
        try:
            from app.services.health_data_service import get_latest_health_data
            
            device_id = state.get("device_id")
            
            if device_id:
                from app.services.health_data_service import get_latest_health_data_by_device
                health_data = get_latest_health_data_by_device(device_id)
            else:
                health_data = get_latest_health_data()
            
            if health_data:
                logger.info(f"Health data collected (device_id: {device_id or 'latest'})")
                logger.debug(f"Data types: steps={bool(health_data.steps)}, heart_rate={bool(health_data.heart_rate)}, sleep={bool(health_data.sleep)}")
                
                data_summary = f"걸음 수: {len(health_data.steps) if health_data.steps else 0}건, 심박수: {len(health_data.heart_rate) if health_data.heart_rate else 0}건, 수면: {len(health_data.sleep) if health_data.sleep else 0}건"
                
                system_prompt = COLLECTOR_SYSTEM.format(collected_data=data_summary)
                llm_response = llm.invoke([
                    SystemMessage(content=system_prompt),
                    HumanMessage(content="수집된 건강 데이터를 평가하세요.")
                ])
                
                logger.debug(f"Data quality assessment: {llm_response.content[:200]}...")
                
                return {
                    "health_data": health_data,
                    "messages": [llm_response]
                }
            else:
                logger.warning("No health data found")
                return {"health_data": None}
                
        except Exception as e:
            logger.error(f"Error in health collector: {e}", exc_info=True)
            return {"health_data": None}
    
    return health_collector

