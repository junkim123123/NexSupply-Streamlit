# NexSupply Mobile

NexSupply B2B 소싱 인텔리전스 플랫폼의 모바일 앱입니다.

## 기능

- 🤖 AI 기반 제품 분석
- 💰 비용 분석 및 시장 인사이트
- ✅ 공급업체 검증
- 📊 실시간 시장 데이터
- 📧 전문가 상담 요청

## 시작하기

### 설치

```bash
npm install
```

### 실행

```bash
# 개발 서버 시작
npm start

# iOS 시뮬레이터
npm run ios

# Android 에뮬레이터
npm run android

# 웹 브라우저
npm run web
```

## 프로젝트 구조

```
nexsupply-mobile/
├── screens/          # 화면 컴포넌트
│   ├── HomeScreen.tsx
│   ├── ResultsScreen.tsx
│   └── ConsultationScreen.tsx
├── services/         # API 호출
│   └── api.ts
├── navigation/       # 네비게이션 설정
│   └── AppNavigator.tsx
└── App.tsx          # 메인 앱 컴포넌트
```

## API 엔드포인트

- `POST /api/analyze` - 제품 분석
- `POST /api/consultation` - 상담 요청

API 베이스 URL: `https://app.nexsupply.net`

