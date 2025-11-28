# TWA (Trusted Web Activity) 생성 가이드

NexSupply PWA를 Google Play Store에 출시하기 위한 TWA 래퍼 생성 가이드입니다.

## 📋 사전 준비 사항

1. ✅ Streamlit 앱이 `https://app.nexsupply.net`에서 실행 중
2. ✅ `static/manifest.json` 파일이 생성되어 있음
3. ✅ `static/icons/icon-192.png`, `static/icons/icon-512.png` 아이콘 파일 준비
4. ✅ Node.js 설치 (Bubblewrap 사용)

## 🚀 1단계: Bubblewrap 설치

```bash
npm install -g @bubblewrap/cli
```

설치 확인:
```bash
bubblewrap --version
```

## 🎯 2단계: TWA 프로젝트 초기화

### 프로젝트 폴더 생성

```bash
mkdir nexsupply-twa
cd nexsupply-twa
```

### Bubblewrap 초기화

```bash
bubblewrap init \
  --manifest=https://app.nexsupply.net/app/static/manifest.json
```

이 명령어는:
- `manifest.json`을 읽어서 앱 이름, 시작 URL, 아이콘 등을 자동으로 가져옵니다
- Android 프로젝트 구조를 생성합니다
- 패키지 이름, 앱 이름 등을 설정합니다

### 초기화 중 입력 사항

Bubblewrap이 다음 정보를 요청할 수 있습니다:

- **Package ID**: `net.nexsupply.app` (또는 원하는 패키지명)
- **App Name**: `NexSupply`
- **Launcher Name**: `NexSupply` (짧은 이름)
- **Signing Key**: 새로 생성하거나 기존 키 사용

## 🔨 3단계: TWA 빌드

### 서명 키 생성 (처음만)

```bash
bubblewrap build
```

처음 실행 시 서명 키를 생성하라는 메시지가 나옵니다. `y`를 선택하면 자동으로 생성됩니다.

### 빌드 결과물

빌드가 완료되면 다음 파일들이 생성됩니다:

- `app-release-signed.apk` - 서명된 APK 파일
- `app-release-bundle.aab` - App Bundle (Play Store 업로드용)
- `assetlinks.json` - Digital Asset Links 파일

## 📦 4단계: assetlinks.json 배치

### assetlinks.json 파일 확인

빌드 후 생성된 `assetlinks.json` 파일을 확인합니다:

```json
[
  {
    "relation": [
      "delegate_permission/common.handle_all_urls"
    ],
    "target": {
      "namespace": "android_app",
      "package_name": "net.nexsupply.app",
      "sha256_cert_fingerprints": [
        "AA:BB:CC:DD:EE:FF:..."
      ]
    }
  }
]
```

### 서버에 배치

**중요**: 이 파일을 다음 경로에 배치해야 합니다:

```
https://app.nexsupply.net/.well-known/assetlinks.json
```

### Streamlit Cloud 배포 시

Streamlit Cloud에서는 `.well-known` 폴더를 직접 서빙할 수 없을 수 있습니다. 다음 방법을 사용하세요:

#### 방법 1: 정적 파일로 배치

1. 프로젝트 루트에 `.well-known` 폴더 생성
2. `assetlinks.json` 파일 복사
3. Streamlit Cloud가 자동으로 서빙하는지 확인

#### 방법 2: Nginx/프록시 설정

서버에서 다음 경로를 정적 파일로 서빙하도록 설정:

```nginx
location /.well-known/assetlinks.json {
    alias /path/to/assetlinks.json;
    add_header Content-Type application/json;
}
```

### 배치 확인

브라우저에서 직접 접속하여 확인:

```
https://app.nexsupply.net/.well-known/assetlinks.json
```

다음 조건을 만족해야 합니다:

- ✅ HTTP 상태 코드: 200
- ✅ Content-Type: `application/json`
- ✅ 파일 내용이 올바른 JSON 형식
- ✅ `package_name`과 `sha256_cert_fingerprints`가 TWA 앱과 일치

## 🧪 5단계: TWA 테스트

### 로컬 테스트

```bash
# APK 설치 (Android 기기 또는 에뮬레이터)
adb install app-release-signed.apk
```

### Digital Asset Links 검증

Google의 Digital Asset Links 검증 도구 사용:

```
https://digitalassetlinks.googleapis.com/v1/statements:list?source.web.site=https://app.nexsupply.net&relation=delegate_permission/common.handle_all_urls
```

또는 Android 명령어:

```bash
adb shell pm get-app-links net.nexsupply.app
```

## 📤 6단계: Google Play Store 제출

### App Bundle 업로드

1. [Google Play Console](https://play.google.com/console) 접속
2. 새 앱 생성 또는 기존 앱 선택
3. **Production** > **Create new release**
4. `app-release-bundle.aab` 파일 업로드
5. 스토어 정보 입력:
   - 앱 이름: NexSupply
   - 짧은 설명: AI-powered B2B sourcing platform
   - 전체 설명: (앱 설명 작성)
   - 스크린샷: (필요 시)
   - 아이콘: 512x512 PNG

### 검토 제출

- 모든 필수 정보 입력 완료
- `assetlinks.json` 배치 확인
- 테스트 완료

## 🔍 문제 해결

### assetlinks.json이 인식되지 않음

1. **경로 확인**: `https://app.nexsupply.net/.well-known/assetlinks.json` 직접 접속
2. **Content-Type 확인**: `application/json`이어야 함
3. **파일 내용 확인**: JSON 형식이 올바른지 확인
4. **패키지명 확인**: `package_name`이 TWA 앱과 일치하는지 확인
5. **서명 지문 확인**: `sha256_cert_fingerprints`가 빌드에 사용한 키와 일치하는지 확인

### TWA에서 주소창이 사라지지 않음

- `assetlinks.json`이 올바르게 배치되고 검증되었는지 확인
- 앱을 완전히 제거하고 재설치
- Chrome 브라우저 캐시 클리어

### 빌드 오류

```bash
# Bubblewrap 캐시 클리어
bubblewrap clean

# 다시 빌드
bubblewrap build
```

## 📚 참고 자료

- [Bubblewrap 공식 문서](https://github.com/GoogleChromeLabs/bubblewrap)
- [Android TWA 가이드](https://developer.android.com/develop/ui/views/layout/webapps/guide-trusted-web-activities-version2)
- [Digital Asset Links 검증](https://developer.android.com/training/app-links/verify-applinks)
- [PWABuilder (대안)](https://www.pwabuilder.com/)

## ✅ 체크리스트

- [ ] Bubblewrap 설치 완료
- [ ] TWA 프로젝트 초기화 완료
- [ ] APK/AAB 빌드 성공
- [ ] `assetlinks.json` 파일 생성 확인
- [ ] `assetlinks.json`을 서버에 배치
- [ ] `https://app.nexsupply.net/.well-known/assetlinks.json` 접속 확인
- [ ] Digital Asset Links 검증 통과
- [ ] TWA 앱 테스트 완료 (주소창 사라짐 확인)
- [ ] Google Play Console에 앱 정보 입력
- [ ] App Bundle 업로드 및 제출



