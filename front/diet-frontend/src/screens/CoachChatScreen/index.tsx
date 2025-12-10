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

// 텍스트 대신 '블록 배열'을 담도록 변경
type ChatMessage = {
  id: number;
  sender: "user" | "bot";
  blocks: BlockData[];
};

// 추가 질문 답변을 담을 타입
type FollowupAnswers = {
  q1: string;
  q2: string;
  q3: string;
};

const CoachChatScreen = ({ basicInfo, lifestyle }: Props) => {
  // 스크롤 자동 이동을 위한 Ref
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // 0: 일반 대화, 1, 2, 3: 각 질문 단계
  const [questionStep, setQuestionStep] = useState(1); // 초기값: 첫 질문을 시작할 단계
  const [followupAnswers, setFollowupAnswers] = useState<FollowupAnswers>({
    q1: "",
    q2: "",
    q3: "",
  });

  // 초기 상태: 텍스트가 아닌 'Block' 구조로 정의
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 1,
      sender: "bot",
      blocks: [
        {
          id: "welcome-1",
          type: "markdown",
          content: "안녕하세요! 저는 AI 다이어트 코치에요! 🥗",
        },
      ],
    },
    {
      id: 2,
      sender: "bot",
      blocks: [
        {
          id: "welcome-2",
          type: "markdown",
          content:
            "지금까지 입력해주신 정보를 바탕으로, **사용자님께 딱 맞는 식단과 운동 계획**을 만들어드릴게요.\n궁금한 점을 편하게 물어봐주세요!",
        },
      ],
    },
    {
      id: 3,
      sender: "bot",
      blocks: [
        {
          id: "summary",
          type: "markdown",
          content: `### 📌 입력 정보 요약
- **기본 정보**: ${basicInfo.age}세 / ${basicInfo.gender} / ${basicInfo.height}cm / ${basicInfo.weight}kg
- **목표**: ${basicInfo.period}주 동안 ${basicInfo.targetLoss}kg 감량
- **라이프스타일**: 주 ${lifestyle.exerciseFreq} 운동, 하루 ${lifestyle.mealsPerDay}
- **특이사항**: ${lifestyle.healthNotes || "없음"}`,
        },
        {
          id: "guide",
          type: "markdown",
          content:
            "지금 알려주신 정보를 기반으로 맞춤형 4주 플랜을 만들어드리기 전에 몇 가지만 더 여쭤보고 싶어요",
        },
      ],
    },
  ]);

  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);

  // ✨ 질문 전송 함수들 (봇 메시지 추가 역할)
  const askQuestion = (step: number, question: string) => {
    const baseId = Date.now() + step;
    const botMsg: ChatMessage = {
      id: baseId,
      sender: "bot",
      blocks: [
        {
          id: `q${step}-${baseId}`,
          type: "markdown",
          content: `**[추가 질문 ${step}/3]**\n${question}`,
        },
      ],
    };
    // 기존 메시지 배열에 봇 메시지 추가
    setMessages((prev) => [...prev, botMsg]);
  };

  // 각 질문 정의
  const askQuestion1 = () => {
    askQuestion(
      1,
      "가장 중요하게 생각하는 **식습관 개선 목표**는 무엇인가요? (예: 야식 끊기, 폭식 줄이기, 채소 섭취 늘리기)"
    );
  };

  const askQuestion2 = () => {
    askQuestion(
      2,
      "선호하는 **운동 종류**나 피하고 싶은 운동이 있나요? (예: 유산소 선호, 근력 운동 싫음, 걷기 좋아함)"
    );
  };

  const askQuestion3 = () => {
    askQuestion(
      3,
      "식단이나 운동 계획에서 **절대 포기할 수 없는 부분**이 있다면 알려주세요. (예: 아침 식사는 꼭 밥으로 먹어야 함, 주말에는 자유식 선호)"
    );
  };



//메시지 업데이트 시 스크롤 이동
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

useEffect(() => {
  const timer = setTimeout(() => {
    askQuestion1();
    setQuestionStep(1); // 이제 1번 질문에 대한 답을 기다리는 상태
  }, 5000); // 5초

  return () => clearTimeout(timer);
}, []);


