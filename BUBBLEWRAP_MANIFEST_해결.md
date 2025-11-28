# Bubblewrap manifest.json 접근 문제 해결

## 🔴 현재 오류

```
cli ERROR Unexpected token '<', "<!doctype "... is not valid JSON
```

**원인:** Streamlit Cloud에서 `manifest.json`이 HTML 페이지로 반환되고 있습니다.

## ✅ 해결 방법

### 방법 1: static 폴더의 manifest.json 사용 (권장)

Streamlit Cloud는 `static/` 폴더의 파일을 `/app/static/` 경로로 서빙합니다.

**URL:**
```
https://nexy-ai-app1-6sc6othrylf2nymoh474p8.streamlit.app/app/static/manifest.json
```

**초기화 명령어:**
```powershell
cd nexsupply-twa
bubblewrap init --manifest=https://nexy-ai-app1-6sc6othrylf2nymoh474p8.streamlit.app/app/static/manifest.json
```

### 방법 2: 로컬 HTTP 서버 사용

1. **Python HTTP 서버 실행** (별도 터미널):
   ```powershell
   python -m http.server 8000
   ```

2. **로컬 URL 사용**:
   ```powershell
   cd nexsupply-twa
   bubblewrap init --manifest=http://localhost:8000/manifest.json
   ```

### 방법 3: Vercel URL 사용

Vercel에 manifest.json이 배포되어 있다면:
```powershell
bubblewrap init --manifest=https://nexy-ai-app1213.vercel.app/manifest.json
```

---

## 🚀 추천: 방법 1 시도

`/app/static/manifest.json` 경로를 사용하세요!



