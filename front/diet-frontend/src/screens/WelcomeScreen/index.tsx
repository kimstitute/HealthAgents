import * as S from "./styled";

type WelcomeScreenProps = {
  onStart: () => void;
};

const WelcomeScreen = ({ onStart }: WelcomeScreenProps) => {
  return (
    <S.Container>
      <S.Card>
        <S.Illust
          src="https://images.pexels.com/photos/14843543/pexels-photo-14843543.jpeg"
          alt="다이어트 사진"
        />
        <S.Title>안녕하세요! 저는 AI 다이어트 코치에요!✨</S.Title>
        <S.Sub>
          사용자님의 건강하고 지속 가능한 다이어트를
          <br />
          끝까지 함께 도와드릴게요.
        </S.Sub>
        <S.StartButton type="button" onClick={onStart}>
          다이어트 시작하기
        </S.StartButton>
      </S.Card>
    </S.Container>
  );
};

export default WelcomeScreen;
