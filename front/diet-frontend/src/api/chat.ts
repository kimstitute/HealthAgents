// api/chat.ts
import {type Block } from "../types/blocks"; 
export interface ChatResponse {
  blocks: Block[];
}
const API_BASE_URL = "http://localhost:8000";
/**
 * 🛠️ MOCK API (프론트엔드 테스트용 가짜 서버)
 * 백엔드 없이도 차트/지도/이미지가 잘 나오는지 확인할 수 있게 해줍니다.
 */
export const fetchChatResponse = async (message: string): Promise<ChatResponse> => {
  return new Promise((resolve) => {
    // 1.5초 뒤에 응답이 오는 척 연기 (로딩바 테스트용)
    setTimeout(() => {
      resolve({
        blocks: [
          // 1. 텍스트 블록
          {
            id: '1',
            type: 'markdown',
            content: `### 🥗 ${message}에 대한 분석 결과입니다.\n오늘 드신 **샐러드 보울**은 탄단지 비율이 아주 훌륭해요! 다만, 드레싱 칼로리가 조금 높을 수 있으니 주의하세요.`
          },
          
          // 2. 가로 배치 (이미지 + 차트)
          {
            id: '2',
            type: 'row',
            gap: '12px',
            children: [
              {
                id: '2-1',
                type: 'image',
                url: 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500&q=80',
                alt: '샐러드 예시',
                caption: '입력하신 식단 이미지'
              },
              {
                id: '2-2',
                type: 'chart',
                chartType: 'doughnut',
                title: '영양소 비율',
                data: {
                  labels: ['탄수화물', '단백질', '지방'],
                  values: [45, 30, 25]
                },
                description: '단백질이 충분합니다! 💪'
              }
            ]
          },

          // 3. 테이블 블록
          {
            id: '3',
            type: 'table',
            title: '상세 영양 성분',
            headers: ['항목', '함량', '권장량 대비'],
            rows: [
              ['칼로리', '450kcal', '22%'],
              ['단백질', '28g', '45%'],
              ['나트륨', '800mg', '⚠️ 주의'],
            ]
          },

          // 4. 지도 블록 (맛집 추천)
          {
            id: '4',
            type: 'markdown',
            content: '혹시 내일 점심은 여기서 어떠세요? 건강한 샐러드 맛집입니다.'
          },
          {
            id: '5',
            type: 'map',
            title: '추천: 그린 샐러드 강남점',
            center: { lat: 37.4979, lng: 127.0276 },
            zoom: 16,
            markers: [
              { lat: 37.4979, lng: 127.0276, label: 'G', type: 'restaurant' }
            ],
            description: '서울 강남구 테헤란로 1길'
          }
        ]
      });
    }, 1500); // 1.5초 딜레이
  });
};



export async function sendMessage(message: string): Promise<Block[]> {
  const response = await fetch(`${API_BASE_URL}/agent/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    // 백엔드 ChatRequest 스키마와 필드명(message) 일치
    body: JSON.stringify({ message }), 
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  // 백엔드 응답이 ChatResponse 타입과 필드명(blocks)까지 완벽히 일치하므로
  // 별도의 매핑(map)이나 변환 함수 없이 바로 캐스팅(as) 가능
  const data = (await response.json()) as ChatResponse;
  
  return data.blocks;
}