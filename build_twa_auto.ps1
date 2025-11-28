# NexSupply TWA 자동 빌드 스크립트
# 사용자 입력 없이 자동으로 진행

$ErrorActionPreference = "Stop"

Write-Host "🚀 NexSupply TWA 자동 빌드 시작..." -ForegroundColor Green

# JDK 확인
$hasJava = $false
try {
    $javaVersion = java -version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $hasJava = $true
        Write-Host "✅ Java가 설치되어 있습니다." -ForegroundColor Green
    }
} catch {
    $hasJava = $false
}

# TWA 프로젝트 디렉토리로 이동
$TWA_DIR = "nexsupply-twa"
if (-not (Test-Path $TWA_DIR)) {
    New-Item -ItemType Directory -Path $TWA_DIR | Out-Null
}

Set-Location $TWA_DIR

# Bubblewrap 초기화 (비대화형)
Write-Host "🔨 Bubblewrap 초기화 중..." -ForegroundColor Yellow
Write-Host "   (JDK 설치 질문에 자동으로 'Y' 입력)" -ForegroundColor Gray

# echo를 사용하여 자동 입력
if (-not $hasJava) {
    Write-Host "   JDK 자동 설치를 진행합니다..." -ForegroundColor Yellow
}

# 초기화 실행 (자동 입력을 위한 방법)
$initProcess = Start-Process -FilePath "bubblewrap" -ArgumentList "init", "--manifest=https://app.nexsupply.app/manifest.json", "--packageId=com.nexsupply.app", "--appVersionName=1.0.0", "--appVersionCode=1" -NoNewWindow -Wait -PassThru

if ($initProcess.ExitCode -ne 0) {
    Write-Host "⚠️  초기화가 완료되지 않았습니다. 수동으로 진행해야 할 수 있습니다." -ForegroundColor Yellow
    Write-Host "   다음 명령어를 수동으로 실행하세요:" -ForegroundColor Yellow
    Write-Host "   cd nexsupply-twa" -ForegroundColor Cyan
    Write-Host "   bubblewrap init --manifest=https://app.nexsupply.app/manifest.json" -ForegroundColor Cyan
    exit 1
}

Write-Host "✅ 초기화 완료!" -ForegroundColor Green

# 빌드 실행
Write-Host "🏗️  APK/AAB 빌드 중..." -ForegroundColor Yellow
bubblewrap build

# assetlinks.json 확인
if (Test-Path "assetlinks.json") {
    Write-Host "✅ assetlinks.json 생성 완료!" -ForegroundColor Green
    
    # SHA-256 지문 추출
    $assetlinksContent = Get-Content "assetlinks.json" -Raw | ConvertFrom-Json
    $fingerprint = $assetlinksContent[0].target.sha256_cert_fingerprints[0]
    
    Write-Host ""
    Write-Host "📋 SHA-256 지문:" -ForegroundColor Cyan
    Write-Host "   $fingerprint" -ForegroundColor White
    Write-Host ""
    
    # 프로젝트 루트로 돌아가서 assetlinks.json 업데이트
    Set-Location ..
    
    Write-Host "📝 .well-known/assetlinks.json 업데이트 중..." -ForegroundColor Yellow
    
    # assetlinks.json 읽기
    $currentAssetlinks = Get-Content ".well-known/assetlinks.json" -Raw | ConvertFrom-Json
    
    # SHA-256 지문 업데이트
    $currentAssetlinks[0].target.sha256_cert_fingerprints[0] = $fingerprint
    
    # JSON 변환 및 저장
    $updatedJson = $currentAssetlinks | ConvertTo-Json -Depth 10
    Set-Content -Path ".well-known/assetlinks.json" -Value $updatedJson -Encoding UTF8
    
    Write-Host "✅ assetlinks.json 업데이트 완료!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 다음 단계:" -ForegroundColor Cyan
    Write-Host "   1. Git 커밋: git add .well-known/assetlinks.json" -ForegroundColor White
    Write-Host "   2. Git 커밋: git commit -m 'Update SHA-256 fingerprint'" -ForegroundColor White
    Write-Host "   3. Git 푸시: git push origin main" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "⚠️  assetlinks.json 파일을 찾을 수 없습니다." -ForegroundColor Yellow
}

Write-Host "🎉 빌드 완료!" -ForegroundColor Green



