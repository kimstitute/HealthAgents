import React, { useState, useEffect, useRef } from "react";
import type { FormEvent } from "react";
import * as S from "./styled"; // 기존 화면 스타일
import ChatBubble from "../../components/ChatBubble";
import { Block } from "../../components/BlockRenderer"; 
import { BlockRenderContainer } from "../../components/BlockRenderer/styled";
import type { Block as BlockData } from "../../types/blocks";
// API 함수
import { fetchChatResponse } from "../../api/chat";


type BasicInfoState = {
  age: string;
  gender: string;
  height: string;
  weight: string;
  period: string;
  targetLoss: string;
};

type LifestyleState = {
  exerciseFreq: string;
  mealsPerDay: string;
  nightSnackFreq: string;
  eatingOutFreq: string;
  healthNotes: string;
};

type Props = {
  basicInfo: BasicInfoState;
  lifestyle: LifestyleState;
};

// ✨ 텍스트 대신 '블록 배열'을 담도록 변경
type ChatMessage = {
  id: number;
  sender: "user" | "bot";
  blocks: BlockData[]; 
};

const CoachChatScreen = ({ basicInfo, lifestyle }: Props) => {
  // 스크롤 자동 이동을 위한 Ref
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // 초기 상태: 텍스트가 아닌 'Block' 구조로 정의
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 1,
      sender: "bot",
      blocks: [
        { id: 'welcome-1', type: 'markdown', content: "안녕하세요! 저는 AI 다이어트 코치에요! 🥗" }
      ],
    },
    {
      id: 2,
      sender: "bot",
      blocks: [
        { 
          id: 'welcome-2', 
          type: 'markdown', 
          content: "지금까지 입력해주신 정보를 바탕으로, **사용자님께 딱 맞는 식단과 운동 계획**을 만들어드릴게요.\n궁금한 점을 편하게 물어봐주세요!" 
        }
      ],
    },
    {
      id: 3,
      sender: "bot",
      blocks: [
        {
          id: 'summary',
          type: 'markdown',
          content: `### 📌 입력 정보 요약
- **기본 정보**: ${basicInfo.age}세 / ${basicInfo.gender} / ${basicInfo.height}cm / ${basicInfo.weight}kg
- **목표**: ${basicInfo.period}주 동안 ${basicInfo.targetLoss}kg 감량
- **라이프스타일**: 주 ${lifestyle.exerciseFreq}회 운동, 하루 ${lifestyle.mealsPerDay}끼
- **특이사항**: ${lifestyle.healthNotes || "없음"}`
        },
        {
          id: 'guide',
          type: 'markdown',
          content: "이 정보를 바탕으로 **'점심 추천해줘'**, **'운동 계획 짜줘'** 등을 물어보시면 AI가 화려한 답변(차트, 지도 등)을 줄 거예요!"
        }
      ]
    },
  ]);

  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);

  // 메시지 추가될 때마다 스크롤 내리기
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isSending) return;

    const text = input.trim();
    setInput("");
    setIsSending(true);

    // 1. 유저 메시지 추가 (유저 입력은 단순 Markdown Block으로 변환)
    const userMsg: ChatMessage = {
      id: Date.now(),
      sender: "user",
      blocks: [{ id: `user-${Date.now()}`, type: 'markdown', content: text }],
    };
    setMessages((prev) => [...prev, userMsg]);

    try {
      // 2. API 호출 (Mock Data 받아오기)
      // 실제로는 여기서 백엔드에 'text'를 보내고 'Block[]'을 받습니다.
      const response = await fetchChatResponse(text);

      const botMsg: ChatMessage = {
        id: Date.now() + 1,
        sender: "bot",
        blocks: response.blocks, // ✨ 서버가 준 블록 그대로 주입
      };
      
      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      console.error("API Error:", error);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <S.Container>
      <S.Inner>
        <S.Header>
          <S.Title>AI 다이어트 코치 채팅</S.Title>
          <S.Sub>차트, 지도, 이미지를 포함한 답변을 확인해보세요 💬</S.Sub>
        </S.Header>

        <S.ChatArea>
          {messages.map((m) => (
            <S.MessageRow key={m.id} side={m.sender === "user" ? "right" : "left"}>
              <ChatBubble variant={m.sender === "user" ? "user" : "bot"}>
                
                {/* ✨ 핵심: 여기서 BlockRenderContainer로 감싸고 Block을 렌더링 */}
                <BlockRenderContainer>
                  {m.blocks.map((block, index) => (
                    // id가 없으면 index를 key로 사용 (안전장치)
                    <Block key={block.id || index} block={block} />
                  ))}
                </BlockRenderContainer>

              </ChatBubble>
            </S.MessageRow>
          ))}
          {/* 스크롤 하단 앵커 */}
          <div ref={messagesEndRef} />
        </S.ChatArea>

        <S.InputForm onSubmit={handleSend}>
          <S.TextInput
            placeholder="예: 오늘 점심 식단 추천해줘 (차트/지도 테스트용)"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <S.SendButton type="submit" disabled={isSending || !input.trim()}>
            {isSending ? "분석 중..." : "전송"}
          </S.SendButton>
        </S.InputForm>
      </S.Inner>
    </S.Container>
  );
};

export default CoachChatScreen;