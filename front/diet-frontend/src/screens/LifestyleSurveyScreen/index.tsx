import { useState } from "react";
import * as S from "./styled";
import ChatBubble from "../../components/ChatBubble";
import ChoiceButtons from "../../components/ChoiceButtons";

type LifestyleState = {
  exerciseFreq: string;
  mealsPerDay: string;
  nightSnackFreq: string;
  eatingOutFreq: string;
  healthNotes: string;
};

type Props = {
  data: LifestyleState;
  onChange: (next: LifestyleState) => void;
  onComplete: (data: LifestyleState) => void;
};

type Question =
  | {
      key: keyof LifestyleState;
      type: "choice";
      text: string;
      options: string[];
    }
  | {
      key: "healthNotes";
      type: "text";
      text: string;
    };

const QUESTIONS: Question[] = [
  {
    key: "exerciseFreq",
    type: "choice",
    text:
      "현재 생활패턴에 대해 질문해볼게요!\n" +
      "사용자님은 주당 운동 횟수가 어떻게 되나요?",
    options: ["없음", "1~2회", "3~5회", "매일"],
  },
  {
    key: "mealsPerDay",
    type: "choice",
    text:
      "주로 먹는 식습관을 물어볼게요.\n" +
      "사용자님은 보통 하루에 몇 끼 드시나요?",
    options: ["1일 1식", "1일 2식", "1일 3식"],
  },
  {
    key: "nightSnackFreq",
    type: "choice",
    text: "야식은 자주 드시나요?",
    options: ["거의 안 먹음", "가끔 먹음", "자주 먹음"],
  },
  {
    key: "eatingOutFreq",
    type: "choice",
    text: "외식이나 배달 음식은 얼마나 자주 드시나요?",
    options: ["거의 없음", "주 1~2회", "주 3~5회", "거의 매일"],
  },
  {
    key: "healthNotes",
    type: "text",
    text:
      "건강 관련 사항도 알려주세요.\n" +
      "위장장애, 알레르기, 수면장애, 의사가 제안한 음식·운동이 있다면 적어주세요.",
  },
];

const LifestyleSurveyScreen = ({ data, onChange, onComplete }: Props) => {
  const [stepIndex, setStepIndex] = useState(0);
  const [healthDraft, setHealthDraft] = useState(data.healthNotes || "");

  const current = QUESTIONS[stepIndex];

  const goNext = (updated: LifestyleState) => {
    if (stepIndex >= QUESTIONS.length - 1) {
      onComplete(updated);
    } else {
      setStepIndex((prev) => prev + 1);
    }
  };

  const handleChoice = (value: string) => {
    if (current.type !== "choice") return;
    const next = { ...data, [current.key]: value };
    onChange(next);
    goNext(next);
  };

  const handleHealthSubmit = () => {
    const next = { ...data, healthNotes: healthDraft };
    onChange(next);
    goNext(next);
  };

  return (
    <S.Container>
      <S.Inner>
        <S.Header>생활 패턴 간단 설문</S.Header>
        <S.ChatArea>
          <ChatBubble variant="bot">{current.text}</ChatBubble>

          {current.type === "choice" && (
            <ChoiceButtons options={current.options} onSelect={handleChoice} />
          )}

          {current.type === "text" && (
            <S.TextBlock>
              <S.TextArea
                placeholder="자유롭게 적어주세요. 없다면 '없음'이라고 적으셔도 됩니다."
                value={healthDraft}
                onChange={(e) => setHealthDraft(e.target.value)}
              />
              <S.SubmitButton type="button" onClick={handleHealthSubmit}>
                입력 완료
              </S.SubmitButton>
            </S.TextBlock>
          )}
        </S.ChatArea>
      </S.Inner>
    </S.Container>
  );
};

export default LifestyleSurveyScreen;
