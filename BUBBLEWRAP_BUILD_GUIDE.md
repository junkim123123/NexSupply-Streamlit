# Bubblewrap TWA 빌드 가이드 - SHA-256 지문 추출

**Day 4: TWA 최종 빌드 및 assetlinks.json 업데이트**

---

## 🎯 목표

1. Bubblewrap으로 TWA 빌드
2. SHA-256 지문 추출
3. `assetlinks.json` 파일 업데이트
4. Vercel 재배포 및 검증

---

## 📋 사전 준비

### 필수 요구사항

- ✅ Node.js 설치 (v14 이상)
- ✅ Bubblewrap CLI 설치
- ✅ manifest.json이 `https://app.nexsupply.app/manifest.json`에서 접근 가능

### 확인 사항

```bash
# Node.js 확인
node --version

# Bubblewrap 확인
bubblewrap --version
```

---

## 🚀 1단계: Bubblewrap 설치 (처음만)

```bash
npm install -g @bubblewrap/cli
```

---

## 🔨 2단계: TWA 프로젝트 초기화

### 프로젝트 폴더 생성

```bash
# 프로젝트 루트에서
mkdir nexsupply-twa
cd nexsupply-twa
```

### Bubblewrap 초기화

```bash
bubblewrap init --manifest=https://app.nexsupply.app/manifest.json
```

**초기화 중 입력 사항:**

- **App name**: `NexSupply`
- **Package ID**: `com.nexsupply.app`
- **Host URL**: `app.nexsupply.app`
- **Create signing key**: `yes` (새 키 생성)
- **Key password**: 안전한 비밀번호 입력 (나중에 필요)

---

## 🏗️ 3단계: TWA 빌드 및 SHA-256 지문 추출

### 빌드 실행

```bash
bubblewrap build
```

### SHA-256 지문 찾기

빌드가 완료되면 다음 중 하나에서 SHA-256 지문을 찾을 수 있습니다:

#### 방법 1: 빌드 로그에서 확인

빌드 출력에서 다음과 같은 형식의 지문을 찾습니다:

```
SHA-256 Fingerprint: AB:4B:7F:4B:96:D1:C9:53:97:0F:95:E7:2B:7D:A3:32:37:1C:7E:9F:B5:28:56:C0:E7:D7:DA:D9:44:47:BE:C6
```

#### 방법 2: assetlinks.json 파일 확인

Bubblewrap이 자동으로 생성한 `assetlinks.json` 파일 확인:

```bash
cat assetlinks.json
```

또는 Windows PowerShell:

```powershell
Get-Content assetlinks.json
```

**파일 위치:** `nexsupply-twa/assetlinks.json`

---

## 📝 4단계: assetlinks.json 업데이트

### SHA-256 지문 복사

Bubblewrap이 생성한 실제 SHA-256 지문을 복사합니다.

**형식 예시:**
```
AB:4B:7F:4B:96:D1:C9:53:97:0F:95:E7:2B:7D:A3:32:37:1C:7E:9F:B5:28:56:C0:E7:D7:DA:D9:44:47:BE:C6
```

### 프로젝트의 assetlinks.json 업데이트

프로젝트 루트의 `.well-known/assetlinks.json` 파일을 엽니다:

```json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.nexsupply.app",
      "sha256_cert_fingerprints": [
        "PLACEHOLDER: Bubblewrap으로 TWA 빌드 후 여기에 실제 SHA256 지문을 입력하세요"
      ]
    }
  }
]
```

**PLACEHOLDER를 실제 지문으로 교체:**

```json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.nexsupply.app",
      "sha256_cert_fingerprints": [
        "AB:4B:7F:4B:96:D1:C9:53:97:0F:95:E7:2B:7D:A3:32:37:1C:7E:9F:B5:28:56:C0:E7:D7:DA:D9:44:47:BE:C6"
      ]
    }
  }
]
```

**중요:**
- 콜론(`:`)으로 구분된 형식 유지
- 대문자/소문자 정확히 복사
- 따옴표 안에 정확히 입력

