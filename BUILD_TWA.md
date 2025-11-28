# TWA 빌드 스크립트 및 자동화

## 빠른 시작

### 1. 아이콘 생성 (필요 시)

```bash
python create_icons.py
```

이 명령어는 `static/icons/icon-192.png`와 `static/icons/icon-512.png`를 생성합니다.

### 2. Bubblewrap으로 TWA 생성

```bash
# Bubblewrap 설치 (처음만)
npm install -g @bubblewrap/cli

# TWA 프로젝트 생성
mkdir nexsupply-twa
cd nexsupply-twa
bubblewrap init --manifest=https://app.nexsupply.net/app/static/manifest.json

# 빌드
bubblewrap build
```

### 3. assetlinks.json 배치

빌드 후 생성된 `assetlinks.json` 파일을 다음 경로에 배치:

```
https://app.nexsupply.net/.well-known/assetlinks.json
```

## 파일 구조

```
nexsupply-platform/
├── static/
│   ├── manifest.json          # PWA 매니페스트
│   └── icons/
│       ├── icon-192.png       # 192x192 아이콘
│       └── icon-512.png        # 512x512 아이콘
├── .streamlit/
│   └── config.toml            # enableStaticServing = true
├── create_icons.py            # 아이콘 생성 스크립트
└── TWA_GUIDE.md              # 상세 가이드
```

## Streamlit Cloud 배포 시 주의사항

### .well-known 폴더 서빙

Streamlit Cloud에서 `.well-known/assetlinks.json`을 서빙하려면:

1. 프로젝트 루트에 `.well-known` 폴더 생성
2. `assetlinks.json` 파일 복사
3. Git에 커밋 및 푸시

또는 서버 설정에서 다음 경로를 정적 파일로 서빙:

```
/.well-known/assetlinks.json
```

## 자동화 스크립트 (선택사항)

### build-twa.sh (Linux/Mac)

```bash
#!/bin/bash
set -e

echo "🚀 NexSupply TWA 빌드 시작..."

# 1. 아이콘 생성
echo "📦 아이콘 생성 중..."
python create_icons.py

# 2. TWA 프로젝트 초기화
echo "🔨 TWA 프로젝트 초기화 중..."
if [ ! -d "nexsupply-twa" ]; then
    mkdir nexsupply-twa
    cd nexsupply-twa
    bubblewrap init --manifest=https://app.nexsupply.net/app/static/manifest.json
else
    cd nexsupply-twa
fi

# 3. 빌드
echo "🏗️ TWA 빌드 중..."
bubblewrap build

# 4. assetlinks.json 복사
echo "📋 assetlinks.json 생성 완료"
echo "다음 경로에 배치하세요:"
echo "https://app.nexsupply.net/.well-known/assetlinks.json"

cd ..
```

### build-twa.ps1 (Windows PowerShell)

```powershell
# NexSupply TWA 빌드 스크립트

Write-Host "🚀 NexSupply TWA 빌드 시작..." -ForegroundColor Green

# 1. 아이콘 생성
Write-Host "📦 아이콘 생성 중..." -ForegroundColor Yellow
python create_icons.py

# 2. TWA 프로젝트 초기화
Write-Host "🔨 TWA 프로젝트 초기화 중..." -ForegroundColor Yellow
if (-not (Test-Path "nexsupply-twa")) {
    New-Item -ItemType Directory -Path "nexsupply-twa"
    Set-Location "nexsupply-twa"
    bubblewrap init --manifest=https://app.nexsupply.net/app/static/manifest.json
} else {
    Set-Location "nexsupply-twa"
}

# 3. 빌드
Write-Host "🏗️ TWA 빌드 중..." -ForegroundColor Yellow
bubblewrap build

# 4. 완료 메시지
Write-Host "✅ 빌드 완료!" -ForegroundColor Green
Write-Host "📋 assetlinks.json을 다음 경로에 배치하세요:" -ForegroundColor Cyan
Write-Host "https://app.nexsupply.net/.well-known/assetlinks.json" -ForegroundColor Cyan

Set-Location ..
```

## 검증

### 1. manifest.json 확인

브라우저에서 접속:
```
https://app.nexsupply.net/app/static/manifest.json
```

### 2. 아이콘 확인

```
https://app.nexsupply.net/app/static/icons/icon-192.png
https://app.nexsupply.net/app/static/icons/icon-512.png
```

### 3. assetlinks.json 확인

```
https://app.nexsupply.net/.well-known/assetlinks.json
```

### 4. Digital Asset Links 검증

```
https://digitalassetlinks.googleapis.com/v1/statements:list?source.web.site=https://app.nexsupply.net&relation=delegate_permission/common.handle_all_urls
```

## 다음 단계

1. ✅ `static/manifest.json` 생성 완료
2. ✅ `static/icons/` 아이콘 준비 완료
3. ✅ `.streamlit/config.toml` 설정 완료
4. ⏭️ Bubblewrap으로 TWA 생성
5. ⏭️ `assetlinks.json` 배치
6. ⏭️ Google Play Store 제출

자세한 내용은 `TWA_GUIDE.md`를 참고하세요.

