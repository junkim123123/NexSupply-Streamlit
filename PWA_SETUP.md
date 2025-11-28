# PWA (Progressive Web App) 설정 가이드

NexSupply 앱이 Google Play Store에 출시될 수 있도록 PWA 기본 요건을 충족했습니다.

## ✅ 완료된 작업

1. **manifest.json** - PWA 매니페스트 파일 생성
2. **service-worker.js** - 오프라인 지원을 위한 Service Worker
3. **PWA 메타 태그** - HTML 헤더에 PWA 메타데이터 추가
4. **Service Worker 등록** - 자동 등록 스크립트 추가

## 📁 생성된 파일

- `manifest.json` - PWA 설정 파일
- `service-worker.js` - 오프라인 캐싱 및 기능
- `utils/pwa_setup.py` - PWA 유틸리티 함수

## 🎨 아이콘 파일 준비

PWA가 제대로 작동하려면 다음 아이콘 파일들이 필요합니다:

### 필수 아이콘 파일

1. **favicon.png** (루트 디렉토리)
   - 크기: 192x192 또는 512x512 권장
   - 형식: PNG
   - 용도: 기본 파비콘

2. **icon-192.png** (루트 디렉토리)
   - 크기: 192x192 픽셀
   - 형식: PNG
   - 용도: Android 홈 화면 아이콘

3. **icon-512.png** (루트 디렉토리)
   - 크기: 512x512 픽셀
   - 형식: PNG
   - 용도: 스플래시 스크린 및 고해상도 아이콘

### 아이콘 생성 방법

#### 방법 1: 온라인 도구 사용
- [PWA Asset Generator](https://www.pwabuilder.com/imageGenerator)
- [RealFaviconGenerator](https://realfavicongenerator.net/)
- [Favicon.io](https://favicon.io/)

#### 방법 2: 이미지 편집 도구
1. 512x512 픽셀의 정사각형 이미지 준비
2. NexSupply 로고 또는 아이콘 사용
3. PNG 형식으로 저장
4. 필요에 따라 192x192 버전 생성

#### 방법 3: Python 스크립트 (Pillow 사용)
```python
from PIL import Image

# 512x512 이미지 생성
img = Image.new('RGB', (512, 512), color='#0EA5E9')
# 로고 추가 등...
img.save('icon-512.png')
img.resize((192, 192)).save('icon-192.png')
img.resize((192, 192)).save('favicon.png')
```

## 🚀 배포 시 확인사항

### Streamlit Cloud 배포

1. **정적 파일 제공**
   - `manifest.json`, `service-worker.js`, 아이콘 파일들을 루트 디렉토리에 배치
   - Streamlit Cloud는 자동으로 정적 파일을 제공합니다

2. **HTTPS 확인**
   - PWA는 HTTPS가 필수입니다
   - Streamlit Cloud는 자동으로 HTTPS를 제공합니다

3. **Service Worker 경로**
   - Service Worker는 루트 경로(`/service-worker.js`)에서 접근 가능해야 합니다

### 로컬 테스트

```bash
# Streamlit 앱 실행
streamlit run streamlit_app.py

# 브라우저에서 확인
# Chrome DevTools > Application > Manifest
# Chrome DevTools > Application > Service Workers
```

## 📱 PWA 기능 확인

### Chrome DevTools에서 확인

1. **Manifest 확인**
   - F12 > Application > Manifest
   - 모든 필드가 올바르게 표시되는지 확인

2. **Service Worker 확인**
   - F12 > Application > Service Workers
   - Service Worker가 등록되고 활성화되었는지 확인

3. **Lighthouse 테스트**
   - F12 > Lighthouse > Progressive Web App
   - PWA 점수 확인 (최소 90점 이상 권장)

### 모바일에서 테스트

1. **Android Chrome**
   - 앱을 열고 메뉴 > "홈 화면에 추가"
   - 홈 화면 아이콘이 생성되는지 확인

2. **iOS Safari**
   - 공유 버튼 > "홈 화면에 추가"
   - 독에 아이콘이 추가되는지 확인

## 🔧 설정 커스터마이징

### manifest.json 수정

`manifest.json` 파일에서 다음을 수정할 수 있습니다:

- `name`: 앱 전체 이름
- `short_name`: 홈 화면에 표시될 짧은 이름
- `theme_color`: 상태 바 색상
- `background_color`: 스플래시 스크린 배경색
- `icons`: 아이콘 경로 및 크기

### Service Worker 커스터마이징

`service-worker.js`에서 다음을 수정할 수 있습니다:

- `CACHE_NAME`: 캐시 버전 관리
- `urlsToCache`: 오프라인에서 캐시할 리소스 목록

## 📋 Google Play Store 출시 체크리스트

- [x] manifest.json 파일 생성
- [x] Service Worker 구현
- [x] PWA 메타 태그 추가
- [ ] 아이콘 파일 생성 (192x192, 512x512)
- [ ] HTTPS 배포 확인
- [ ] Lighthouse PWA 점수 90점 이상
- [ ] 모바일에서 "홈 화면에 추가" 테스트
- [ ] 오프라인 기능 테스트

## 🐛 문제 해결

### Service Worker가 등록되지 않음
- HTTPS 연결 확인
- Service Worker 파일 경로 확인 (`/service-worker.js`)
- 브라우저 콘솔에서 오류 확인

### 아이콘이 표시되지 않음
- 아이콘 파일 경로 확인
- 파일 크기 확인 (192x192, 512x512)
- 파일 형식 확인 (PNG)

### Manifest 오류
- `manifest.json` JSON 형식 확인
- 필수 필드 확인 (`name`, `start_url`, `icons`)
- 브라우저 DevTools에서 오류 확인

## 📚 참고 자료

- [MDN: Progressive Web Apps](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
- [Web.dev: PWA](https://web.dev/progressive-web-apps/)
- [Google Play: PWA 배포 가이드](https://developer.chrome.com/docs/android/trusted-web-activity/)