---

## 🔄 5단계: Git 커밋 및 푸시

```bash
# 파일 수정 확인
git status

# 수정된 파일 추가
git add .well-known/assetlinks.json

# 커밋
git commit -m "feat: Update assetlinks.json with actual SHA-256 fingerprint from Bubblewrap"

# 푸시
git push origin main
```

---

## ✅ 6단계: Vercel 재배포 확인

### 자동 재배포

Vercel이 Git 푸시를 감지하여 자동으로 재배포를 시작합니다 (약 1-2분).

### 배포 확인

Vercel 대시보드에서:
- 배포 상태가 "Building" → "Ready"로 변경되는지 확인
- 배포 로그에서 오류가 없는지 확인

---

## 🧪 7단계: 최종 검증

### 브라우저에서 확인

재배포 완료 후 (약 1-2분) 다음 URL로 접속:

```
https://nexy-ai-app1213.vercel.app/.well-known/assetlinks.json
```

**확인 사항:**
- ✅ HTTP 상태 코드: 200 OK
- ✅ Content-Type: `application/json; charset=utf-8`
- ✅ PLACEHOLDER가 사라지고 실제 SHA-256 지문이 표시됨
- ✅ JSON 형식이 올바름

### 터미널에서 확인

```bash
curl https://nexy-ai-app1213.vercel.app/.well-known/assetlinks.json
```

### Digital Asset Links 검증

Google 검증 도구 사용:

```
https://digitalassetlinks.googleapis.com/v1/statements:list?source.web.site=https://nexy-ai-app1213.vercel.app&relation=delegate_permission/common.handle_all_urls
```

---

## 📦 빌드 결과물

빌드가 완료되면 다음 파일들이 생성됩니다:

- `app-release-signed.apk` - 서명된 APK 파일
- `app-release-bundle.aab` - App Bundle (Play Store 업로드용)
- `assetlinks.json` - Digital Asset Links 파일 (SHA-256 지문 포함)

---

## 🔍 문제 해결

### SHA-256 지문을 찾을 수 없음

**해결 방법:**

1. **빌드 로그 다시 확인**
   ```bash
   # 빌드 로그를 파일로 저장
   bubblewrap build > build.log 2>&1
   cat build.log | grep -i "sha256\|fingerprint"
   ```

2. **키스토어에서 직접 추출**
   ```bash
   # Java keytool 사용 (Java 설치 필요)
   keytool -list -v -keystore android.keystore -alias twa
   ```

3. **Bubblewrap 업데이트**
   ```bash
   npm update -g @bubblewrap/cli
   ```

### assetlinks.json이 업데이트되지 않음

**확인 사항:**
- 파일 경로가 정확한지 확인 (`.well-known/assetlinks.json`)
- Git에 커밋되었는지 확인 (`git status`)
- Vercel 재배포가 완료되었는지 확인

---

## 📋 체크리스트

### 빌드 전
- [ ] Node.js 설치 확인
- [ ] Bubblewrap 설치 확인
- [ ] manifest.json 접근 가능 확인

### 빌드
- [ ] TWA 프로젝트 초기화 완료
- [ ] APK/AAB 빌드 성공
- [ ] SHA-256 지문 추출 완료

### 업데이트
- [ ] assetlinks.json 파일 업데이트
- [ ] Git 커밋 및 푸시 완료
- [ ] Vercel 재배포 확인

### 검증
- [ ] URL 접근 테스트 (200 OK)
- [ ] PLACEHOLDER가 실제 지문으로 교체됨
- [ ] Digital Asset Links 검증 통과

---

## 🎯 다음 단계

assetlinks.json 업데이트가 완료되면:

1. **Google Play Console 등록** (Day 6-7)
2. **AAB 파일 업로드**
3. **앱 정보 입력**
4. **출시**

---

**이 가이드를 따라하면 TWA 빌드와 assetlinks.json 업데이트가 완료됩니다! 🚀**