const handleSend = async (e: FormEvent) => {
  e.preventDefault();
  if (!input.trim() || isSending) return;

  const text = input.trim();
  setInput("");

  const baseId = Date.now();

  // 1) 유저 메시지는 항상 먼저 화면에 추가
  const userMsg: ChatMessage = {
    id: baseId,
    sender: "user",
    blocks: [
      {
        id: `user-${baseId}`,
        type: "markdown",
        content: text,
      },
    ],
  };
  setMessages((prev) => [...prev, userMsg]);

  // 2) 질문 단계에 따라 행동 분기

  // ✅ Q1에 대한 답을 방금 받은 경우
  if (questionStep === 1) {
    setFollowupAnswers((prev) => ({ ...prev, q1: text }));
    setQuestionStep(2);   // 이제 Q2를 물어볼 차례
    askQuestion2();       // Q2 질문 전송
    return;               // 아직 백엔드 호출 X
  }

  // ✅ Q2에 대한 답을 방금 받은 경우
  if (questionStep === 2) {
    setFollowupAnswers((prev) => ({ ...prev, q2: text }));
    setQuestionStep(3);
    askQuestion3();       // Q3 질문 전송
    return;
  }

  // ✅ Q3에 대한 답을 방금 받은 경우 → 여기서 백엔드로 전체 데이터 전송
  if (questionStep === 3) {
    // 바로 아래 한 줄처럼 "업데이트된 값"을 만들어 두고, 이걸로 payload 구성
    const updatedAnswers = { ...followupAnswers, q3: text };
    setFollowupAnswers(updatedAnswers);
    setQuestionStep(0); // 추가질문 단계 종료



    // 🔹 여기서 allUserData 만들어서 백엔드로 보냄
    const allUserData = {
      // Notion Name이랑 맞출 값 (props로 userName이 있다면 그걸 쓰셔도 됨)
      user_name: "강진희",
      basicInfo,      // props에서 받은 기본 정보
      lifestyle,      // props에서 받은 라이프스타일 정보
      followup: updatedAnswers, // q1, q2, q3 모두 포함
    };

    setIsSending(true);
    try {
      // ❗ 여기서는 "플랜 생성용" API를 따로 두는 걸 추천
      // 예: fetchPlan(allUserData)
      const response = await fetchChatResponse(allUserData as any);

      const botMsg: ChatMessage = {
        id: baseId + 1,
        sender: "bot",
        blocks: response.blocks ?? [
          {
            id: `bot-fallback-${baseId}`,
            type: "markdown",
            content: "플랜을 생성하는 중 문제가 발생했어요.",
          },
        ],
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      console.error("API Error:", error);
      const errMsg: ChatMessage = {
        id: baseId + 1,
        sender: "bot",
        blocks: [
          {
            id: `bot-error-${baseId}`,
            type: "markdown",
            content: "❌ 서버 오류가 발생했어요. 잠시 후 다시 시도해 주세요.",
          },
        ],
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setIsSending(false);
    }

    return;
  }

  // ✅ 그 외의 경우(추가질문 끝난 뒤 일반 채팅 모드)
  setIsSending(true);
  try {
    const response = await fetchChatResponse(text);
    const botMsg: ChatMessage = {
      id: baseId + 1,
      sender: "bot",
      blocks: response.blocks ?? [
        {
          id: `bot-fallback-${baseId}`,
          type: "markdown",
          content: "⚠️ 서버 응답을 불러오지 못했어요.",
        },
      ],
    };
    setMessages((prev) => [...prev, botMsg]);
  } catch (error) {
    console.error("API Error:", error);
    const errMsg: ChatMessage = {
      id: baseId + 1,
      sender: "bot",
      blocks: [
        {
          id: `bot-error-${baseId}`,
          type: "markdown",
          content: "❌ 서버 오류가 발생했어요. 잠시 후 다시 시도해 주세요.",
        },
      ],
    };
    setMessages((prev) => [...prev, errMsg]);
  } finally {
    setIsSending(false);
  }
};

  return (
    <S.Container>
      <S.Inner>
        <S.Header>
          <S.Title>AI 다이어트 코치 채팅</S.Title>
          <S.Sub>
            이 코치는 의료 상담이 아닌 일반적인 다이어트 조언을 제공합니다.{"\n"}
            건강 이상이 느껴지면 전문가와 상담하세요
          </S.Sub>
        </S.Header>

        <S.ChatArea>
          {messages.map((m) => (
            <S.MessageRow
              key={m.id}
              side={m.sender === "user" ? "right" : "left"}
            >
              <ChatBubble variant={m.sender === "user" ? "user" : "bot"}>
                <BlockRenderContainer>
                  {m.blocks.map((block, index) => (
                    <Block key={block.id || index} block={block} />
                  ))}
                </BlockRenderContainer>
              </ChatBubble>
            </S.MessageRow>
          ))}
          <div ref={messagesEndRef} />
        </S.ChatArea>

        <S.InputForm onSubmit={handleSend}>
          <S.TextInput
            placeholder={questionStep !== 0 ? `Q${questionStep}에 대한 답변을 입력해주세요.` : "예: 오늘 점심 식단 추천해줘"}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isSending}
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