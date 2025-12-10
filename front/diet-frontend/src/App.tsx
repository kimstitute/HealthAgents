import { useState } from "react";
import WelcomeScreen from "./screens/WelcomeScreen";
import BasicInfoScreen from "./screens/BasicInfoScreen";
import LifestyleSurveyScreen from "./screens/LifestyleSurveyScreen";
import CoachChatScreen from "./screens/CoachChatScreen";

type Step = "welcome" | "basic" | "survey" | "chat";

// [수정됨] 요청하신 타입 및 필드명으로 원복
type BasicInfoState = {
  age: string;
  gender: string;
  height: string;     // heightCm -> height
  weight: string;     // weightKg -> weight
  period: string;     // periodWeeks -> period
  targetLoss: string; // targetLossKg -> targetLoss
};

// 라이프스타일 설문 타입
type LifestyleState = {
  exerciseFreq: string;
  mealsPerDay: string;
  nightSnackFreq: string;
  eatingOutFreq: string;
  healthNotes: string;
};

function App() {
  const [step, setStep] = useState<Step>("welcome");

  // [수정됨] BasicInfoState 타입 적용 및 초기값 키 이름 변경
  const [basicInfo, setBasicInfo] = useState<BasicInfoState>({
    age: "",
    gender: "",
    height: "",
    weight: "",
    period: "",
    targetLoss: "",
  });

  const [lifestyle, setLifestyle] = useState<LifestyleState>({
    exerciseFreq: "",
    mealsPerDay: "",
    nightSnackFreq: "",
    eatingOutFreq: "",
    healthNotes: "",
  });

  // 1) 첫 화면 → 기본 정보 화면
  const handleStart = () => setStep("basic");

  // 2) 기본 정보 입력 완료 → 라이프스타일 설문 화면
  // [수정됨] 매개변수 타입 변경 (BasicInfo -> BasicInfoState)
  const handleBasicNext = (info: BasicInfoState) => {
    setBasicInfo(info);
    setStep("survey");
  };

  // 3) 라이프스타일 설문 완료 → 코칭 채팅 화면
  const handleSurveyComplete = (data: LifestyleState) => {
    setLifestyle(data);
    setStep("chat");
  };

  return (
    <>
      {step === "welcome" && <WelcomeScreen onStart={handleStart} />}

      {step === "basic" && (
        <BasicInfoScreen
          data={basicInfo}
          onChange={setBasicInfo}
          onNext={handleBasicNext}
        />
      )}

      {step === "survey" && (
        <LifestyleSurveyScreen
          data={lifestyle}
          onChange={setLifestyle}
          onComplete={handleSurveyComplete}
        />
      )}

      {step === "chat" && (
        <CoachChatScreen basicInfo={basicInfo} lifestyle={lifestyle} />
      )}
    </>
  );
}

export default App;