// src/api/chat.ts
import type { Block } from "../types/blocks";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export type ChatApiResponse = {
  blocks: Block[];
};

export async function fetchChatResponse(
  message: string
): Promise<ChatApiResponse> {
  const res = await fetch(`${API_BASE_URL}/agent/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }), // 👈 ChatRequest.message
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API Error ${res.status}: ${text}`);
  }

  const data = (await res.json()) as ChatApiResponse;
  return data;
}
