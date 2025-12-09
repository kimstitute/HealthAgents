import { useState } from "react"; // 1. useState import 추가
import * as S from "./styled";
import FormInput from "../../components/FormInput";

type BasicInfoScreenProps = {
  onNext: () => void;
};

const BasicInfoScreen = ({ onNext }: BasicInfoScreenProps) => {
  // 1. 스토어 제거하고 로컬 state 생성
  const [info, setInfo] = useState({
    age: "",
    gender: "",
    heightCm: "",
    weightKg: "",
    periodWeeks: "",
    targetLossKg: "",
  });

  // 2. 입력값 변경 핸들러
  const handleChange = (field: string, value: string) => {
    setInfo((prev) => ({ ...prev, [field]: value }));
  };

  const handleNext = () => {
    // TODO: 나중에 검증/백엔드 전송 가능
    console.log("입력된 정보:", info); // 데이터 확인용 로그
    onNext();
  };

  return (
    <S.Container>
      <S.Inner>
        <S.Title>
          사용자님 안녕하세요. 👋
          <br />
          저는 사용자님의 다이어트 개인 비서입니다.
        </S.Title>
        <S.Sub>
          맞춤형 다이어트 코치를 위해
          <br />
          기본 신체 정보를 작성해주세요!
        </S.Sub>

        <S.FormCard>
          {/* value와 onChange를 로컬 state인 info와 handleChange로 연결 */}
          <FormInput
            label="나이"
            type="number"
            value={info.age}
            onChange={(v) => handleChange("age", v)}
            placeholder="예: 25"
          />
          <FormInput
            label="성별"
            type="select"
            value={info.gender}
            onChange={(v) => handleChange("gender", v)}
            options={["여성", "남성", "기타"]}
          />
          <FormInput
            label="키 (cm)"
            type="number"
            value={info.heightCm}
            onChange={(v) => handleChange("heightCm", v)}
            placeholder="예: 162"
          />
          <FormInput
            label="현재 체중 (kg)"
            type="number"
            value={info.weightKg}
            onChange={(v) => handleChange("weightKg", v)}
            placeholder="예: 65"
          />
          <FormInput
            label="다이어트 기간 (주)"
            type="number"
            value={info.periodWeeks}
            onChange={(v) => handleChange("periodWeeks", v)}
            placeholder="예: 4"
          />
          <FormInput
            label="목표 감량 체중 (kg)"
            type="number"
            value={info.targetLossKg}
            onChange={(v) => handleChange("targetLossKg", v)}
            placeholder="예: 5"
          />
        </S.FormCard>

        <S.NextButton type="button" onClick={handleNext}>
          다음 단계로 이동하기 ➜
        </S.NextButton>
      </S.Inner>
    </S.Container>
  );
};

export default BasicInfoScreen;