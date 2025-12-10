# Health Agents

건강 데이터 수집, 분석, 맞춤형 조언 제공을 위한 멀티에이전트 AI 시스템

## 목차

- [프로젝트 개요](#프로젝트-개요)
- [시스템 아키텍처](#시스템-아키텍처)
- [기술 스택](#기술-스택)
- [프로젝트 구조](#프로젝트-구조)
- [설치 및 실행](#설치-및-실행)
- [API 문서](#api-문서)
- [데이터 흐름](#데이터-흐름)
- [에이전트 시스템](#에이전트-시스템)
- [환경 변수](#환경-변수)
- [개발 가이드](#개발-가이드)

---

## 프로젝트 개요

Health Agents는 Android Health Connect를 통한 실시간 건강 데이터 수집, LangGraph 기반 멀티에이전트 분석, 그리고 사용자 맞춤형 건강 조언을 제공하는 통합 시스템입니다.

### 핵심 기능

- **실시간 건강 데이터 수집**: Android Health Connect API를 통한 걸음 수, 심박수, 수면, 칼로리 등 다양한 건강 지표 수집
- **멀티에이전트 AI 분석**: LangGraph를 활용한 4단계 에이전트 파이프라인을 통한 지능형 데이터 분석
- **맞춤형 조언 제공**: 사용자 프로필 및 라이프스타일 정보를 기반으로 한 개인화된 건강 조언
- **다양한 시각화**: 마크다운, 차트, 표 등 다양한 형식의 블록 기반 응답 제공
- **FCM 기반 비동기 통신**: Firebase Cloud Messaging을 통한 백엔드 주도 데이터 요청

### 시스템 특징

- **단일 사용자 시스템**: 개인 사용자 전용 시스템으로 설계되어 device_id 구분 없이 최근 데이터 자동 사용
- **LLM 통합**: 모든 에이전트가 OpenAI GPT 모델을 활용하여 지능형 처리 수행
- **효율적인 토큰 관리**: 계산 로직과 구조화된 요약을 통해 LLM 토큰 사용량 최적화
- **확장 가능한 아키텍처**: 새로운 에이전트 및 도구 추가가 용이한 모듈화된 구조

---

## 시스템 아키텍처

### 전체 시스템 구조

```
┌─────────────────────────────────────────────────────────────┐
│                    Android Application                      │
│  - Health Connect SDK 1.1.0                                │
│  - Kotlin + Jetpack Compose                                 │
│  - FCM 통합                                                 │
└───────────────────────┬───────────────────────────────────┘
                         │
                         │ FCM / REST API
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    Backend Server                           │
│  - FastAPI 0.115+                                           │
│  - LangGraph (멀티에이전트 오케스트레이션)                   │
│  - LangChain OpenAI                                         │
│  - Firebase Admin SDK                                       │
└───────────────────────┬───────────────────────────────────┘
                         │
                         │ REST API
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Application                      │
│  - React 19.2.0 + TypeScript                                │
│  - Vite 7.2.5                                              │
│  - Chart.js + styled-components                            │
└─────────────────────────────────────────────────────────────┘
```

### 멀티에이전트 파이프라인

```
User Message
    ↓
┌─────────────────────┐
│ Health Collector     │  건강 데이터 수집 및 품질 평가
│ (LLM: 데이터 평가)   │
└──────────┬───────────┘
           ↓ health_data
┌─────────────────────┐
│ Health Agent        │  통계 계산 및 데이터 분석
│ (계산 + LLM 해석)   │
└──────────┬───────────┘
           ↓ health_analysis
┌─────────────────────┐
│ Analysis Agent      │  종합 분석 및 맞춤형 조언
│ (LLM + Tools)       │
└──────────┬───────────┘
           ↓ analysis_result
┌─────────────────────┐
│ Report Agent        │  블록 생성 (JSON)
│ (LLM: 블록 생성)    │
└──────────┬───────────┘
           ↓ blocks
    Response Blocks
```

---

## 기술 스택

### Backend

| 카테고리 | 기술 | 버전 | 용도 |
|---------|------|------|------|
| **프레임워크** | FastAPI | 0.115+ | RESTful API 서버 |
| **ASGI 서버** | Uvicorn | 0.30+ | 비동기 웹 서버 |
| **에이전트 프레임워크** | LangGraph | 0.2+ | 멀티에이전트 오케스트레이션 |
| **LLM 통합** | LangChain OpenAI | 0.1+ | OpenAI API 통합 |
| **데이터 검증** | Pydantic | 2.0+ | 스키마 검증 및 직렬화 |
| **설정 관리** | Pydantic Settings | 2.6+ | 환경 변수 관리 |
| **푸시 알림** | Firebase Admin SDK | 6.5+ | FCM 메시지 전송 |

### Frontend

| 카테고리 | 기술 | 버전 | 용도 |
|---------|------|------|------|
| **UI 프레임워크** | React | 19.2.0 | 사용자 인터페이스 |
| **언어** | TypeScript | 5.9.3 | 타입 안전성 |
| **빌드 도구** | Vite | 7.2.5 | 개발 서버 및 번들링 |
| **스타일링** | styled-components | 6.1.19 | CSS-in-JS |
| **차트 라이브러리** | Chart.js | 4.5.1 | 데이터 시각화 |
| **차트 래퍼** | react-chartjs-2 | 5.3.1 | React Chart.js 통합 |
| **마크다운** | react-markdown | 10.1.0 | 마크다운 렌더링 |

### Android

| 카테고리 | 기술 | 버전 | 용도 |
|---------|------|------|------|
| **언어** | Kotlin | - | 프로그래밍 언어 |
| **UI 프레임워크** | Jetpack Compose | - | 선언적 UI |
| **아키텍처** | MVVM | - | 아키텍처 패턴 |
| **건강 데이터** | Health Connect SDK | 1.1.0 | 건강 데이터 수집 |
| **HTTP 클라이언트** | Retrofit | 2.9.0 | REST API 통신 |
| **비동기 처리** | Coroutines | 1.7.3 | 비동기 작업 |
| **백그라운드 작업** | WorkManager | - | 백그라운드 작업 관리 |

---

## 프로젝트 구조

### 전체 디렉토리 구조

```
HealthAgents/
├── Server/                      # 백엔드 서버
│   ├── app/
│   │   ├── agents/             # 멀티에이전트 시스템
│   │   │   ├── health_graph.py
│   │   │   ├── health_state.py
│   │   │   ├── health_tools.py
│   │   │   ├── prompts.py
│   │   │   ├── nodes/          # 에이전트 노드
│   │   │   └── utils/          # 유틸리티 함수
│   │   ├── api/                # API 엔드포인트
│   │   ├── services/           # 비즈니스 로직
│   │   ├── schemas/            # 데이터 모델
│   │   ├── config.py
│   │   └── main.py
│   ├── requirements.txt
│   └── *.json                  # Firebase 설정 파일
│
├── front/                       # 프론트엔드
│   └── diet-frontend/
│       ├── src/
│       │   ├── api/            # API 통신
│       │   ├── components/     # 재사용 컴포넌트
│       │   ├── screens/       # 화면 컴포넌트
│       │   ├── types/          # TypeScript 타입
│       │   ├── theme/         # 테마 및 스타일
│       │   └── utils/         # 유틸리티
│       ├── package.json
│       └── vite.config.ts
│
├── docs/                        # 문서
│   ├── COMPLETE_SYSTEM_OVERVIEW.md
│   ├── agent_architecture.md
│   ├── api_spec.md
│   ├── HEALTH_CONNECT_IMPLEMENTATION.md
│   └── workflow_final_check.md
│
└── README.md
```

### Backend 상세 구조

```
Server/app/
├── agents/                      # 멀티에이전트 시스템
│   ├── health_graph.py         # LangGraph 오케스트레이션
│   ├── health_state.py        # 공유 상태 정의 (TypedDict)
│   ├── health_tools.py         # 에이전트 도구 정의
│   ├── prompts.py              # 시스템 프롬프트 중앙 관리
│   ├── nodes/                  # 에이전트 노드 구현
│   │   ├── health_collector.py    # 데이터 수집 에이전트
│   │   ├── health_agent.py        # 데이터 분석 에이전트
│   │   ├── analysis_agent.py     # 종합 분석 에이전트
│   │   └── report_agent.py        # 리포트 생성 에이전트
│   └── utils/
│       └── data_formatter.py   # 데이터 포맷팅 유틸리티
│
├── api/                         # FastAPI 라우터
│   ├── chat_api.py             # 채팅 API (/agent/*)
│   ├── health_api.py           # 건강 데이터 API (/health/*)
│   └── fcm_api.py              # FCM 관리 API (/devices/*, /health/data/*)
│
├── services/                   # 비즈니스 로직 레이어
│   ├── fcm_service.py          # FCM 메시지 전송
│   ├── device_service.py       # 기기 및 요청 관리
│   ├── health_data_service.py  # 건강 데이터 조회
│   └── user_session_service.py # 사용자 세션 관리
│
├── schemas/                     # Pydantic 모델
│   ├── chat_data.py            # 채팅 관련 스키마
│   ├── health_data.py          # 건강 데이터 스키마
│   ├── fcm_data.py             # FCM 관련 스키마
│   ├── user_data.py            # 사용자 정보 스키마
│   └── agent_data.py           # 에이전트 내부 데이터 스키마
│
├── config.py                    # 설정 관리 (Pydantic Settings)
└── main.py                      # FastAPI 애플리케이션 진입점
```

### Frontend 상세 구조

```
front/diet-frontend/src/
├── api/
│   └── chat.ts                 # 백엔드 API 통신 함수
│
├── components/
│   ├── BlockRenderer/          # 블록 렌더링 컴포넌트
│   │   ├── index.tsx
│   │   └── styled.ts
│   ├── ChatBubble/            # 채팅 버블 UI 컴포넌트
│   ├── ChoiceButtons/         # 선택 버튼 컴포넌트
│   └── FormInput/             # 입력 폼 컴포넌트
│
├── screens/
│   ├── WelcomeScreen/         # 환영 화면
│   ├── BasicInfoScreen/       # 기본 정보 입력 화면
│   ├── LifestyleSurveyScreen/ # 라이프스타일 설문 화면
│   └── CoachChatScreen/       # AI 코치 채팅 화면
│
├── types/
│   ├── blocks.ts              # 블록 타입 정의
│   └── survey.ts              # 설문 타입 정의
│
├── theme/                      # 테마 및 글로벌 스타일
│   ├── GlobalStyle.ts
│   ├── theme.ts
│   └── styled.d.ts
│
├── utils/
│   └── format.ts              # 포맷팅 유틸리티
│
├── App.tsx                     # 메인 애플리케이션 컴포넌트
└── main.tsx                    # 애플리케이션 진입점
```

---

## 설치 및 실행

### 사전 요구사항

- **Python**: 3.10 이상
- **Node.js**: 18.0.0 이상
- **npm** 또는 **yarn**
- **Conda** (권장, Python 환경 관리)
- **Android Studio** (안드로이드 앱 개발용)
- **Firebase 프로젝트** (FCM 사용 시)

### Backend 설치 및 실행

#### 1. Python 환경 설정

```bash
# Conda 환경 생성 (권장)
conda create -n quantagents python=3.10
conda activate quantagents

# 또는 venv 사용
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

#### 2. 의존성 설치

```bash
cd Server
pip install -r requirements.txt
```

#### 3. 환경 변수 설정

프로젝트 루트 또는 `Server/` 디렉토리에 `.env` 파일 생성:

```env
# OpenAI API 설정
OPENAI_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.7

# Firebase 설정
FIREBASE_SERVICE_ACCOUNT_PATH=path/to/firebase-service-account.json
```

#### 4. Firebase 설정

1. Firebase Console에서 서비스 계정 키 다운로드
2. `FIREBASE_SERVICE_ACCOUNT_PATH`에 경로 설정
3. 또는 `Server/` 디렉토리에 직접 배치

#### 5. 서버 실행

```bash
# 개발 모드 (자동 리로드)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 프로덕션 모드
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

서버가 정상적으로 시작되면 다음 URL에서 접근 가능:
- API 문서: `http://localhost:8000/docs`
- 대체 문서: `http://localhost:8000/redoc`

### Frontend 설치 및 실행

#### 1. 의존성 설치

```bash
cd front/diet-frontend
npm install
```

#### 2. 환경 변수 설정 (선택)

프로젝트 루트에 `.env` 파일 생성:

```env
VITE_API_BASE_URL=http://localhost:8000
```

설정하지 않으면 기본값 `http://localhost:8000` 사용

#### 3. 개발 서버 실행

```bash
npm run dev
```

개발 서버가 시작되면 브라우저에서 `http://localhost:5173` 접속

#### 4. 프로덕션 빌드

```bash
npm run build
```

빌드 결과물은 `dist/` 디렉토리에 생성됩니다.

### Android 앱 실행

Android Studio에서 프로젝트를 열고 실행합니다. 자세한 내용은 `docs/HEALTH_CONNECT_IMPLEMENTATION.md`를 참조하세요.

---

## API 문서

### Base URL

```
http://localhost:8000
```

### 주요 엔드포인트

#### 1. 사용자 정보 초기화

**`POST /agent/plan/init`**

사전 질문 완료 후 사용자 정보를 백엔드에 저장합니다.

**Request Body:**
```json
{
  "user_name": "강진희",
  "basicInfo": {
    "age": "25",
    "gender": "여성",
    "height": "165",
    "weight": "60",
    "period": "4",
    "targetLoss": "5"
  },
  "lifestyle": {
    "exerciseFreq": "3",
    "mealsPerDay": "3",
    "nightSnackFreq": "자주",
    "eatingOutFreq": "가끔",
    "healthNotes": "없음"
  },
  "followup": {
    "q1": "야식 끊기",
    "q2": "유산소 선호",
    "q3": "아침 식사는 꼭 밥으로"
  },
  "device_id": null
}
```

**Response:**
```json
{
  "status": "success",
  "message": "사용자 정보가 저장되었습니다.",
  "session_id": "abc123def456"
}
```

#### 2. 채팅 메시지 처리

**`POST /agent/chat`**

사용자 메시지를 받아 멀티에이전트 파이프라인을 통해 분석 결과를 블록 배열로 반환합니다.

**Request Body:**
```json
{
  "message": "오늘 건강 상태 알려줘",
  "device_id": null
}
```

**Response:**
```json
{
  "blocks": [
    {
      "type": "markdown",
      "content": "## 건강 상태 요약\n\n2025-12-10일 기준으로..."
    },
    {
      "type": "chart",
      "chartType": "bar",
      "title": "걸음 수 (2025-12-10)",
      "data": {
        "labels": ["걸음 수"],
        "values": [8500]
      },
      "description": "총 8,500보, 평균 8,500보"
    },
    {
      "type": "table",
      "title": "건강 데이터 요약 (2025-12-10)",
      "headers": ["항목", "값", "상태"],
      "rows": [
        ["걸음 수 (평균)", "8,500보", "정상"],
        ["심박수 (평균)", "72bpm", "정상"],
        ["수면 시간 (평균)", "7.5시간", "정상"]
      ]
    }
  ]
}
```

#### 3. 건강 데이터 수신

**`POST /health/data`**

안드로이드 앱으로부터 건강 데이터를 직접 수신합니다.

**Request Body:**
```json
{
  "user_id": "user123",
  "device_id": "547c177250466685",
  "timestamp": "2025-12-10T12:00:00Z",
  "steps": {
    "count": 8500,
    "date": "2025-12-10"
  },
  "heart_rate": {
    "bpm": 72,
    "timestamp": "2025-12-10T12:00:00Z"
  },
  "sleep": {
    "hours": 7.5,
    "start_time": "2025-12-09T23:00:00Z",
    "end_time": "2025-12-10T06:30:00Z"
  },
  "calories": {
    "active": 500,
    "date": "2025-12-10"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Data received and saved"
}
```

#### 4. FCM 기기 등록

**`POST /devices/register`**

안드로이드 앱의 FCM 토큰을 등록합니다.

**Request Body:**
```json
{
  "device_id": "547c177250466685",
  "fcm_token": "eCkBmt7CRqeFB-A0fvQ6EY:APA91b...",
  "user_id": null
}
```

#### 5. 건강 데이터 요청 (FCM)

**`POST /health/data/request`**

FCM을 통해 안드로이드 앱에 건강 데이터 수집을 요청합니다.

**Request Body:**
```json
{
  "device_id": "547c177250466685",
  "data_types": ["steps", "heart_rate", "sleep"],
  "start_date": "2025-12-10",
  "end_date": "2025-12-10"
}
```

**Response:**
```json
{
  "request_id": "req_20251210_120000_547c1772",
  "status": "sent",
  "message": "Request sent via FCM"
}
```

#### 6. 건강 데이터 응답 수신 (FCM)

**`POST /health/data/response`**

FCM 요청에 대한 안드로이드 앱의 응답을 수신합니다.

자세한 API 명세는 `docs/api_spec.md`를 참조하세요.

---

## 데이터 흐름

### 전체 데이터 흐름도

```
┌──────────────────────────────────────────────────────────────┐
│                    Android Application                        │
│                                                               │
│  1. Health Connect에서 데이터 수집                            │
│  2. POST /health/data 또는 POST /health/data/response         │
│  3. RequestedHealthData 형식으로 변환하여 전송                │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ↓ HTTP POST
┌──────────────────────────────────────────────────────────────┐
│                    Backend Server                            │
│                                                               │
│  health_api.py                                                │
│    ├─ HealthDataRequest 수신                                  │
│    ├─ RequestedHealthData로 변환                             │
│    ├─ device_service.save_data_response()                    │
│    └─ _data_responses 메모리 저장소에 저장                    │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ↓
┌──────────────────────────────────────────────────────────────┐
│                    Frontend Application                       │
│                                                               │
│  1. WelcomeScreen → BasicInfoScreen → LifestyleSurveyScreen   │
│  2. CoachChatScreen: 사전 질문 3개 (Q1, Q2, Q3)              │
│  3. POST /agent/plan/init                                     │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ↓ HTTP POST
┌──────────────────────────────────────────────────────────────┐
│                    Backend Server                            │
│                                                               │
│  chat_api.py                                                  │
│    ├─ PlanRequest 수신                                        │
│    ├─ user_session_service.save_user_session()               │
│    └─ _user_sessions 메모리 저장소에 저장                    │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ↓
┌──────────────────────────────────────────────────────────────┐
│                    Frontend Application                       │
│                                                               │
│  사용자 채팅 메시지 입력                                      │
│  POST /agent/chat                                             │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ↓ HTTP POST
┌──────────────────────────────────────────────────────────────┐
│                    Backend - HealthGraph                      │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Health Collector                                     │    │
│  │   ├─ get_latest_user_session()                       │    │
│  │   │   └─ 사용자 정보 조회 (basic_info, lifestyle)    │    │
│  │   ├─ get_latest_health_data()                        │    │
│  │   │   └─ 건강 데이터 조회                            │    │
│  │   └─ LLM: 데이터 품질 평가                           │    │
│  │   → HealthState에 health_data 주입                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                        ↓                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Health Agent                                        │    │
│  │   ├─ filter_data_by_date("2025-12-10")             │    │
│  │   ├─ analyze_steps() → StepsSummary                │    │
│  │   ├─ analyze_heart_rate() → HeartRateSummary        │    │
│  │   ├─ analyze_sleep() → SleepSummary                │    │
│  │   ├─ detect_anomalies() → List[Anomaly]           │    │
│  │   ├─ analyze_trends() → List[Trend]                │    │
│  │   └─ LLM: 계산 결과 해석                            │    │
│  │   → HealthState에 health_analysis 주입             │    │
│  └─────────────────────────────────────────────────────┘    │
│                        ↓                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Analysis Agent                                      │    │
│  │   ├─ 사용자 정보 + 건강 분석 결과 조합              │    │
│  │   ├─ Tools 호출 (선택적):                           │    │
│  │   │   ├─ get_health_analysis_summary()             │    │
│  │   │   ├─ get_anomalies()                           │    │
│  │   │   └─ get_trends()                              │    │
│  │   └─ LLM: 맞춤형 종합 분석                          │    │
│  │   → HealthState에 analysis_result 주입              │    │
│  └─────────────────────────────────────────────────────┘    │
│                        ↓                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Report Agent                                        │    │
│  │   ├─ analysis_result + health_analysis 조합        │    │
│  │   ├─ LLM: JSON 형식 블록 생성                      │    │
│  │   │   └─ { markdown, charts, tables }              │    │
│  │   └─ JSON 파싱 실패 시 폴백 메커니즘               │    │
│  │   → HealthState에 blocks 주입                       │    │
│  └─────────────────────────────────────────────────────┘    │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ↓ HTTP Response
┌──────────────────────────────────────────────────────────────┐
│                    Frontend Application                       │
│                                                               │
│  BlockRenderer                                                │
│    ├─ MarkdownBlock → ReactMarkdown 컴포넌트                 │
│    ├─ ChartBlock → Chart.js (bar, line, doughnut, etc.)     │
│    ├─ TableBlock → HTML <table>                              │
│    └─ ImageBlock → <img> 태그                                 │
└──────────────────────────────────────────────────────────────┘
```

### HealthState 데이터 변환 과정

```
초기 상태:
{
  messages: [HumanMessage("오늘 건강 상태 알려줘")]
}
    ↓
[Health Collector]
{
  messages: [...],
  health_data: RequestedHealthData {
    steps: [DailyStepsData(...)],
    heart_rate: [HeartRateDataPoint(...)],
    sleep: [SleepDataPoint(...)]
  },
  user_name: "강진희",
  basic_info: BasicInfo {...},
  lifestyle: Lifestyle {...},
  followup_answers: FollowupAnswers {...}
}
    ↓
[Health Agent]
{
  ...,
  health_analysis: HealthAnalysis {
    steps_summary: StepsSummary {...},
    heart_rate_summary: HeartRateSummary {...},
    sleep_summary: SleepSummary {...},
    anomalies: [Anomaly(...)],
    trends: [Trend(...)]
  }
}
    ↓
[Analysis Agent]
{
  ...,
  analysis_result: AnalysisResult {
    summary: "종합 분석 텍스트...",
    insights: [...],
    recommendations: [...],
    concerns: [...]
  }
}
    ↓
[Report Agent]
{
  ...,
  blocks: [
    MarkdownBlock {...},
    ChartBlock {...},
    TableBlock {...}
  ]
}
```

---

## 에이전트 시스템

### 에이전트 개요

Health Agents 시스템은 LangGraph를 기반으로 한 4단계 에이전트 파이프라인으로 구성됩니다. 각 에이전트는 특정 역할을 담당하며, HealthState를 통해 데이터를 공유합니다.

### 에이전트 상세

#### 1. Health Data Collector

**책임**: 건강 데이터 수집 및 품질 평가

**입력**:
- `device_id` (선택): 기기 ID

**처리 로직**:
1. `get_latest_health_data()`: 가장 최근 건강 데이터 조회
   - device_id가 있으면 해당 기기 데이터 조회
   - 없으면 모든 데이터 중 최신 데이터 조회
2. LLM을 통한 데이터 품질 평가
   - 데이터 완전성 검증
   - 분석 가능성 판단

**출력**:
- `health_data`: RequestedHealthData
- `messages`: LLM 평가 메시지

**시스템 프롬프트**:
```
당신은 건강 데이터 수집 전문가입니다.
수집된 건강 데이터의 품질과 완전성을 평가하고 요약하세요.
중요: 워치 결측값 문제로 인해 2025-12-10일 데이터만 유효합니다.
```

#### 2. Health Agent

**책임**: 건강 데이터 분석 및 통계 계산

**입력**:
- `health_data`: RequestedHealthData

**처리 로직**:
1. **데이터 필터링**: `filter_data_by_date("2025-12-10")`
2. **통계 계산**:
   - `analyze_steps()`: 걸음 수 통계 (총합, 평균, 목표 달성률, 트렌드)
   - `analyze_heart_rate()`: 심박수 통계 (평균, 최고/최저, 안정/활동 심박수, 변동성)
   - `analyze_sleep()`: 수면 통계 (평균 시간, 일정성, 부족한 날)
3. **이상 징후 탐지**: `detect_anomalies()`
   - 평균 대비 편차가 큰 데이터 포인트 식별
   - 심각도 분류 (low, medium, high)
4. **트렌드 분석**: `analyze_trends()`
   - 시간에 따른 변화율 계산
   - 증가/감소/안정 트렌드 판단
5. **LLM 해석**: 계산된 통계를 LLM이 해석하여 구조화된 분석 생성

**출력**:
- `health_analysis`: HealthAnalysis
- `messages`: LLM 해석 메시지

**생성 데이터 구조**:
```python
HealthAnalysis {
    steps_summary: {
        total: int,              # 총 걸음 수
        average: float,          # 평균 걸음 수
        days_with_data: int,     # 데이터가 있는 일수
        trend: str,              # "increasing" | "decreasing" | "stable"
        goal_achievement: float, # 목표 달성률 (0.0 ~ 1.0)
        anomaly_days: List[str]  # 이상 징후가 있는 날짜 목록
    },
    heart_rate_summary: {
        average: float,          # 평균 심박수
        max: int,                # 최고 심박수
        min: int,                # 최저 심박수
        resting_avg: float,      # 안정 심박수 평균
        active_avg: float,       # 활동 심박수 평균
        variability: str        # "low" | "normal" | "high"
    },
    sleep_summary: {
        average_hours: float,    # 평균 수면 시간
        total_nights: int,       # 수면 데이터가 있는 날 수
        consistency: float,     # 수면 패턴 일정성 (0.0 ~ 1.0)
        insufficient_nights: int # 수면 부족한 날 수
    },
    anomalies: [
        {
            type: str,           # "low_steps" | "high_heart_rate" | "insufficient_sleep"
            date: str,           # 날짜
            severity: str,       # "low" | "medium" | "high"
            description: str     # 설명
        }
    ],
    trends: [
        {
            metric: str,         # "steps" | "heart_rate" | "sleep"
            direction: str,      # "increasing" | "decreasing"
            change_percent: float, # 변화율 (%)
            period: str          # "day" | "week" | "month"
        }
    ]
}
```

#### 3. Analysis Agent

**책임**: 종합 분석 및 맞춤형 조언 생성

**입력**:
- `health_analysis`: HealthAnalysis
- `basic_info`: BasicInfo
- `lifestyle`: Lifestyle
- `followup_answers`: FollowupAnswers
- `messages`: 사용자 메시지

**처리 로직**:
1. **컨텍스트 구성**: 사용자 정보와 건강 분석 결과를 조합
2. **Tools 호출** (LLM이 필요에 따라 결정):
   - `get_health_analysis_summary()`: 건강 분석 요약
   - `get_anomalies()`: 이상 징후 목록
   - `get_trends()`: 트렌드 목록
3. **LLM 종합 분석**:
   - 사용자의 목표, 라이프스타일, 건강 상태를 종합 고려
   - 맞춤형 건강 조언 생성
   - 우려사항 식별

**출력**:
- `analysis_result`: AnalysisResult
- `messages`: LLM 분석 메시지

**시스템 프롬프트**:
```
당신은 건강 데이터 분석 전문가입니다.
건강 데이터 분석 결과와 사용자 정보를 바탕으로 맞춤형 종합 분석과 조언을 제공하세요.
중요: 워치 결측값 문제로 인해 2025-12-10일 데이터만 분석 대상입니다.
```

#### 4. Report Agent

**책임**: 사용자 친화적인 리포트 블록 생성

**입력**:
- `analysis_result`: AnalysisResult
- `health_analysis`: HealthAnalysis
- `messages`: 사용자 메시지

**처리 로직**:
1. **LLM 블록 생성**: JSON 형식으로 블록 생성 요청
   ```json
   {
     "markdown": "마크다운 텍스트",
     "charts": [
       {
         "type": "bar",
         "title": "제목",
         "labels": [...],
         "values": [...],
         "description": "..."
       }
     ],
     "tables": [
       {
         "title": "제목",
         "headers": [...],
         "rows": [...]
       }
     ]
   }
   ```
2. **JSON 파싱**: LLM 응답을 파싱하여 Block 객체 생성
3. **폴백 메커니즘**: JSON 파싱 실패 시 기존 로직 사용
   - `create_chart_blocks()`: HealthAnalysis에서 ChartBlock 생성
   - `create_table_blocks()`: HealthAnalysis에서 TableBlock 생성

**출력**:
- `blocks`: List[Block]
  - MarkdownBlock
  - ChartBlock (bar, line, doughnut, pie, radar)
  - TableBlock

**시스템 프롬프트**:
```
당신은 건강 리포트 생성 전문가입니다.
분석 결과를 바탕으로 사용자 친화적인 리포트 블록을 생성하세요.
다음 형식의 JSON으로 응답하세요: { markdown, charts, tables }
```

### Tools

에이전트가 사용할 수 있는 도구들:

#### `get_health_analysis_summary`
건강 분석 결과의 요약을 반환합니다.

**입력**: `health_analysis: Dict[str, Any]`

**출력**: 요약 텍스트 (예: "걸음 수: 평균 8500보, 목표 달성률 85% | 심박수: 평균 72bpm")

#### `get_anomalies`
건강 분석 결과에서 이상 징후를 반환합니다.

**입력**: `health_analysis: Dict[str, Any]`

**출력**: 이상 징후 목록
```python
[
  {
    "type": "low_steps",
    "date": "2025-12-10",
    "severity": "medium",
    "description": "걸음 수가 평균보다 낮음"
  }
]
```

#### `get_trends`
건강 분석 결과에서 트렌드를 반환합니다.

**입력**: `health_analysis: Dict[str, Any]`

**출력**: 트렌드 목록
```python
[
  {
    "metric": "steps",
    "direction": "increasing",
    "change_percent": 15.5,
    "period": "day"
  }
]
```

---

## 환경 변수

### Backend 환경 변수

`Server/.env` 파일 또는 환경 변수로 설정:

```env
# OpenAI API 설정
OPENAI_API_KEY=sk-...                    # 필수: OpenAI API 키
LLM_MODEL=gpt-4o-mini                    # 기본값: gpt-4o-mini
LLM_TEMPERATURE=0.7                       # 기본값: 0.7

# Firebase 설정
FIREBASE_SERVICE_ACCOUNT_PATH=./healthagents-a379b-firebase-adminsdk-fbsvc-98946ab443.json
                                          # Firebase 서비스 계정 키 경로

# 애플리케이션 설정
APP_NAME=Health Agents                    # 기본값: Health Agents
```

### Frontend 환경 변수

`front/diet-frontend/.env` 파일:

```env
VITE_API_BASE_URL=http://localhost:8000  # 백엔드 API 기본 URL
```

---

## 개발 가이드

### 코드 스타일

- **Python**: PEP 8 준수, 타입 힌트 사용
- **TypeScript**: ESLint 규칙 준수, strict 모드 활성화
- **주석**: 한국어 주석 사용, 불필요한 주석 최소화

### 새로운 에이전트 추가

1. `Server/app/agents/nodes/` 디렉토리에 새 노드 파일 생성
2. `create_*_agent(llm)` 함수 구현
3. `Server/app/agents/health_graph.py`에 노드 추가 및 엣지 연결
4. 필요시 `Server/app/agents/prompts.py`에 프롬프트 추가

### 새로운 Tool 추가

1. `Server/app/agents/health_tools.py`에 `@tool` 데코레이터로 함수 정의
2. `HEALTH_TOOLS` 리스트에 추가
3. 에이전트에서 `llm.bind_tools(HEALTH_TOOLS)` 사용

### 새로운 블록 타입 추가

1. `front/diet-frontend/src/types/blocks.ts`에 타입 정의
2. `front/diet-frontend/src/components/BlockRenderer/index.tsx`에 렌더링 로직 추가
3. `Server/app/schemas/chat_data.py`에 Pydantic 모델 추가

### 디버깅

#### Backend 로깅

백엔드는 DEBUG 레벨로 로깅이 설정되어 있습니다:
```python
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
```

#### Frontend 디버깅

브라우저 개발자 도구 사용:
- **Console**: JavaScript 오류 및 로그 확인
- **Network**: API 요청/응답 확인
- **React DevTools**: 컴포넌트 상태 확인

---

## 주요 제약사항

### 데이터 날짜 제한

현재 시스템은 워치 결측값 문제로 인해 **2025-12-10일 데이터만** 처리합니다.

- `data_formatter.py`의 `filter_data_by_date()` 함수로 자동 필터링
- 모든 시스템 프롬프트에 명시
- 향후 데이터 품질 개선 시 제한 해제 가능

### 메모리 기반 저장소

현재 모든 데이터는 메모리에 저장됩니다:
- `_user_sessions`: 사용자 세션 정보
- `_data_responses`: 건강 데이터 응답
- `_data_requests`: 데이터 요청 상태
- `_device_tokens`: 기기 FCM 토큰

**영향**: 서버 재시작 시 모든 데이터가 초기화됩니다.

**해결 방안**: 프로덕션 환경에서는 데이터베이스 연동 필요 (PostgreSQL, MongoDB 등)

### 단일 사용자 시스템

현재는 단일 사용자를 위한 시스템으로 설계되어 있습니다:
- device_id 구분 없이 최근 데이터 자동 사용
- 사용자 인증 없음
- 멀티 사용자 지원 시 확장 필요

---

## 테스트

### Backend API 테스트

```bash
# FCM 플로우 테스트
cd Server
python test_real_fcm.py

# 통합 테스트
python test_and_check_data.py
```

### Frontend 테스트

```bash
cd front/diet-frontend
npm run dev
# 브라우저에서 수동 테스트
```

---

## 배포

### Backend 배포

1. 프로덕션 환경 변수 설정
2. 데이터베이스 연동 (선택)
3. Gunicorn 또는 유사한 프로덕션 ASGI 서버 사용

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend 배포

```bash
cd front/diet-frontend
npm run build
# dist/ 디렉토리를 정적 호스팅 서비스에 배포
```

---

## 라이선스

이 프로젝트는 교육 목적으로 개발되었습니다.

---

## 참고 문서

- [시스템 전체 개요](./docs/COMPLETE_SYSTEM_OVERVIEW.md)
- [에이전트 아키텍처](./docs/agent_architecture.md)
- [API 명세서](./docs/api_spec.md)
- [Health Connect 구현 가이드](./docs/HEALTH_CONNECT_IMPLEMENTATION.md)
- [프론트엔드 실행 가이드](./front/diet-frontend/FRONTEND_GUIDE.md)

---

## 기여

이 프로젝트는 학술 연구 목적으로 개발되었습니다.

---

## 문의

프로젝트 관련 문의사항은 이슈를 통해 제출해주세요.
