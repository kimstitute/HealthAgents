export type BasicInfo = {
  age: string;          // 나이
  gender: string;       // 성별
  heightCm: string;     // 키
  weightKg: string;     // 현재 체중
  periodWeeks: string;  // 다이어트 기간 (주)
  targetLossKg: string; // 목표 감량 체중
};

export type LifestyleAnswers = {
  exerciseFreq: string;   // 주당 운동 횟수
  mealsPerDay: string;    // 하루 식사 횟수
  nightSnackFreq: string; // 야식 빈도
  eatingOutFreq: string;  // 외식/배달 빈도
  healthNotes: string;    // 건강 관련 특이사항
};

export type SurveyState = {
  basicInfo: BasicInfo;
  lifestyle: LifestyleAnswers;
};
