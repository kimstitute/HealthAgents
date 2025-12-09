// 나중에 LLM/백엔드로 보낼 때 사용 가능한 간단 포매터들

import { BasicInfo, LifestyleAnswers } from "../types/survey";

export const formatBasicInfoSummary = (info: BasicInfo): string => {
  return [
    `나이: ${info.age || "미입력"}`,
    `성별: ${info.gender || "미입력"}`,
    `키: ${info.heightCm || "미입력"} cm`,
    `현재 체중: ${info.weightKg || "미입력"} kg`,
    `기간: ${info.periodWeeks || "미입력"} 주`,
    `목표 감량: ${info.targetLossKg || "미입력"} kg`,
  ].join("\n");
};

export const formatLifestyleSummary = (life: LifestyleAnswers): string => {
  return [
    `주당 운동 횟수: ${life.exerciseFreq || "미입력"}`,
    `하루 식사 횟수: ${life.mealsPerDay || "미입력"}`,
    `야식 빈도: ${life.nightSnackFreq || "미입력"}`,
    `외식/배달 빈도: ${life.eatingOutFreq || "미입력"}`,
    `건강 관련 특이사항: ${life.healthNotes || "없음"}`,
  ].join("\n");
};
