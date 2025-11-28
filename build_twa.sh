#!/bin/bash
# NexSupply TWA 빌드 스크립트
# Google Play Store 출시를 위한 APK/AAB 생성

set -e

echo "🚀 NexSupply TWA 빌드 시작..."

# 1. Node.js 및 Bubblewrap 확인
if ! command -v node &> /dev/null; then
    echo "❌ Node.js가 설치되지 않았습니다."
    echo "https://nodejs.org/ 에서 설치하세요."
    exit 1
fi

if ! command -v bubblewrap &> /dev/null; then
    echo "📦 Bubblewrap 설치 중..."
    npm install -g @bubblewrap/cli
fi

# 2. TWA 프로젝트 디렉토리 생성
TWA_DIR="nexsupply-twa"
if [ ! -d "$TWA_DIR" ]; then
    echo "📁 TWA 프로젝트 디렉토리 생성 중..."
    mkdir -p "$TWA_DIR"
    cd "$TWA_DIR"
    
    echo "🔨 Bubblewrap 초기화 중..."
    bubblewrap init --manifest=https://app.nexsupply.app/manifest.json
    
    echo "✅ 초기화 완료!"
    echo ""
    echo "⚠️  다음 단계:"
    echo "   1. App name: NexSupply"
    echo "   2. Package ID: com.nexsupply.app"
    echo "   3. Host URL: app.nexsupply.app"
    echo "   4. Create signing key: yes"
    echo ""
else
    echo "📁 기존 TWA 프로젝트 사용 중..."
    cd "$TWA_DIR"
fi

# 3. APK/AAB 빌드
echo "🏗️  APK/AAB 빌드 중..."
bubblewrap build

# 4. assetlinks.json 확인 및 복사
if [ -f "assetlinks.json" ]; then
    echo "✅ assetlinks.json 생성 완료!"
    echo ""
    echo "📋 다음 단계:"
    echo "   1. 프로젝트 루트에 .well-known 폴더 생성"
    echo "   2. assetlinks.json을 .well-known/ 폴더로 복사"
    echo "   3. Git에 커밋 및 푸시"
    echo "   4. https://app.nexsupply.app/.well-known/assetlinks.json 접근 확인"
    echo ""
    
    # 자동 복사 (선택사항)
    read -p "assetlinks.json을 .well-known 폴더로 복사하시겠습니까? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd ..
        mkdir -p .well-known
        cp "$TWA_DIR/assetlinks.json" .well-known/
        echo "✅ .well-known/assetlinks.json 복사 완료!"
    fi
else
    echo "⚠️  assetlinks.json 파일을 찾을 수 없습니다."
    echo "   빌드가 완료된 후 수동으로 확인하세요."
fi

echo ""
echo "🎉 빌드 완료!"
echo ""
echo "📦 생성된 파일:"
echo "   - $TWA_DIR/app-release-signed.apk"
echo "   - $TWA_DIR/app-release-bundle.aab"
echo ""
echo "다음 단계: Google Play Console에 AAB 파일 업로드"

