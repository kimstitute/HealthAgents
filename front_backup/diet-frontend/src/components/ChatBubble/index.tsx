import { ReactNode } from "react";
import * as S from "./styled";

type ChatBubbleProps = {
  children: ReactNode;
  variant?: "bot" | "user" | "info";
};

const ChatBubble = ({ children, variant = "bot" }: ChatBubbleProps) => {
  return <S.Bubble variant={variant}>{children}</S.Bubble>;
};

export default ChatBubble;
