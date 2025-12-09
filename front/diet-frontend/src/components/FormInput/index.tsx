import * as S from "./styled";

type FormInputProps = {
  label: string;
  type?: "text" | "number" | "select";
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  options?: string[]; // select일 때
};

const FormInput = ({
  label,
  type = "text",
  value,
  onChange,
  placeholder,
  options,
}: FormInputProps) => {
  return (
    <S.Row>
      <S.Label>{label}</S.Label>
      {type === "select" && options ? (
        <S.Select value={value} onChange={(e) => onChange(e.target.value)}>
          <option value="">선택</option>
          {options.map((op) => (
            <option key={op}>{op}</option>
          ))}
        </S.Select>
      ) : (
        <S.Input
          type={type}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
        />
      )}
    </S.Row>
  );
};

export default FormInput;
