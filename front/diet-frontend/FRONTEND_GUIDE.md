# 프론트엔드 실행 가이드

## 프로젝트 개요

- **프레임워크**: React 19.2.0
- **빌드 도구**: Vite (rolldown-vite 7.2.5)
- **언어**: TypeScript
- **스타일링**: styled-components 6.1.19
- **차트**: Chart.js 4.5.1 + react-chartjs-2 5.3.1
- **마크다운**: react-markdown 10.1.0

## 사전 요구사항

- Node.js 18.0.0 이상
- npm 또는 yarn

## 설치 및 실행

### 1. 의존성 설치

```bash
cd front/diet-frontend
npm install
```

### 2. 환경 변수 설정 (선택)

프로젝트 루트에 `.env` 파일을 생성하여 백엔드 API URL을 설정할 수 있습니다:

```env
VITE_API_BASE_URL=http://localhost:8000
```

설정하지 않으면 기본값 `http://localhost:8000`이 사용됩니다.

### 3. 개발 서버 실행

```bash
npm run dev
```

개발 서버가 시작되면 브라우저에서 다음 URL로 접속:
- 기본: `http://localhost:5173`

### 4. 프로덕션 빌드

```bash
npm run build
```

빌드 결과물은 `dist/` 폴더에 생성됩니다.

### 5. 프로덕션 미리보기

```bash
npm run preview
```

## 프로젝트 구조

```
diet-frontend/
├── src/
│   ├── api/
│   │   └── chat.ts              # 백엔드 API 통신
│   ├── components/
│   │   ├── BlockRenderer/        # 블록 렌더링 (Markdown, Chart, Table 등)
│   │   ├── ChatBubble/          # 채팅 버블 컴포넌트
│   │   ├── ChoiceButtons/       # 선택 버튼 컴포넌트
│   │   └── FormInput/           # 입력 폼 컴포넌트
│   ├── screens/
│   │   ├── WelcomeScreen/        # 환영 화면
│   │   ├── BasicInfoScreen/     # 기본 정보 입력 화면
│   │   ├── LifestyleSurveyScreen/ # 라이프스타일 설문 화면
│   │   └── CoachChatScreen/     # AI 코치 채팅 화면
│   ├── types/
│   │   ├── blocks.ts            # 블록 타입 정의
│   │   └── survey.ts            # 설문 타입 정의
│   ├── theme/                   # 테마 및 글로벌 스타일
│   ├── utils/                   # 유틸리티 함수
│   ├── App.tsx                  # 메인 앱 컴포넌트
│   └── main.tsx                 # 진입점
├── public/                      # 정적 파일
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## 사용 흐름

### 1. 환영 화면
- 앱 시작 시 표시
- "시작하기" 버튼 클릭

### 2. 기본 정보 입력
- 나이, 성별, 키, 체중
- 다이어트 기간, 목표 감량 체중
- "다음" 버튼 클릭

### 3. 라이프스타일 설문
- 운동 빈도, 하루 식사 횟수
- 야식 빈도, 외식 빈도
- 건강 특이사항
- "완료" 버튼 클릭

### 4. AI 코치 채팅
- 사전 질문 3개 자동 표시 (5초 후)
- 질문에 답변하면 다음 질문 표시
- 3번째 질문 답변 후 사용자 정보 백엔드 저장
- 이후 일반 채팅 모드로 전환
- 건강 데이터 기반 맞춤형 조언 제공

## API 엔드포인트

### 백엔드 연결

프론트엔드는 다음 백엔드 API를 사용합니다:

1. **POST `/agent/plan/init`**
   - 사용자 정보 초기화
   - 사전 질문 완료 후 호출
   - Request: `PlanRequest`
   - Response: `PlanResponse`

2. **POST `/agent/chat`**
   - 채팅 메시지 전송
   - Request: `{ message: string, device_id?: string }`
   - Response: `{ blocks: Block[] }`

### 환경 변수

- `VITE_API_BASE_URL`: 백엔드 API 기본 URL (기본값: `http://localhost:8000`)

## 지원하는 블록 타입

프론트엔드는 다음 블록 타입을 렌더링할 수 있습니다:

1. **MarkdownBlock**: 마크다운 텍스트
2. **ChartBlock**: 차트 (bar, line, doughnut, pie, radar)
3. **TableBlock**: 표
4. **ImageBlock**: 이미지
5. **RowBlock**: 가로 배치 블록
6. **MapBlock**: 지도 (Google Maps)
7. **AirQualityBlock**: 대기질 정보

## 문제 해결

### 포트 충돌

기본 포트 5173이 사용 중이면 Vite가 자동으로 다른 포트를 사용합니다.
터미널에 표시된 URL을 확인하세요.

### CORS 오류

백엔드 서버가 CORS를 허용하도록 설정되어 있는지 확인하세요.
FastAPI의 경우 `CORSMiddleware`가 설정되어 있어야 합니다.

### API 연결 실패

1. 백엔드 서버가 실행 중인지 확인
2. `VITE_API_BASE_URL` 환경 변수가 올바른지 확인
3. 브라우저 개발자 도구의 Network 탭에서 요청 상태 확인

### 빌드 오류

```bash
# node_modules 삭제 후 재설치
rm -rf node_modules package-lock.json
npm install
```

## 개발 팁

### Hot Module Replacement (HMR)

Vite는 기본적으로 HMR을 지원합니다.
코드 수정 시 자동으로 브라우저가 업데이트됩니다.

### 타입 체크

```bash
npm run build
```

빌드 시 TypeScript 타입 체크가 수행됩니다.

### 린트

```bash
npm run lint
```

ESLint를 사용하여 코드 스타일을 검사합니다.

## 주요 기능

### 1. 사전 질문 시스템
- 사용자 정보 수집
- 3단계 질문 플로우
- 자동 백엔드 저장

### 2. 블록 기반 렌더링
- 다양한 블록 타입 지원
- Chart.js를 통한 차트 시각화
- 반응형 디자인

### 3. 실시간 채팅
- 스크롤 자동 이동
- 로딩 상태 표시
- 에러 처리

## 다음 단계

1. 백엔드 서버 실행 확인
2. 프론트엔드 개발 서버 실행
3. 브라우저에서 `http://localhost:5173` 접속
4. 사전 질문 완료 후 채팅 시작

