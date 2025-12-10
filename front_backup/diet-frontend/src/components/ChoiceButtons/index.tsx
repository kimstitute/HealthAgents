import * as S from "./styled";

type ChoiceButtonsProps = {
  options: string[];
  onSelect: (value: string) => void;
};

const ChoiceButtons = ({ options, onSelect }: ChoiceButtonsProps) => {
  return (
    <S.Wrapper>
      {options.map((opt) => (
        <S.Button key={opt} type="button" onClick={() => onSelect(opt)}>
          {opt}
        </S.Button>
      ))}
    </S.Wrapper>
  );
};

export default ChoiceButtons;
