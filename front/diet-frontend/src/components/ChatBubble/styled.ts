import styled, { css } from "styled-components";

export const Bubble = styled.div<{
  variant: "bot" | "user" | "info";
}>`
  max-width: 360px;
  padding: 14px 16px;
  border-radius: 16px;
  line-height: 1.5;
  font-size: ${({ theme }) => theme.fontSizes.sm};
  white-space: pre-line;

  ${(p) =>
    p.variant === "bot" &&
    css`
      background: ${p.theme.colors.bubbleBot};
      color: ${p.theme.colors.textMain};
      border-bottom-left-radius: 4px;
      margin-bottom: 12px;
    `}

  ${(p) =>
    p.variant === "user" &&
    css`
      background: ${p.theme.colors.bubbleUser};
      color: #fff;
      border-bottom-right-radius: 4px;
      margin-left: auto;
      margin-bottom: 12px;
    `}

  ${(p) =>
    p.variant === "info" &&
    css`
      background: #e5e7eb;
      color: ${p.theme.colors.textMain};
      margin-bottom: 12px;
    `}
`;
