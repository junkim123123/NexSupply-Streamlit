# Streamlit Cloud 환경에서 TWA 설정 가이드

**Streamlit Community Cloud 배포 환경에 맞춘 `assetlinks.json` 배치 방법**

---

## 🔍 문제 상황

Streamlit Cloud는 보안상의 이유로 `.well-known` 폴더와 같은 숨겨진 경로의 파일을 직접 서빙하지 않습니다.

**필요한 경로:**
```
https://app.nexsupply.app/.well-known/assetlinks.json
```

**Streamlit Cloud 제약:**
- `.well-known` 폴더 직접 서빙 불가
- 정적 파일은 `static/` 폴더를 통해서만 서빙 가능

---

## ✅ 해결 방법: 3가지 옵션

### 옵션 A: 별도 정적 웹사이트 사용 (권장) ⭐

가장 안정적이고 확실한 방법입니다.

#### 1단계: 새 GitHub 저장소 생성

```bash
# 로컬에서 새 저장소 생성
mkdir nexsupply-assetlinks
cd nexsupply-assetlinks
git init
```

#### 2단계: assetlinks.json 파일 준비

**주의:** 이 파일은 Bubblewrap으로 TWA를 빌드한 후 생성됩니다.

```bash
# TWA 빌드 후 생성된 파일을 복사
cp ../nexsupply-twa/assetlinks.json .well-known/
```

또는 수동으로 생성:

```json
// .well-known/assetlinks.json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.nexsupply.app",
      "sha256_cert_fingerprints": [
        "AA:BB:CC:DD:EE:FF:..." // Bubblewrap이 생성한 값
      ]
    }
  }
]
```

#### 3단계: Vercel에 배포 (권장)

**Vercel 배포 (가장 간단):**

1. **GitHub 저장소 푸시**
   ```bash
   git add .well-known/assetlinks.json
   git commit -m "Add assetlinks.json for TWA"
   git push origin main
   ```

