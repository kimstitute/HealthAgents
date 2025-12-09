import { useState } from "react";
import * as S from "./styled";
import ChatBubble from "../../components/ChatBubble";
import ChoiceButtons from "../../components/ChoiceButtons";

// 부모 컴포넌트에게 데이터를 넘겨줄 수 있도록 타입 수정
type LifestyleSurveyScreenProps = {
  onComplete: (data: any) => void;
};

type Question =
  | {
      key: "exerciseFreq" | "mealsPerDay" | "nightSnackFreq" | "eatingOutFreq";
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
    text: "좋아요! 😊\n보통 하루에 몇 끼 드시나요?",
    options: ["1일 1식", "1일 2식", "1일 3식"],
  },
  {
    key: "nightSnackFreq",
    type: "choice",
    text: "야식은 얼마나 드시나요?",
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
      "마지막으로 건강 관련해서 참고해야 할 사항이 있나요?\n" +
      "(위장장애, 알레르기, 수면장애, 의사가 권장한 음식/운동 등)",
  },
];

const LifestyleSurveyScreen = ({ onComplete }: LifestyleSurveyScreenProps) => {
  // 1. 스토어 대신 로컬 state로 답변 저장
  const [answers, setAnswers] = useState<Record<string, string>>({});
  
  const [stepIndex, setStepIndex] = useState(0);
  const [healthNotesDraft, setHealthNotesDraft] = useState("");

  const current = QUESTIONS[stepIndex];

  // 다음 단계로 넘어가거나 완료 처리하는 함수
  const handleNextStep = (updatedAnswers: Record<string, string>) => {
    if (stepIndex >= QUESTIONS.length - 1) {
      // 마지막 단계라면 최종 데이터와 함께 완료 함수 호출
      console.log("설문 완료 데이터:", updatedAnswers);
      onComplete(updatedAnswers);
    } else {
      // 다음 질문으로 이동
      setStepIndex((prev) => prev + 1);
    }
  };

  // 객관식 답변 처리
  const handleChoice = (value: string) => {
    if (current.type !== "choice") return;
    
    // 답변 저장
    const newAnswers = { ...answers, [current.key]: value };
    setAnswers(newAnswers);
    
    // 다음으로
    handleNextStep(newAnswers);
  };

  // 주관식(건강 메모) 답변 처리
  const handleHealthNotesSubmit = () => {
    // 답변 저장
    const newAnswers = { ...answers, healthNotes: healthNotesDraft };
    setAnswers(newAnswers);

    // 다음으로 (보통 여기가 마지막)
    handleNextStep(newAnswers);
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
                placeholder="자유롭게 적어주세요. 없다면 '없음'이라고 적어주셔도 됩니다."
                value={healthNotesDraft}
                onChange={(e) => setHealthNotesDraft(e.target.value)}
              />
              <S.SubmitButton type="button" onClick={handleHealthNotesSubmit}>
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