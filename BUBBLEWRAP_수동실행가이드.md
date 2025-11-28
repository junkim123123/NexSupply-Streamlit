# Bubblewrap 수동 실행 가이드

**Bubblewrap 초기화는 대화형 프로세스이므로 수동으로 진행해야 합니다.**

---

## 🚀 빠른 실행

터미널에서 다음 명령어를 실행하세요:

```powershell
cd nexsupply-twa
bubblewrap init --manifest=https://app.nexsupply.app/manifest.json
```

---

## 📋 질문별 답변 가이드

초기화 중 다음 질문들이 나타납니다. 아래 답변을 입력하세요:

### 1. JDK 설치
```
? Do you want Bubblewrap to install the JDK (recommended)? (Y/n)
```
**답변:** `Y` (Enter)

### 2. Android SDK 설치
```
? Do you want Bubblewrap to install the Android SDK (recommended)? (Y/n)
```
**답변:** `Y` (Enter)

### 3. Android SDK 라이선스 동의
```
? Do you agree to the Android SDK terms and conditions at [URL]? (Y/n)
```
**답변:** `Y` (Enter)

### 4. App name
```
? Application name: 
```
**답변:** `NexSupply` (Enter)

### 5. Package ID
```
? Package ID: 
```
**답변:** `com.nexsupply.app` (Enter)

### 6. Host URL
```
? Host URL: 
```
**답변:** `app.nexsupply.app` (Enter)

### 7. Create signing key
```
? Do you want to create a new signing key? (Y/n)
```
**답변:** `Y` (Enter)

### 8. Key password
```
? Key password: 
```
**답변:** 원하는 비밀번호 입력 (예: `nexsupply2024`) (Enter)

### 9. Confirm password
```
? Confirm password: 
```
**답변:** 같은 비밀번호 다시 입력 (Enter)

---

## 🏗️ 빌드 실행

초기화가 완료되면:

```powershell
bubblewrap build
```

빌드 중 비밀번호를 묻으면 위에서 입력한 비밀번호를 입력하세요.

---

## 📝 SHA-256 지문 추출

빌드가 완료되면:

```powershell
Get-Content assetlinks.json
```

또는 빌드 로그에서 `SHA-256 Fingerprint:` 또는 `Fingerprint:`를 찾으세요.

---

## 🔄 assetlinks.json 업데이트

SHA-256 지문을 복사한 후:

1. 프로젝트 루트로 이동:
   ```powershell
   cd ..
   ```

2. `.well-known/assetlinks.json` 파일 열기

3. PLACEHOLDER를 실제 지문으로 교체:
   ```json
   "sha256_cert_fingerprints": [
     "실제_SHA256_지문_여기에_붙여넣기"
   ]
   ```

4. Git 커밋 및 푸시:
   ```powershell
   git add .well-known/assetlinks.json
   git commit -m "feat: Update SHA-256 fingerprint from Bubblewrap"
   git push origin main
   ```

---

## ⚡ 빠른 참조

**필요한 모든 답변:**
- JDK 설치: `Y`
- Android SDK 설치: `Y`
- 라이선스 동의: `Y`
- App name: `NexSupply`
- Package ID: `com.nexsupply.app`
- Host URL: `app.nexsupply.app`
- Create signing key: `Y`
- Key password: (원하는 비밀번호)

---

**이 가이드를 따라 진행하시면 됩니다! 🚀**



