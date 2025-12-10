import styled from "styled-components";

export const Container = styled.div`
  min-height: 100vh;
  padding: 24px;
  background: radial-gradient(circle at top, #fee2e2, #eef2ff);
  display: flex;
  justify-content: center;
  align-items: center;
`;

export const Inner = styled.div`
  background: ${({ theme }) => theme.colors.cardBg || "#fff"};
  border-radius: 24px;
  box-shadow: ${({ theme }) => theme.shadows?.soft || "0 8px 20px rgba(0,0,0,0.12)"};
  width: 100%;
  max-width: 480px;
  padding: 20px 18px 16px;
  display: flex;
  flex-direction: column;
  max-height: 640px;
`;

export const Header = styled.div`
  margin-bottom: 8px;
`;

export const Title = styled.h2`
  margin: 0;
  font-size: 18px;
`;

export const Sub = styled.p`
  margin: 4px 0 0;
  font-size: 12px;
  color: #6b7280;
`;

export const ChatArea = styled.div`
  flex: 1;
  margin-top: 8px;
  padding: 10px 4px;
  overflow-y: auto;
`;

export const MessageRow = styled.div<{ side: "left" | "right" }>`
  display: flex;
  justify-content: ${(p) => (p.side === "right" ? "flex-end" : "flex-start")};
`;

export const InputForm = styled.form`
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
`;

export const TextInput = styled.input`
  flex: 1;
  border-radius: 999px;
  border: 1px solid #d4d4d8;
  padding: 8px 12px;
  font-size: 13px;
  outline: none;

  &:focus {
    border-color: #4f46e5;
    box-shadow: 0 0 0 1px rgba(79, 70, 229, 0.18);
  }
`;

export const SendButton = styled.button`
  padding: 0 14px;
  border-radius: 999px;
  border: none;
  background: #4f46e5;
  color: #fff;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;

  &:disabled {
    opacity: 0.5;
    cursor: default;
  }
`;
