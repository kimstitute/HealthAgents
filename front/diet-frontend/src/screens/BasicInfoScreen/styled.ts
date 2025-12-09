import styled from "styled-components";

export const Container = styled.div`
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px;
  background: linear-gradient(135deg, #eef2ff, #fef9c3);
`;

export const Inner = styled.div`
  background: ${({ theme }) => theme.colors.cardBg};
  border-radius: 24px;
  padding: 28px 26px 24px;
  box-shadow: ${({ theme }) => theme.shadows.soft};
  width: 100%;
  max-width: 420px;
`;

export const Title = styled.h2`
  margin: 0 0 6px;
  font-size: ${({ theme }) => theme.fontSizes.xl};
`;

export const Sub = styled.p`
  margin: 0 0 18px;
  font-size: ${({ theme }) => theme.fontSizes.sm};
  color: ${({ theme }) => theme.colors.textSub};
  line-height: 1.4;
`;

export const FormCard = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

export const NextButton = styled.button`
  width: 100%;
  margin-top: 18px;
  padding: 11px 0;
  border-radius: ${({ theme }) => theme.radii.pill};
  border: none;
  background: ${({ theme }) => theme.colors.primary};
  color: #fff;
  font-weight: 600;
  font-size: ${({ theme }) => theme.fontSizes.sm};
  cursor: pointer;
  transition: 0.16s;

  &:hover {
    background: #4338ca;
    transform: translateY(-1px);
  }

  &:active {
    transform: translateY(0);
  }
`;
