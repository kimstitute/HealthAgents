import { FormEvent, useState } from "react";
import * as S from "./styled";
import ChatBubble from "../../components/ChatBubble";

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

type ChatMessage = {
  id: number;
  sender: "user" | "bot";
  text: string;
};

const CoachChatScreen = ({ basicInfo, lifestyle }: Props) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 1,
      sender: "bot",
      text: "안녕하세요! 저는 AI 다이어트 코치에요! 🥗",
    },
    {
      id: 2,
      sender: "bot",
      text:
        "지금까지 입력해주신 정보를 바탕으로, 사용자님께 맞는 다이어트 계획을 같이 만들어볼게요.\n" +
        "궁금한 점이나 힘든 점을 편하게 말씀해 주세요!",
    },
    {
      id: 3,
      sender: "bot",
      text:
        "📌 지금까지 입력해주신 내용 요약이에요.\n\n" +
        `- 나이: ${basicInfo.age || "미입력"}세\n` +
        `- 성별: ${basicInfo.gender || "미입력"}\n` +
        `- 키: ${basicInfo.height || "미입력"} cm\n` +
        `- 현재 체중: ${basicInfo.weight || "미입력"} kg\n` +
        `- 기간: ${basicInfo.period || "미입력"} 주\n` +
        `- 목표 감량: ${basicInfo.targetLoss || "미입력"} kg\n\n` +
        `- 주당 운동 횟수: ${lifestyle.exerciseFreq || "미입력"}\n` +
        `- 하루 식사 횟수: ${lifestyle.mealsPerDay || "미입력"}\n` +
        `- 야식 빈도: ${lifestyle.nightSnackFreq || "미입력"}\n` +
        `- 외식/배달 빈도: ${lifestyle.eatingOutFreq || "미입력"}\n` +
        `- 건강 관련 사항: ${
          lifestyle.healthNotes?.trim() || "없음"
        }\n\n이 정보를 바탕으로 질문을 주시면, 나중에 LLM이 맞춤 코칭을 해줄 거예요!`,
    },
  ]);

  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);

  const handleSend = (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isSending) return;

    const text = input.trim();
    setInput("");

    const userMsg: ChatMessage = {
      id: Date.now(),
      sender: "user",
      text,
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsSending(true);

    // TODO: 나중에 여기서 백엔드에 LLM 질문 보내기
    setTimeout(() => {
      const botMsg: ChatMessage = {
        id: Date.now() + 1,
        sender: "bot",
        text:
          "좋은 이야기네요! 😊\n" +
          "나중에 백엔드와 연결되면, 여기에서 LLM이 식단/운동 계획을 구체적으로 답해줄 거예요.\n" +
          "현재는 프론트엔드 데모라 간단한 더미 응답만 보여드리고 있어요.",
      };
      setMessages((prev) => [...prev, botMsg]);
      setIsSending(false);
    }, 800);
  };

  return (
    <S.Container>
      <S.Inner>
        <S.Header>
          <S.Title>AI 다이어트 코치 채팅</S.Title>
          <S.Sub>이제부터는 코치와 자유롭게 대화해 보세요 💬</S.Sub>
        </S.Header>

        <S.ChatArea>
          {messages.map((m) => (
            <S.MessageRow key={m.id} side={m.sender === "user" ? "right" : "left"}>
              <ChatBubble variant={m.sender === "user" ? "user" : "bot"}>
                {m.text}
              </ChatBubble>
            </S.MessageRow>
          ))}
        </S.ChatArea>

        <S.InputForm onSubmit={handleSend}>
          <S.TextInput
            placeholder="궁금한 점이나 오늘의 상태를 자유롭게 적어주세요."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <S.SendButton type="submit" disabled={isSending || !input.trim()}>
            {isSending ? "생각 중..." : "전송"}
          </S.SendButton>
        </S.InputForm>
      </S.Inner>
    </S.Container>
  );
};

export default CoachChatScreen;
