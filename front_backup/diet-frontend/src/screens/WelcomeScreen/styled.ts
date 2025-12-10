import styled from "styled-components";

export const Container = styled.div`
  height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #fee2e2, #e0f2fe);
  display: flex;
  justify-content: center;
  align-items: center;
`;

export const Card = styled.div`
  background: ${({ theme }) => theme.colors.cardBg};
  border-radius: 24px;
  padding: 32px 32px 28px;
  box-shadow: ${({ theme }) => theme.shadows.soft};
  text-align: center;
  max-width: 420px;
  width: 90%;
  animation: fadeIn 0.7s ease-out;

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(14px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

export const Illust = styled.img`
  width: 260px;
  height: 180px;
  object-fit: cover;
  border-radius: 18px;
  margin-bottom: 20px;
`;

export const Title = styled.h1`
  font-size: ${({ theme }) => theme.fontSizes.title};
  margin: 0 0 10px;
`;

export const Sub = styled.p`
  margin: 0;
  font-size: ${({ theme }) => theme.fontSizes.sm};
  color: ${({ theme }) => theme.colors.textSub};
  line-height: 1.5;
`;

export const StartButton = styled.button`
  margin-top: 22px;
  padding: 12px 26px;
  border-radius: ${({ theme }) => theme.radii.pill};
  border: none;
  background: ${({ theme }) => theme.colors.accent};
  color: white;
  font-size: ${({ theme }) => theme.fontSizes.md};
  font-weight: 600;
  cursor: pointer;
  transition: background 0.18s, transform 0.12s;

  &:hover {
    background: #f97373;
    transform: translateY(-1px);
  }

  &:active {
    transform: translateY(0);
  }
`;
