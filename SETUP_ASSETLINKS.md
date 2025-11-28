# assetlinks.json 배치 가이드 (Streamlit Cloud 환경)

**Streamlit Cloud에서 TWA를 위한 assetlinks.json 배치 방법**

---

## 🎯 목표

`https://app.nexsupply.app/.well-known/assetlinks.json` 경로로 접근 가능하도록 설정

**문제:** Streamlit Cloud는 `.well-known` 폴더를 직접 서빙하지 않음

**해결:** 별도의 정적 웹사이트(Vercel/Netlify) 사용

---

## 🚀 빠른 시작 (Vercel 사용)

### 1단계: 새 저장소 준비

```bash
# 프로젝트 루트에서
cd ..
git clone https://github.com/junkim123123/nexy-ai-app1.git
# 또는 새 저장소 생성
mkdir nexsupply-assetlinks
cd nexsupply-assetlinks
```

### 2단계: 파일 복사

이미 준비된 파일들을 사용:

```bash
# vercel-assetlinks 폴더의 내용을 새 저장소로 복사
cp -r vercel-assetlinks/* nexsupply-assetlinks/
```

### 3단계: GitHub에 푸시

```bash
cd nexsupply-assetlinks
git init
git add .
git commit -m "Initial commit: assetlinks.json for TWA"
git branch -M main
git remote add origin https://github.com/junkim123123/nexsupply-assetlinks.git
git push -u origin main
```

### 4단계: Vercel 배포

1. [Vercel](https://vercel.com) 접속
2. GitHub로 로그인
3. "Add New Project" 클릭
4. `nexsupply-assetlinks` 저장소 선택
5. Framework Preset: **Other** 선택
6. Deploy 클릭

### 5단계: 도메인 설정 (선택사항)

**Custom Domain 추가:**
- Vercel Dashboard → Settings → Domains
- `assetlinks.nexsupply.app` 추가
- DNS 설정 (Vercel이 제공하는 값 사용)

**또는 Vercel 제공 도메인 사용:**
```
https://nexsupply-assetlinks.vercel.app/.well-known/assetlinks.json
```

---

## 📝 assetlinks.json 업데이트

### TWA 빌드 후

1. **Bubblewrap으로 TWA 빌드**
   ```bash
   cd nexsupply-platform
   .\build_twa.ps1  # 또는 ./build_twa.sh
   ```

2. **생성된 assetlinks.json 확인**
   ```bash
   cat nexsupply-twa/assetlinks.json
   ```

3. **Vercel 저장소에 업데이트**
   ```bash
   cd ../nexsupply-assetlinks
   cp ../nexsupply-platform/nexsupply-twa/assetlinks.json .well-known/
   git add .well-known/assetlinks.json
   git commit -m "Update assetlinks.json with TWA certificate"
   git push
   ```

4. **Vercel 자동 재배포 확인**
   - Vercel Dashboard에서 배포 상태 확인
   - 약 1-2분 후 자동 배포 완료

---

## ✅ 검증

### 1. URL 접근 테스트

브라우저에서 접속:

```
https://assetlinks.nexsupply.app/.well-known/assetlinks.json
```

또는 Vercel 도메인:

```
https://nexsupply-assetlinks.vercel.app/.well-known/assetlinks.json
```

**확인 사항:**
- ✅ HTTP 상태 코드: 200
- ✅ Content-Type: `application/json`
- ✅ JSON 형식이 올바름
- ✅ `package_name`: `com.nexsupply.app`
- ✅ `sha256_cert_fingerprints` 값이 올바름

### 2. Digital Asset Links 검증

Google 검증 도구 사용:

```
https://digitalassetlinks.googleapis.com/v1/statements:list?source.web.site=https://assetlinks.nexsupply.app&relation=delegate_permission/common.handle_all_urls
```

**주의:** `source.web.site`는 `assetlinks.json`이 있는 도메인을 가리켜야 합니다.

### 3. TWA 앱에서 검증

```bash
adb shell pm get-app-links com.nexsupply.app
```

---

## 🔄 대안: Netlify 사용

### Netlify 배포

1. **Netlify 계정 생성**
   - [Netlify](https://www.netlify.com) 접속
   - GitHub로 로그인

2. **프로젝트 연결**
   - "Add new site" → "Import an existing project"
   - GitHub 저장소 선택

3. **빌드 설정**
   - Build command: (비워둠)
   - Publish directory: `.` (루트)

4. **netlify.toml 추가** (선택사항)

```toml
# netlify.toml
[[redirects]]
  from = "/.well-known/*"
  to = "/.well-known/:splat"
  status = 200
  force = true

[[headers]]
  for = "/.well-known/*"
  [headers.values]
    Content-Type = "application/json"
```

---

## ⚠️ 중요 사항

### 도메인 일치 문제

**문제:** TWA 앱이 `https://app.nexsupply.app`을 열지만, `assetlinks.json`은 `https://assetlinks.nexsupply.app`에 있음

**해결 방법:**

1. **같은 도메인 사용 (권장)**
   - `assetlinks.nexsupply.app` 대신 `app.nexsupply.app` 서브도메인 사용
   - 또는 메인 도메인 `nexsupply.app` 사용

2. **TWA 설정 수정**
   - Bubblewrap 초기화 시 Host URL을 `assetlinks.nexsupply.app`로 설정
   - 이 경우 TWA 앱이 다른 도메인을 열게 됨

3. **리다이렉트 설정**
   - `app.nexsupply.app/.well-known/assetlinks.json` 요청을
   - `assetlinks.nexsupply.app/.well-known/assetlinks.json`로 리다이렉트
   - (복잡하고 권장하지 않음)

### 최적 해결책

**같은 도메인 사용:**
- Vercel/Netlify에 `app.nexsupply.app` 서브도메인 연결
- 또는 메인 도메인 `nexsupply.app` 사용
- `assetlinks.json`을 같은 도메인에 배치

---

## 📋 체크리스트

### 초기 설정
- [ ] 새 GitHub 저장소 생성
- [ ] `.well-known/assetlinks.json` 파일 준비
- [ ] Vercel/Netlify 계정 생성
- [ ] 저장소 연결 및 배포
- [ ] 도메인 설정 (선택사항)

### TWA 빌드 후
- [ ] Bubblewrap으로 TWA 빌드
- [ ] `assetlinks.json` 파일 확인
- [ ] Vercel 저장소에 업데이트
- [ ] 재배포 확인
- [ ] URL 접근 테스트
- [ ] Digital Asset Links 검증 통과

---

## 🔗 관련 문서

- `STREAMLIT_CLOUD_TWA_SETUP.md` - 상세 가이드
- `TWA_READ_ME.md` - TWA 빌드 가이드
- `BUILD_TWA.md` - 빌드 스크립트

---

**다음 단계:** Day 4에서 Bubblewrap으로 TWA를 빌드한 후, 생성된 `assetlinks.json`을 이 저장소에 업데이트하세요.