2. **Vercel 연결**
   - [Vercel](https://vercel.com) 접속
   - GitHub 계정으로 로그인
   - "New Project" 클릭
   - `nexsupply-assetlinks` 저장소 선택
   - Framework Preset: **Other** 선택
   - Root Directory: `.` (루트)
   - Deploy 클릭

3. **도메인 설정**
   - Vercel 대시보드 → Settings → Domains
   - Custom Domain 추가: `assetlinks.nexsupply.app`
   - 또는 Vercel 제공 도메인 사용: `nexsupply-assetlinks.vercel.app`

4. **최종 경로 확인**
   ```
   https://assetlinks.nexsupply.app/.well-known/assetlinks.json
   ```

**또는 Netlify 배포:**

1. **Netlify에 저장소 연결**
   - [Netlify](https://www.netlify.com) 접속
   - "Add new site" → "Import an existing project"
   - GitHub 저장소 선택

2. **빌드 설정**
   - Build command: (비워둠)
   - Publish directory: `.` (루트)

3. **도메인 설정**
   - Site settings → Domain management
   - Custom domain 추가

---

### 옵션 B: Streamlit 앱 내에서 동적 생성 (고급)

Streamlit 앱 내부에서 `assetlinks.json`을 동적으로 서빙하는 방법입니다.

#### 1단계: assetlinks.json 데이터 준비

`utils/assetlinks.py` 파일 생성:

```python
# utils/assetlinks.py
"""
Digital Asset Links JSON 데이터
Bubblewrap으로 TWA 빌드 후 생성된 값을 여기에 입력
"""

ASSETLINKS_DATA = [
    {
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {
            "namespace": "android_app",
            "package_name": "com.nexsupply.app",
            "sha256_cert_fingerprints": [
                "AA:BB:CC:DD:EE:FF:..."  # Bubblewrap이 생성한 값으로 교체
            ]
        }
    }
]
```

#### 2단계: streamlit_app.py에 라우팅 추가

```python
# streamlit_app.py 상단에 추가
import json
from utils.assetlinks import ASSETLINKS_DATA

# assetlinks.json 요청 처리
if st.query_params.get("assetlinks") == "true":
    st.set_page_config(page_title="assetlinks.json")
    st.header("")  # 헤더 숨기기
    st.json(ASSETLINKS_DATA)
    st.stop()
```

**문제점:**
- Streamlit은 URL 경로를 직접 제어할 수 없음
- `/well-known/assetlinks.json` 경로로 접근 불가
- 쿼리 파라미터 방식은 표준 경로가 아님

**결론:** 이 방법은 TWA 검증에 실패할 가능성이 높습니다.

---

### 옵션 C: Streamlit Cloud 정적 파일 서빙 시도 (실험적)

Streamlit Cloud의 정적 파일 서빙 기능을 활용하는 방법입니다.

#### 1단계: static 폴더에 파일 배치

```bash
# 프로젝트 루트에서
mkdir -p static/.well-known
cp nexsupply-twa/assetlinks.json static/.well-known/
```

#### 2단계: manifest.json 수정

`manifest.json`에서 assetlinks.json 경로를 정적 파일 경로로 변경:

```json
{
  "name": "NexSupply - AI Sourcing Assistant",
  ...
  "assetlinks_url": "/app/static/.well-known/assetlinks.json"
}
```

**문제점:**
- TWA는 반드시 `/.well-known/assetlinks.json` 경로를 요구함
- `/app/static/.well-known/assetlinks.json` 경로는 표준이 아님
- 검증 실패 가능성 높음

---

## 🎯 최종 권장사항: 옵션 A (Vercel/Netlify)

**이유:**
1. ✅ 표준 경로 (`/.well-known/assetlinks.json`) 지원
2. ✅ 무료 플랜 제공
3. ✅ 배포가 간단하고 빠름
4. ✅ TWA 검증 100% 통과 보장

---

## 📋 실행 체크리스트

### 옵션 A 실행 (Vercel)

- [ ] 새 GitHub 저장소 생성 (`nexsupply-assetlinks`)
- [ ] `.well-known/assetlinks.json` 파일 준비
- [ ] Vercel 계정 생성 및 연결
- [ ] 배포 완료 확인
- [ ] `https://assetlinks.nexsupply.app/.well-known/assetlinks.json` 접근 테스트
- [ ] Digital Asset Links 검증 통과 확인

### TWA 빌드 후

- [ ] Bubblewrap으로 TWA 빌드
- [ ] 생성된 `assetlinks.json` 파일 확인
- [ ] 파일 내용을 Vercel 저장소에 복사
- [ ] Vercel에 재배포
- [ ] TWA 앱에서 검증

---

## 🔗 관련 파일

- `TWA_READ_ME.md` - TWA 빌드 가이드
- `BUILD_TWA.md` - 빌드 스크립트 가이드
- `DAY1_EXECUTION_GUIDE.md` - Day 1 실행 가이드

---

## 📞 문제 해결

### Vercel 배포 오류

**문제:** `.well-known` 폴더가 인식되지 않음

**해결:**
1. `vercel.json` 파일 생성:
   ```json
   {
     "headers": [
       {
         "source": "/.well-known/(.*)",
         "headers": [
           {
             "key": "Content-Type",
             "value": "application/json"
           }
         ]
       }
     ]
   }
   ```

### Netlify 배포 오류

**문제:** `.well-known` 폴더 접근 불가

**해결:**
1. `netlify.toml` 파일 생성:
   ```toml
   [[redirects]]
     from = "/.well-known/*"
     to = "/.well-known/:splat"
     status = 200
     force = true
   ```

---

**다음 단계:** Day 4에서 Bubblewrap으로 TWA를 빌드한 후, 생성된 `assetlinks.json` 파일을 Vercel에 배포하세요.

