# .well-known 폴더

이 폴더는 Digital Asset Links를 위한 파일을 저장합니다.

## assetlinks.json

Bubblewrap으로 TWA를 빌드한 후 생성되는 `assetlinks.json` 파일을 이 폴더에 배치하세요.

### 배치 방법

1. `nexsupply-twa/assetlinks.json` 파일을 이 폴더로 복사
2. Git에 커밋 및 푸시
3. 다음 URL에서 접근 가능한지 확인:
   ```
   https://app.nexsupply.app/.well-known/assetlinks.json
   ```

### 중요 사항

- 파일명은 정확히 `assetlinks.json`이어야 합니다 (대소문자 구분)
- Content-Type은 `application/json`이어야 합니다
- HTTPS로만 접근 가능해야 합니다

