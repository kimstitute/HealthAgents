import { useState } from "react";
import WelcomeScreen from "./screens/WelcomeScreen";
import BasicInfoScreen from "./screens/BasicInfoScreen";
import LifestyleSurveyScreen from "./screens/LifestyleSurveyScreen";

type Step = "welcome" | "basic" | "survey";

function App() {
  const [step, setStep] = useState<Step>("welcome");

  // 첫 화면 → 기본 정보 화면
  const handleStart = () => setStep("basic");

  // 기본 정보 입력 완료 → 라이프스타일 설문 화면
  const handleBasicNext = () => {
    // 나중에 여기서 백엔드로 기본 정보 전송 가능
    setStep("survey");
  };

  // 라이프스타일 설문 완료
  const handleSurveyComplete = () => {
    // 나중에 여기서 모든 설문 데이터를 모아서 LLM 코칭 화면으로 넘기면 됨
    console.log("설문 완료!");
    alert("설문이 저장되었습니다! (나중에 LLM 코칭 화면으로 연결 예정)");
  };

  return (
    <>
      {step === "welcome" && <WelcomeScreen onStart={handleStart} />}
      {step === "basic" && <BasicInfoScreen onNext={handleBasicNext} />}
      {step === "survey" && (
        <LifestyleSurveyScreen onComplete={handleSurveyComplete} />
      )}
    </>
  );
}

export default App;
