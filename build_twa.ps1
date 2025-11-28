# NexSupply TWA 빌드 스크립트 (Windows PowerShell)
# Google Play Store 출시를 위한 APK/AAB 생성

$ErrorActionPreference = "Stop"

Write-Host "🚀 NexSupply TWA 빌드 시작..." -ForegroundColor Green

# 1. Node.js 및 Bubblewrap 확인
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js가 설치되지 않았습니다." -ForegroundColor Red
    Write-Host "https://nodejs.org/ 에서 설치하세요." -ForegroundColor Yellow
    exit 1
}

if (-not (Get-Command bubblewrap -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Bubblewrap 설치 중..." -ForegroundColor Yellow
    npm install -g @bubblewrap/cli
}

# 2. TWA 프로젝트 디렉토리 생성
$TWA_DIR = "nexsupply-twa"
if (-not (Test-Path $TWA_DIR)) {
    Write-Host "📁 TWA 프로젝트 디렉토리 생성 중..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $TWA_DIR | Out-Null
    Set-Location $TWA_DIR
    
    Write-Host "🔨 Bubblewrap 초기화 중..." -ForegroundColor Yellow
    bubblewrap init --manifest=https://app.nexsupply.app/manifest.json
    
    Write-Host "✅ 초기화 완료!" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  다음 단계:" -ForegroundColor Yellow
    Write-Host "   1. App name: NexSupply"
    Write-Host "   2. Package ID: com.nexsupply.app"
    Write-Host "   3. Host URL: app.nexsupply.app"
    Write-Host "   4. Create signing key: yes"
    Write-Host ""
} else {
    Write-Host "📁 기존 TWA 프로젝트 사용 중..." -ForegroundColor Yellow
    Set-Location $TWA_DIR
}

# 3. APK/AAB 빌드
Write-Host "🏗️  APK/AAB 빌드 중..." -ForegroundColor Yellow
bubblewrap build

# 4. assetlinks.json 확인 및 복사
if (Test-Path "assetlinks.json") {
    Write-Host "✅ assetlinks.json 생성 완료!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 다음 단계:" -ForegroundColor Cyan
    Write-Host "   1. 프로젝트 루트에 .well-known 폴더 생성"
    Write-Host "   2. assetlinks.json을 .well-known/ 폴더로 복사"
    Write-Host "   3. Git에 커밋 및 푸시"
    Write-Host "   4. https://app.nexsupply.app/.well-known/assetlinks.json 접근 확인"
    Write-Host ""
    
    # 자동 복사 (선택사항)
    $response = Read-Host "assetlinks.json을 .well-known 폴더로 복사하시겠습니까? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        Set-Location ..
        New-Item -ItemType Directory -Path ".well-known" -Force | Out-Null
        Copy-Item "$TWA_DIR/assetlinks.json" ".well-known/"
        Write-Host "✅ .well-known/assetlinks.json 복사 완료!" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️  assetlinks.json 파일을 찾을 수 없습니다." -ForegroundColor Yellow
    Write-Host "   빌드가 완료된 후 수동으로 확인하세요."
}

Write-Host ""
Write-Host "🎉 빌드 완료!" -ForegroundColor Green
Write-Host ""
Write-Host "📦 생성된 파일:" -ForegroundColor Cyan
Write-Host "   - $TWA_DIR/app-release-signed.apk"
Write-Host "   - $TWA_DIR/app-release-bundle.aab"
Write-Host ""
Write-Host "다음 단계: Google Play Console에 AAB 파일 업로드" -ForegroundColor Yellow



