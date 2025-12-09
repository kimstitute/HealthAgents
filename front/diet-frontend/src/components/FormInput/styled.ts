import styled from "styled-components";

export const Row = styled.div`
  display: flex;
  flex-direction: column;
  gap: 4px;
`;

export const Label = styled.label`
  font-size: ${({ theme }) => theme.fontSizes.xs};
  color: ${({ theme }) => theme.colors.textSub};
`;

const baseField = `
  padding: 9px 11px;
  border-radius: 10px;
  border: 1px solid #d4d4d8;
  font-size: 13px;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;

  &:focus {
    border-color: #4f46e5;
    box-shadow: 0 0 0 1px rgba(79, 70, 229, 0.15);
  }
`;

export const Input = styled.input`
  ${baseField}
`;

export const Select = styled.select`
  ${baseField}
`;
