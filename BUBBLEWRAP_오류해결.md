# Bubblewrap 오류 해결: twa-manifest.json 파일 없음

## 🔴 오류 내용

```
cli ERROR ENOENT: no such file or directory, open 'twa-manifest.json'
```

## 🔍 원인

Bubblewrap 초기화가 완전히 완료되지 않아 `twa-manifest.json` 파일이 생성되지 않았습니다.

## ✅ 해결 방법

### 방법 1: 초기화 다시 실행 (권장)

1. **nexsupply-twa 폴더 삭제 후 재생성**
   ```powershell
   cd ..
   Remove-Item -Path nexsupply-twa -Recurse -Force
   New-Item -ItemType Directory -Path nexsupply-twa
   cd nexsupply-twa
   ```

2. **초기화 다시 실행**
   ```powershell
   bubblewrap init --manifest=https://app.nexsupply.app/manifest.json
   ```

3. **질문에 답변**
   - Android SDK 설치: `Y`
   - 라이선스 동의: `Y`
   - App name: `NexSupply`
   - Package ID: `com.nexsupply.app`
   - Host URL: `app.nexsupply.app`
   - Create signing key: `Y`
   - Key password: `nexsupply2024`
   - Confirm password: `nexsupply2024`

4. **초기화 완료 확인**
   ```powershell
   Test-Path twa-manifest.json
   ```
   `True`가 나와야 합니다.

### 방법 2: 경로 문제 해결

경로에 공백이 있어 문제가 될 수 있습니다 ("바탕 화면").

**해결:**
- 프로젝트를 공백이 없는 경로로 이동
- 또는 경로를 따옴표로 감싸기

---

## 🚀 다음 단계

초기화가 완료되면:

```powershell
bubblewrap build
```

비밀번호: `nexsupply2024`

---

**지금:** 초기화를 다시 실행하세요!



