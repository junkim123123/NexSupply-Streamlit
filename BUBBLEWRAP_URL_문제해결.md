# Bubblewrap URL 문제 해결

## 🔴 오류 내용

1. `getaddrinfo ENOTFOUND app.nexsupply.app` - 도메인을 찾을 수 없음
2. `Invalid URL` - 로컬 파일 경로는 사용 불가

## 🔍 원인

Bubblewrap은 **HTTP/HTTPS URL만** 받습니다. 로컬 파일 경로나 존재하지 않는 도메인은 사용할 수 없습니다.

## ✅ 해결 방법

### 방법 1: 실제 배포된 URL 사용 (권장)

실제로 배포된 Streamlit 앱의 URL을 사용해야 합니다.

**확인해야 할 URL:**
- Streamlit Cloud: `https://[your-app].streamlit.app/manifest.json`
- Vercel: `https://nexy-ai-app1213.vercel.app/manifest.json`
- 기타 배포 플랫폼

**초기화 명령어:**
```powershell
bubblewrap init --manifest=https://실제배포URL/manifest.json
```

### 방법 2: 로컬 서버 사용

1. **로컬에서 Streamlit 앱 실행**
   ```powershell
   cd ..
   streamlit run streamlit_app.py
   ```

2. **로컬 URL 사용**
   ```powershell
   bubblewrap init --manifest=http://localhost:8501/manifest.json
   ```

### 방법 3: Vercel에 manifest.json 배포

현재 Vercel에 배포된 URL을 사용:

```powershell
bubblewrap init --manifest=https://nexy-ai-app1213.vercel.app/manifest.json
```

---

## 🚀 다음 단계

1. **실제 배포된 manifest.json URL 확인**
2. **해당 URL로 초기화 실행**
3. **빌드 진행**

---

**지금:** 실제 배포된 manifest.json URL을 확인하고 사용하세요!



