# NexSupply 완벽 가이드 - Vercel 해결 포함

**ALL-IN-ONE 가이드 | 최종 버전: 2025년 11월 28일**

---

## 📑 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [PWA 구현](#pwa-구현)
3. [TWA 빌드](#twa-빌드)
4. [Vercel assetlinks.json 배치](#vercel-assetlinksjson-배치)
5. [Google Play Store 출시](#google-play-store-출시)
6. [1주일 실행 계획](#1주일-실행-계획)

---

## 프로젝트 개요

### NexSupply 핵심 메시지

> **One Photo. Real Landed Cost. No Surprises.**

Upload a product photo or Alibaba link → Get:
- ✅ Landed Cost (±20-30% accuracy)
- ✅ Verified Suppliers (risk scores)
- ✅ Leadtime Breakdown (11-13 weeks detail)
- ✅ Expert Consultation (Pro plan)

**Result:** Save $10K-100K per sourcing project

### 타겟 시장

- **Primary:** Amazon FBA 셀러 (150K 명)
- **Secondary:** Shopify 상인 (200K 명)
- **Tertiary:** 전통 소매 바이어 (150K 명)

---

## PWA 구현

### 완료된 작업

- ✅ `manifest.json` 생성 (프로젝트 루트)
- ✅ `service-worker.js` 생성 (프로젝트 루트)
- ✅ `streamlit_app.py`에 PWA 메타 태그 추가
- ✅ `.streamlit/config.toml`에 `enableStaticServing = true` 설정

### 파일 구조

```
nexsupply-platform/
├── manifest.json          # PWA 매니페스트
├── service-worker.js      # Service Worker
├── streamlit_app.py       # PWA 메타 태그 포함
├── .streamlit/
│   └── config.toml        # enableStaticServing = true
└── .well-known/
    └── assetlinks.json    # TWA 보안 파일
```

---

## TWA 빌드

### Bubblewrap 설치

```bash
npm install -g @bubblewrap/cli
```

### TWA 프로젝트 초기화

```bash
mkdir nexsupply-twa
cd nexsupply-twa
bubblewrap init --manifest=https://app.nexsupply.app/manifest.json
```

### APK/AAB 빌드

```bash
bubblewrap build
```

**생성된 파일:**
- `app-release-signed.apk`
- `app-release-bundle.aab`
- `assetlinks.json` (중요!)

---

## Vercel assetlinks.json 배치

### 문제: 404 오류

**원인:**
1. 파일이 실제로 배포되지 않음
2. MIME 타입이 올바르지 않음
3. 파일 경로가 잘못됨

### 해결: vercel.json 설정

프로젝트 루트에 `vercel.json` 생성:

```json
{
  "version": 2,
  "headers": [
    {
      "source": "/.well-known/assetlinks.json",
      "headers": [
        {
          "key": "Content-Type",
          "value": "application/json; charset=utf-8"
        },
        {
          "key": "Cache-Control",
          "value": "public, max-age=86400, immutable"
        },
        {
          "key": "Content-Disposition",
          "value": "inline"
        },
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        }
      ]
    },
    {
      "source": "/manifest.json",
      "headers": [
        {
          "key": "Content-Type",
          "value": "application/json; charset=utf-8"
        }
      ]
    },
    {
      "source": "/service-worker.js",
      "headers": [
        {
          "key": "Content-Type",
          "value": "application/javascript; charset=utf-8"
        },
        {
          "key": "Cache-Control",
          "value": "public, max-age=0"
        }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### 배포 및 확인

1. **Git 푸시**
   ```bash
   git add vercel.json
   git commit -m "Add vercel.json with assetlinks.json headers"
   git push origin main
   ```

2. **Vercel 자동 재배포** (1-2분)

3. **테스트**
   ```
   https://your-domain.vercel.app/.well-known/assetlinks.json
   ```

4. **성공 확인**
   - HTTP 200 OK
   - Content-Type: `application/json; charset=utf-8`
   - JSON 내용 표시

---

## Google Play Store 출시

### 1단계: Developer Account 생성

- [Google Play Console](https://play.google.com/console) 접속
- $25 결제 (Developer Account 등록비)

### 2단계: 앱 정보 입력

- Package name: `com.nexsupply.app`
- 앱 이름: `NexSupply`
- 약식 설명: `AI로 중국 소싱 비용을 40초 만에 계산하세요.`
- 전체 설명: (앱 상세 설명)

### 3단계: AAB 파일 업로드

- `nexsupply-twa/app-release-bundle.aab` 업로드
- 출시 노트 작성

### 4단계: 출시

- 모든 필수 정보 입력 확인
- "출시" 버튼 클릭
- 심사 대기 (2-3일)

---

## 1주일 실행 계획

### Day 1: PWA 구현 ✅

- [x] manifest.json 생성
- [x] service-worker.js 생성
- [x] streamlit_app.py 수정
- [x] Git 커밋 및 푸시

### Day 2-3: PWA 검증

- [ ] Streamlit Cloud 배포
- [ ] Chrome DevTools에서 PWA 검증
- [ ] "홈 화면에 추가" 테스트

### Day 4: TWA 빌드

- [ ] Bubblewrap 설치
- [ ] TWA 프로젝트 초기화
- [ ] APK/AAB 빌드
- [ ] assetlinks.json 생성

### Day 5: assetlinks.json 배치

- [x] vercel.json 설정
- [x] Git 푸시
- [ ] Vercel 재배포 확인
- [ ] URL 접근 테스트 (200 OK)

### Day 6-7: Google Play Store 등록

- [ ] Developer Account 생성
- [ ] 앱 정보 입력
- [ ] AAB 파일 업로드
- [ ] 출시

### Day 8-10: 심사 & 출시

- [ ] Google Play 자동 심사
- [ ] 심사 통과 알림
- [ ] Play Store에서 검색 가능
- [ ] 사용자 다운로드 가능 🎉

---

## ✅ 최종 체크리스트

### PWA
- [x] manifest.json 생성
- [x] service-worker.js 생성
- [x] PWA 메타 태그 추가
- [x] Streamlit Cloud 배포

### TWA
- [ ] Bubblewrap 설치
- [ ] APK/AAB 빌드
- [ ] assetlinks.json 생성

### Vercel
- [x] vercel.json 설정
- [x] .well-known/assetlinks.json 배치
- [ ] URL 접근 확인 (200 OK)

### Play Store
- [ ] Developer Account 생성
- [ ] 앱 정보 입력
- [ ] AAB 업로드
- [ ] 출시

---

## 🎯 예상 결과

**1주일 후:**
- ✅ PWA 활성화 (웹에서 "홈 화면에 추가" 가능)
- ✅ Google Play Store 출시 (Android 사용자 다운로드 가능)
- ✅ 첫 100명 다운로드 목표

**1개월 후:**
- ✅ 1,000 사용자 확보
- ✅ Pro 플랜 전환 시작
- ✅ 첫 Enterprise 고객

---

## 📚 관련 문서

- `Vercel-assetlinks-404-완벽해결.md` - Vercel 404 해결 상세 가이드
- `TWA_READ_ME.md` - TWA 빌드 가이드
- `BUILD_TWA.md` - 빌드 스크립트
- `DAY1_EXECUTION_GUIDE.md` - Day 1 실행 가이드

---

**🚀 지금 바로 시작하세요! 모든 준비가 완료되었습니다!**



