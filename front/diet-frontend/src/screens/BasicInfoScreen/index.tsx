import * as S from "./styled";
import FormInput from "../../components/FormInput";

type BasicInfo = {
  age: string;
  gender: string;
  heightCm: string;
  weightKg: string;
  periodWeeks: string;
  targetLossKg: string;
};

type BasicInfoScreenProps = {
  data: BasicInfo;                                // 👈 App에서 내려주는 값
  onChange: (next: BasicInfo) => void;           // 👈 App의 setter
  onNext: (info: BasicInfo) => void;             // 👈 다음 단계로 넘어갈 때 App에 알려줌
};

const BasicInfoScreen = ({ data, onChange, onNext }: BasicInfoScreenProps) => {
  // 로컬 state ❌  App state 사용 ⭕
  const handleChange = (field: keyof BasicInfo, value: string) => {
    onChange({
      ...data,
      [field]: value,
    });
  };

  const handleNext = () => {
    console.log("입력된 정보:", data);
    onNext(data);
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
          <FormInput
            label="나이"
            type="number"
            value={data.age}
            onChange={(v) => handleChange("age", v)}
            placeholder="예: 25"
          />
          <FormInput
            label="성별"
            type="select"
            value={data.gender}
            onChange={(v) => handleChange("gender", v)}
            options={["여성", "남성", "기타"]}
          />
          <FormInput
            label="키 (cm)"
            type="number"
            value={data.heightCm}
            onChange={(v) => handleChange("heightCm", v)}
            placeholder="예: 162"
          />
          <FormInput
            label="현재 체중 (kg)"
            type="number"
            value={data.weightKg}
            onChange={(v) => handleChange("weightKg", v)}
            placeholder="예: 65"
          />
          <FormInput
            label="다이어트 기간 (주)"
            type="number"
            value={data.periodWeeks}
            onChange={(v) => handleChange("periodWeeks", v)}
            placeholder="예: 4"
          />
          <FormInput
            label="목표 감량 체중 (kg)"
            type="number"
            value={data.targetLossKg}
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
