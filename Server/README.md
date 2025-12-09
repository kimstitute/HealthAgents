# Health Agents Backend

FastAPI 기반 건강 관리 에이전트 백엔드 서버

## 요구사항

- Python 3.10+

## 설치

```bash
cd Server
pip install -r requirements.txt
```

## 실행

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API 문서

서버 실행 후 접속:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| POST | /agent/chat | 채팅 요청/응답 |

상세 명세: [docs/api_spec.md](../docs/api_spec.md)

## 테스트

```bash
curl -X POST http://localhost:8000/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "이번 주 걸음 수 분석해줘"}'
```

