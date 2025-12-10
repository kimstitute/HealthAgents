// src/api/chat.ts
import type { Block } from "../types/blocks";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export type ChatApiResponse = {
  blocks: Block[];
};

export type PlanRequest = {
  user_name: string;
  basicInfo: {
    age: string;
    gender: string;
    height: string;
    weight: string;
    period: string;
    targetLoss: string;
  };
  lifestyle: {
    exerciseFreq: string;
    mealsPerDay: string;
    nightSnackFreq: string;
    eatingOutFreq: string;
    healthNotes?: string;
  };
  followup: {
    q1: string;
    q2: string;
    q3: string;
  };
  device_id?: string;
};

export type PlanResponse = {
  status: string;
  message: string;
  session_id?: string;
};

export async function initPlan(planData: PlanRequest): Promise<PlanResponse> {
  const res = await fetch(`${API_BASE_URL}/agent/plan/init`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(planData),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API Error ${res.status}: ${text}`);
  }

  const data = (await res.json()) as PlanResponse;
  return data;
}

export async function fetchChatResponse(
  message: string,
  device_id?: string
): Promise<ChatApiResponse> {
  const res = await fetch(`${API_BASE_URL}/agent/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message, device_id }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API Error ${res.status}: ${text}`);
  }

  const data = (await res.json()) as ChatApiResponse;
  return data;
}
