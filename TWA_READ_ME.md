# NexSupply TWA 빌드 및 Google Play Store 출시 가이드

**최종 버전: 2025년 11월 28일**  
**상태: 즉시 실행 가능 ✅**

---

## 📋 목차

1. [사전 준비](#사전-준비)
2. [Bubblewrap으로 APK/AAB 빌드](#bubblewrap으로-apkab-빌드)
3. [assetlinks.json 배치](#assetlinksjson-배치)
4. [Google Play Console 등록](#google-play-console-등록)
5. [앱 등재 및 출시](#앱-등재-및-출시)
6. [문제 해결](#문제-해결)

---

## 사전 준비

### 필수 요구사항

- ✅ Node.js 설치 (v14 이상)
- ✅ Google 계정 (Play Console 등록용)
- ✅ $25 (Google Play Developer 등록비)
- ✅ Streamlit 앱이 `https://app.nexsupply.app`에서 실행 중

### 확인 사항

1. **manifest.json 확인**
   ```
   https://app.nexsupply.app/manifest.json
   ```
   브라우저에서 접속하여 JSON이 올바르게 표시되는지 확인

2. **Service Worker 확인**
   ```
   https://app.nexsupply.app/service-worker.js
   ```
   JavaScript 파일이 올바르게 로드되는지 확인

---

## Bubblewrap으로 APK/AAB 빌드

### 방법 1: 자동 스크립트 사용 (권장)

#### Windows (PowerShell)

```powershell
.\build_twa.ps1
```

#### Linux/Mac (Bash)

```bash
chmod +x build_twa.sh
./build_twa.sh
```

### 방법 2: 수동 빌드

#### 1단계: Bubblewrap 설치

```bash
npm install -g @bubblewrap/cli
```

#### 2단계: 프로젝트 초기화

```bash
mkdir nexsupply-twa
cd nexsupply-twa

bubblewrap init --manifest=https://app.nexsupply.app/manifest.json
```

**초기화 중 입력 사항:**

- **App name**: `NexSupply`
- **Package ID**: `com.nexsupply.app`
- **Host URL**: `app.nexsupply.app`
- **Create signing key**: `yes` (새 키 생성)
- **Key password**: 안전한 비밀번호 입력 (나중에 필요)

#### 3단계: APK/AAB 빌드

```bash
bubblewrap build
```

**빌드 결과:**

- `app-release-signed.apk` - 서명된 APK 파일
- `app-release-bundle.aab` - App Bundle (Play Store 업로드용)
- `assetlinks.json` - Digital Asset Links 파일

---

## assetlinks.json 배치

### 1단계: 파일 복사

빌드 후 생성된 `assetlinks.json` 파일을 프로젝트 루트의 `.well-known` 폴더로 복사:

```bash
# Windows
copy nexsupply-twa\assetlinks.json .well-known\

# Linux/Mac
cp nexsupply-twa/assetlinks.json .well-known/
```

### 2단계: Git 커밋 및 푸시

```bash
git add .well-known/assetlinks.json
git commit -m "Add assetlinks.json for TWA"
git push
```

### 3단계: 배치 확인

브라우저에서 다음 URL에 접속하여 확인:

```
https://app.nexsupply.app/.well-known/assetlinks.json
```

**확인 사항:**

- ✅ HTTP 상태 코드: 200
- ✅ Content-Type: `application/json`
- ✅ 파일 내용이 올바른 JSON 형식
- ✅ `package_name`: `com.nexsupply.app`
- ✅ `sha256_cert_fingerprints`가 올바르게 표시됨

### 4단계: Digital Asset Links 검증

Google의 검증 도구 사용:

```
https://digitalassetlinks.googleapis.com/v1/statements:list?source.web.site=https://app.nexsupply.app&relation=delegate_permission/common.handle_all_urls
```

또는 Android 명령어:

```bash
adb shell pm get-app-links com.nexsupply.app
```

---

## Google Play Console 등록

### 1단계: Developer Account 생성

1. [Google Play Console](https://play.google.com/console) 접속
2. "앱 만들기" 클릭
3. 다음 정보 입력:
   - **앱 이름**: `NexSupply`
   - **기본 언어**: 한국어 또는 영어
   - **앱 또는 게임**: 앱
   - **무료 또는 유료**: 무료
4. $25 결제 (Developer Account 등록비)
5. 팀 정보 입력

### 2단계: 앱 정보 입력

**앱 정보** 섹션에서:

- **Package name**: `com.nexsupply.app` (Bubblewrap에서 설정한 것과 동일)
- **앱 이름**: `NexSupply`
- **약식 설명**: `AI로 중국 소싱 비용을 40초 만에 계산하세요.`
- **전체 설명**: (앱의 상세 설명 작성)

**예시 전체 설명:**

```
NexSupply는 AI 기반 B2B 소싱 플랫폼입니다.

주요 기능:
✅ 착가 계산 (Landed Cost) - 40초 만에 정확한 비용 산출
✅ 공급업체 검증 - 위험도 평가 및 신뢰성 점수
✅ 리드타임 분석 - 생산 및 배송 일정 예측
✅ 전문가 상담 - Pro 플랜에서 제공

사용 방법:
1. 제품 사진 또는 Alibaba 링크 업로드
2. AI가 자동으로 분석
3. 착가, 공급업체, 리드타임 정보 확인
4. 전문가 상담 요청 (선택사항)

NexSupply로 소싱 프로젝트당 $10K-100K를 절약하세요.
```

---

## 앱 등재 및 출시

### 1단계: 콘텐츠 등급 설정

1. **콘텐츠 등급** 섹션으로 이동
2. 설문지 작성 (자동으로 등급 부여)
3. 일반적으로 "Everyone" 등급

### 2단계: 개인정보 보호 정책

**개인정보 보호 및 보안** 섹션에서:

- **개인정보 처리방침 URL**: `https://app.nexsupply.app/privacy`
- 개인정보 처리방침 페이지가 준비되어 있어야 함

### 3단계: 앱 아이콘 및 그래픽

**앱 아이콘:**

- **512x512 PNG** 이미지 필요
- 투명 배경 권장
- 파일: `icon-512.png`

**스크린샷 (최소 2개):**

- **540x720 PNG** 또는 **1080x1440 PNG**
- 앱의 주요 기능을 보여주는 이미지
- 파일: `screenshot-540.png`, `screenshot-1080.png`

**기능 그래픽 (선택사항):**

- 기능 하이라이트 이미지
- 프로모션 그래픽

### 4단계: APK/AAB 업로드

1. **프로덕션** > **새 출시 만들기** 클릭
2. **App Bundle 업로드** 선택
3. `nexsupply-twa/app-release-bundle.aab` 파일 업로드
4. 출시 노트 작성:
   ```
   첫 번째 출시
   - AI 기반 착가 계산
   - 공급업체 검증
   - 리드타임 분석
   ```
5. **검토** 클릭

### 5단계: 최종 검토 및 출시

1. 모든 필수 정보 입력 확인
2. **출시** 버튼 클릭
3. 심사 대기 (보통 2-3일)

---

## 문제 해결

### assetlinks.json이 로드되지 않음

**증상:**
- `https://app.nexsupply.app/.well-known/assetlinks.json` 접속 시 404 오류

**해결 방법:**

1. **파일 경로 확인**
   - 파일이 `.well-known/assetlinks.json`에 있는지 확인
   - 파일명이 정확한지 확인 (대소문자 구분)

2. **Streamlit Cloud 설정**
   - Streamlit Cloud가 `.well-known` 폴더를 서빙하는지 확인
   - 필요 시 서버 설정에서 정적 파일 서빙 활성화

3. **Git 커밋 확인**
   - 파일이 Git에 커밋되었는지 확인
   - `git status`로 확인

### APK 서명 오류

**증상:**
- 빌드 중 서명 오류 발생

**해결 방법:**

1. **키스토어 확인**
   - `nexsupply-twa/android.keystore` 파일 존재 확인
   - 비밀번호 정확한지 재확인

2. **Bubblewrap 업데이트**
   ```bash
   npm update -g @bubblewrap/cli
   ```

### Play Store 심사 거부

**일반적인 거부 사유:**

1. **개인정보 처리방침 누락**
   - 개인정보 처리방침 URL이 유효한지 확인

2. **앱 아이콘 문제**
   - 512x512 PNG 형식인지 확인
   - 투명 배경 권장

3. **스크린샷 부족**
   - 최소 2개의 스크린샷 필요

4. **설명 텍스트 불명확**
   - 앱의 기능이 명확하게 설명되었는지 확인

---

## 체크리스트

### 빌드 전

- [ ] Node.js 설치 확인
- [ ] Bubblewrap 설치 확인
- [ ] `manifest.json` 접근 가능 확인
- [ ] `service-worker.js` 접근 가능 확인

### 빌드

- [ ] TWA 프로젝트 초기화 완료
- [ ] APK/AAB 빌드 성공
- [ ] `assetlinks.json` 생성 확인

### 배치

- [ ] `.well-known/assetlinks.json` 배치 완료
- [ ] Git 커밋 및 푸시 완료
- [ ] URL 접근 확인 완료
- [ ] Digital Asset Links 검증 통과

### Play Store

- [ ] Developer Account 생성 완료
- [ ] 앱 정보 입력 완료
- [ ] 개인정보 처리방침 URL 입력
- [ ] 아이콘 및 스크린샷 준비
- [ ] AAB 파일 업로드 완료
- [ ] 출시 버튼 클릭

---

## 다음 단계

### 출시 후 (1주일)

- [ ] 첫 100명 다운로드 목표
- [ ] 사용자 피드백 수집
- [ ] 버그 수정 및 업데이트

### 마케팅 (1개월)

- [ ] Product Hunt 출시
- [ ] Reddit 마케팅 (r/FBA, r/Shopify)
- [ ] Google Ads 캠페인
- [ ] 목표: 1,000 사용자 확보

---

## 참고 자료

- [Bubblewrap 공식 문서](https://github.com/GoogleChromeLabs/bubblewrap)
- [Android TWA 가이드](https://developer.android.com/develop/ui/views/layout/webapps/guide-trusted-web-activities-version2)
- [Digital Asset Links 검증](https://developer.android.com/training/app-links/verify-applinks)
- [Google Play Console 도움말](https://support.google.com/googleplay/android-developer)

---

## 요약

**예상 소요 시간:**

- 빌드: 1.5시간
- assetlinks.json 배치: 30분
- Play Store 등록: 1시간
- 심사 대기: 2-3일

**총 소요 시간: 3시간 + 심사 대기**

---

🎉 **축하합니다!** 이제 NexSupply를 Google Play Store에 출시할 준비가 완료되었습니다!

