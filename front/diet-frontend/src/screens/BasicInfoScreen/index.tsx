import * as S from "./styled";
import FormInput from "../../components/FormInput";

// 1. App.tsx와 변수명을 똑같이 맞춘 타입 정의
type BasicInfo = {
  age: string;
  gender: string;
  height: string;      // heightCm -> height 로 변경
  weight: string;      // weightKg -> weight 로 변경
  period: string;      // periodWeeks -> period 로 변경
  targetLoss: string;  // targetLossKg -> targetLoss 로 변경
};

// 2. App.tsx에서 내려주는 props를 받도록 정의
type BasicInfoScreenProps = {
  data: BasicInfo;                     // App.tsx의 basicInfo 상태
  onChange: (info: BasicInfo) => void; // App.tsx의 setBasicInfo 함수
  onNext: (info: BasicInfo) => void;   // 다음 단계 이동 함수
};

const BasicInfoScreen = ({ data, onChange, onNext }: BasicInfoScreenProps) => {

  // 3. 입력값 변경 시 App.tsx의 상태를 업데이트
  const handleChange = (field: keyof BasicInfo, value: string) => {
    onChange({ ...data, [field]: value });
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
          {/* value는 data에서 가져오고, 필드명은 height, weight 등으로 통일 */}
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
            value={data.height}
            onChange={(v) => handleChange("height", v)}
            placeholder="예: 162"
          />
          <FormInput
            label="현재 체중 (kg)"
            type="number"
            value={data.weight}
            onChange={(v) => handleChange("weight", v)}
            placeholder="예: 65"
          />
          <FormInput
            label="다이어트 기간 (주)"
            type="number"
            value={data.period}
            onChange={(v) => handleChange("period", v)}
            placeholder="예: 4"
          />
          <FormInput
            label="목표 감량 체중 (kg)"
            type="number"
            value={data.targetLoss}
            onChange={(v) => handleChange("targetLoss", v)}
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