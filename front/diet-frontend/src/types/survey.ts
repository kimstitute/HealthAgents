export type BasicInfo = {
  age: string;       // 나이
  gender: string;    // 성별
  height: string;    // 키 (cm)
  weight: string;    // 현재 체중 (kg)
  period: string;    // 다이어트 기간 (주)
  targetLoss: string; // 목표 감량 체중 (kg)
};

export type LifestyleAnswers = {
  exerciseFreq: string;    // 주당 운동 횟수
  mealsPerDay: string;     // 하루 식사 횟수
  nightSnackFreq: string;  // 야식 빈도
  eatingOutFreq: string;   // 외식/배달 빈도
  healthNotes: string;     // 건강 특이사항
};

export type SurveyState = {
  basicInfo: BasicInfo;
  lifestyle: LifestyleAnswers;
};
