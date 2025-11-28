# Bubblewrap URL 문제 해결 방법

## 🔴 현재 오류

1. `getaddrinfo ENOTFOUND app.nexsupply.app` - 도메인을 찾을 수 없음
2. `Invalid URL` - 로컬 파일 경로는 사용 불가

## ✅ 해결 방법 (3가지 옵션)

### 옵션 1: Vercel URL 사용 (가장 간단)

현재 Vercel에 배포된 URL 사용:

```powershell
cd nexsupply-twa
bubblewrap init --manifest=https://nexy-ai-app1213.vercel.app/manifest.json
```

**주의:** Vercel에 `manifest.json`이 배포되어 있어야 합니다.

### 옵션 2: 로컬 서버 실행

1. **Streamlit 앱 실행** (별도 터미널):
   ```powershell
   cd ..
   streamlit run streamlit_app.py
   ```

2. **로컬 URL 사용**:
   ```powershell
   cd nexsupply-twa
   bubblewrap init --manifest=http://localhost:8501/manifest.json
   ```

### 옵션 3: Streamlit Cloud URL 사용

Streamlit Cloud에 배포되어 있다면:

```powershell
bubblewrap init --manifest=https://[your-app].streamlit.app/manifest.json
```

---

## 🚀 추천 방법

**옵션 2 (로컬 서버)**를 추천합니다:

1. **터미널 1에서 Streamlit 실행:**
   ```powershell
   streamlit run streamlit_app.py
   ```

2. **터미널 2에서 Bubblewrap 초기화:**
   ```powershell
   cd nexsupply-twa
   bubblewrap init --manifest=http://localhost:8501/manifest.json
   ```

---

**지금:** 위 방법 중 하나를 선택하여 실행하세요!



