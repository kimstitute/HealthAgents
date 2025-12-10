import styled from "styled-components";

export const Container = styled.div`
  min-height: 100vh;
  padding: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: radial-gradient(circle at top, #fee2e2, #eef2ff);
`;

export const Inner = styled.div`
  background: ${({ theme }) => theme.colors.cardBg};
  border-radius: 24px;
  padding: 24px 22px 22px;
  box-shadow: ${({ theme }) => theme.shadows.soft};
  max-width: 420px;
  width: 100%;
`;

export const Header = styled.h2`
  margin: 0 0 14px;
  font-size: ${({ theme }) => theme.fontSizes.lg};
`;

export const ChatArea = styled.div`
  margin-top: 4px;
`;

export const TextBlock = styled.div`
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

export const TextArea = styled.textarea`
  min-height: 120px;
  border-radius: 12px;
  border: 1px solid #d4d4d8;
  padding: 10px 12px;
  font-size: ${({ theme }) => theme.fontSizes.sm};
  resize: vertical;
  outline: none;

  &:focus {
    border-color: ${({ theme }) => theme.colors.primary};
    box-shadow: 0 0 0 1px rgba(79, 70, 229, 0.18);
  }
`;

export const SubmitButton = styled.button`
  align-self: flex-end;
  padding: 8px 16px;
  border-radius: ${({ theme }) => theme.radii.pill};
  border: none;
  background: ${({ theme }) => theme.colors.primary};
  color: #fff;
  font-size: ${({ theme }) => theme.fontSizes.sm};
  font-weight: 500;
  cursor: pointer;
`;
