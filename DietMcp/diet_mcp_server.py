from fastmcp import FastMCP
import httpx  # 통신을 위해 추가된 라이브러리

# 서버 이름 정의
mcp = FastMCP("DietCoachServer")

@mcp.tool()
def call_diet_agent(message: str) -> str:
    """
    FastAPI 백엔드의 /agent/chat 엔드포인트를 호출해서
    다이어트 조언을 받아오는 툴입니다.
    
    Args:
        message: 사용자의 질문 (예: "오늘 피자 먹었는데 괜찮아?")
    """
    url = "http://127.0.0.1:8000/agent/chat"
    
    # 백엔드 서버가 기대하는 데이터 형식에 맞춰야 합니다.
    # 보통 {"query": "질문내용"} 또는 {"message": "질문내용"} 형식을 씁니다.
    # (백엔드 코드를 확인해서 key값을 맞춰주세요. 여기선 'query'라고 가정합니다.)
    payload = {
        "query": message 
    }

    try:
        # 1. 백엔드 서버로 POST 요청 보내기 (전화 걸기)
        with httpx.Client() as client:
            response = client.post(url, json=payload, timeout=30.0)
            
        # 2. 응답 확인 (전화 잘 받았는지 확인)
        response.raise_for_status()
        
        # 3. 결과 반환 (받은 대답을 Claude에게 전달)
        # 백엔드가 {"response": "..."} 형태로 준다고 가정할 때:
        result = response.json()
        return str(result) # 혹은 result.get("answer") 등 필요한 부분만 추출
        
    except Exception as e:
        return f"에러가 발생했습니다: {str(e)}\n(백엔드 서버가 켜져 있는지 확인해주세요!)"

if __name__ == "__main__":
    mcp.run()